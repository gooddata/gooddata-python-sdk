#  (C) 2024 GoodData Corporation
from collections.abc import Generator
from typing import Optional

import orjson
import pyarrow.flight
import structlog
from gooddata_flight_server import (
    ErrorCode,
    ErrorInfo,
    FlightDataTaskResult,
    FlightServerMethods,
    ServerContext,
    TaskExecutionResult,
    TaskWaitTimeoutError,
)

from gooddata_flexfun.flex_fun import FlexFun
from gooddata_flexfun.flex_fun_registry import FlexFunRegistry
from gooddata_flexfun.flex_fun_task import FlexFunTask

_LOGGER = structlog.get_logger("gooddata_flexfun.rpc")
_DEFAULT_TASK_WAIT = 60.0


class _FlexFunServerMethods(FlightServerMethods):
    def __init__(self, ctx: ServerContext, registry: FlexFunRegistry) -> None:
        self._ctx = ctx
        self._registry = registry

    @staticmethod
    def _create_descriptor(fun_name: str, metadata: Optional[dict]) -> pyarrow.flight.FlightDescriptor:
        cmd = {
            "function_name": fun_name,
            "metadata": metadata,
        }

        return pyarrow.flight.FlightDescriptor.for_command(orjson.dumps(cmd))

    def _create_fun_info(self, fun: type[FlexFun]) -> pyarrow.flight.FlightInfo:
        # these are for type checker; the registry will only register functions
        # that have proper metadata on them
        assert fun.Name is not None
        assert fun.Schema is not None

        return pyarrow.flight.FlightInfo(
            schema=fun.Schema,
            descriptor=self._create_descriptor(fun.Name, fun.Metadata),
            endpoints=[],
            total_bytes=-1,
            total_records=-1,
        )

    def _extract_invocation_payload(
        self, descriptor: pyarrow.flight.FlightDescriptor
    ) -> tuple[str, dict, Optional[tuple[str, ...]]]:
        if descriptor.command is None or not len(descriptor.command):
            raise ErrorInfo.bad_argument(
                "Incorrect FlexFun invocation. Flight descriptor must contain command with the invocation payload."
            )

        try:
            payload = orjson.loads(descriptor.command)
        except Exception:
            raise ErrorInfo.bad_argument("Incorrect FlexFun invocation. The invocation payload is not a valid JSON.")

        fun = payload.get("function_name")
        if fun is None or not len(fun):
            raise ErrorInfo.bad_argument(
                "Incorrect FlexFun invocation. The invocation payload does not specify 'function_name'."
            )

        parameters = payload.get("parameters") or {}
        columns = parameters.get("columns")

        return fun, parameters, columns

    def _prepare_task(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> FlexFunTask:
        fun_name, parameters, columns = self._extract_invocation_payload(descriptor)
        headers = self.call_info_middleware(context).headers
        flex_fun = self._registry.create_function(fun_name)

        return FlexFunTask(
            fun=flex_fun,
            parameters=parameters,
            columns=columns,
            headers=headers,
            cmd=descriptor.command,
        )

    def _prepare_flight_info(self, task_result: TaskExecutionResult) -> pyarrow.flight.FlightInfo:
        if task_result.error is not None:
            raise task_result.error.as_flight_error()

        if task_result.cancelled:
            raise ErrorInfo.for_reason(
                ErrorCode.COMMAND_CANCELLED,
                f"FlexFun invocation was cancelled. Invocation task was: '{task_result.task_id}'.",
            ).to_server_error()

        result = task_result.result
        assert isinstance(result, FlightDataTaskResult)

        return pyarrow.flight.FlightInfo(
            schema=result.get_schema(),
            descriptor=pyarrow.flight.FlightDescriptor.for_command(task_result.cmd),
            endpoints=[
                pyarrow.flight.FlightEndpoint(
                    ticket=pyarrow.flight.Ticket(ticket=orjson.dumps({"task_id": task_result.task_id})),
                    locations=[self._ctx.location],
                )
            ],
            total_records=-1,
            total_bytes=-1,
        )

    ###################################################################
    # Implementation of Flight RPC methods
    ###################################################################

    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        structlog.contextvars.bind_contextvars(peer=context.peer())
        _LOGGER.info("list_flights", available_funs=self._registry.flex_funs_names)

        return (self._create_fun_info(fun) for fun in self._registry.flex_funs.values())

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        structlog.contextvars.bind_contextvars(peer=context.peer())
        task: Optional[FlexFunTask] = None

        try:
            task = self._prepare_task(context, descriptor)
            self._ctx.task_executor.submit(task)

            try:
                # XXX: this should be enhanced to implement polling
                task_result = self._ctx.task_executor.wait_for_result(task.task_id, _DEFAULT_TASK_WAIT)
            except TaskWaitTimeoutError:
                raise ErrorInfo.for_reason(
                    ErrorCode.TIMEOUT, f"GetFlightInfo timed out while waiting for task {task.task_id}."
                ).to_timeout_error()

            # if this bombs then there must be something really wrong because the task
            # was clearly submitted and code was waiting for its completion. this invariant
            # should not happen in this particular code path. The None return value may
            # be applicable one day when polling is in use and a request comes to check whether
            # particular task id finished
            assert task_result is not None

            return self._prepare_flight_info(task_result)
        except Exception:
            if task is not None:
                _LOGGER.error("get_flight_info_failed", task_id=task.task_id, fun=task.fun_name, exc_info=True)
            else:
                _LOGGER.error("flexfun_submit_failed", exc_info=True)

            raise

    def do_get(
        self,
        context: pyarrow.flight.ServerCallContext,
        ticket: pyarrow.flight.Ticket,
    ) -> pyarrow.flight.FlightDataStream:
        structlog.contextvars.bind_contextvars(peer=context.peer())

        try:
            try:
                ticket_payload = orjson.loads(ticket.ticket)
            except Exception:
                raise ErrorInfo.bad_argument("Incorrect ticket payload. The ticket payload is not a valid JSON.")

            task_id = ticket_payload.get("task_id")
            if task_id is None or not len(task_id):
                raise ErrorInfo.bad_argument("Incorrect ticket payload. The ticket payload does not specify 'task_id'.")

            task_result = self._ctx.task_executor.wait_for_result(task_id)
            if task_result is None:
                raise ErrorInfo.for_reason(
                    ErrorCode.INVALID_TICKET,
                    f"Unable to serve data for task '{task_id}'. The task result is not present.",
                ).to_user_error()

            result = task_result.result
            if not isinstance(result, FlightDataTaskResult):
                raise ErrorInfo.for_reason(
                    ErrorCode.INTERNAL_ERROR,
                    f"An internal error has occurred while attempting read result for '{task_id}'."
                    f"While the result exists, it is of an unexpected type. "
                    f"This is a bug in FlexFun server implementation.",
                ).to_internal_error()

            rlock, data = result.acquire_data()

            def _on_end(_: Optional[pyarrow.ArrowException]) -> None:
                """
                Once the request that streams the data out is done, make sure
                to release the read-lock. Single-use results are closed at
                this point because the data cannot be read again anyway.
                """
                rlock.release()

                if result.single_use_data:
                    # note: results with single-use data can only ever have one active
                    #  reader (e.g. this one). since the rlock is now released the
                    #  close will proceed without chance of being blocked
                    try:
                        result.close()
                    except Exception:
                        # log and sink these Exceptions - not much to do
                        _LOGGER.error("do_get_close_failed", exc_info=True)

            finalizer = self.call_finalizer_middleware(context)
            finalizer.register_on_end(_on_end)

            if isinstance(data, pyarrow.Table):
                _LOGGER.info("do_get_table", task_id=task_id, num_rows=data.num_rows)

                return pyarrow.flight.RecordBatchStream(data)
            elif isinstance(data, pyarrow.RecordBatchReader):
                _LOGGER.info("do_get_reader", task_id=task_id)

                return pyarrow.flight.RecordBatchStream(data)

            _LOGGER.info("do_get_generator", task_id=task_id)
            return pyarrow.flight.GeneratorStream(data)
        except Exception:
            _LOGGER.error("do_get_failed", exc_info=True)
            raise


_FLEXFUN_CONFIG_SECTION = "flexfun"
_FLEXFUN_FUNCTION_LIST = "functions"


def create_flexfun_flight_methods(ctx: ServerContext) -> FlightServerMethods:
    """
    This factory creates implementation of Flight RPC methods that realize the FlexFun server.

    FlexFun Server hosts one or more functions developed externally, and linked to the server
    at runtime - during startup.

    :param ctx: server's context
    :return: new instance of Flight RPC server methods to integrate into the server
    """
    modules = list(ctx.settings.get(f"{_FLEXFUN_CONFIG_SECTION}.{_FLEXFUN_FUNCTION_LIST}") or [])
    _LOGGER.info("flexfun_init", modules=modules)
    registry = FlexFunRegistry().load(ctx, modules)

    return _FlexFunServerMethods(ctx, registry)
