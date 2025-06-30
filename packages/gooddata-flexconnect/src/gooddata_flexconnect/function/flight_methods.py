#  (C) 2024 GoodData Corporation
import time
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
    flight_server_methods,
)

from gooddata_flexconnect.function.function import FlexConnectFunction
from gooddata_flexconnect.function.function_invocation import (
    CancelInvocation,
    RetryInvocation,
    SubmitInvocation,
    extract_pollable_invocation_from_descriptor,
    extract_submit_invocation_from_descriptor,
)
from gooddata_flexconnect.function.function_registry import FlexConnectFunctionRegistry
from gooddata_flexconnect.function.function_task import FlexConnectFunctionTask

_LOGGER = structlog.get_logger("gooddata_flexconnect.rpc")

POLLING_HEADER_NAME = "x-quiver-pollable"
"""
If this header is present on the get flight info call, the polling extension will be used.
Otherwise the basic do get will be used.
"""


def _prepare_poll_error(task_id: str) -> pyarrow.flight.FlightError:
    return ErrorInfo.poll(
        flight_info=None,
        cancel_descriptor=pyarrow.flight.FlightDescriptor.for_command(f"c:{task_id}".encode()),
        retry_descriptor=pyarrow.flight.FlightDescriptor.for_command(f"r:{task_id}".encode()),
    )


class _FlexConnectServerMethods(FlightServerMethods):
    def __init__(
        self,
        ctx: ServerContext,
        registry: FlexConnectFunctionRegistry,
        call_deadline_ms: float,
        poll_interval_ms: float,
    ) -> None:
        self._ctx = ctx
        self._registry = registry
        self._call_deadline = call_deadline_ms / 1000
        self._poll_interval = poll_interval_ms / 1000

    @staticmethod
    def _create_descriptor(fun_name: str, metadata: Optional[dict]) -> pyarrow.flight.FlightDescriptor:
        cmd = {
            "functionName": fun_name,
            "metadata": metadata,
        }

        return pyarrow.flight.FlightDescriptor.for_command(orjson.dumps(cmd))

    def _create_fun_info(self, fun: type[FlexConnectFunction]) -> pyarrow.flight.FlightInfo:
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

    def _prepare_task(
        self,
        context: pyarrow.flight.ServerCallContext,
        submit_invocation: SubmitInvocation,
    ) -> FlexConnectFunctionTask:
        headers = self.call_info_middleware(context).headers
        fun = self._registry.create_function(submit_invocation.function_name)

        return FlexConnectFunctionTask(
            fun=fun,
            parameters=submit_invocation.parameters,
            columns=submit_invocation.columns,
            headers=headers,
            cmd=submit_invocation.command,
        )

    def _prepare_flight_info(
        self, task_id: str, task_result: Optional[TaskExecutionResult]
    ) -> pyarrow.flight.FlightInfo:
        if task_result is None:
            raise ErrorInfo.for_reason(
                ErrorCode.BAD_ARGUMENT, f"Task with id '{task_id}' does not exist."
            ).to_user_error()

        if task_result.error is not None:
            raise task_result.error.as_flight_error()

        if task_result.cancelled:
            raise ErrorInfo.for_reason(
                ErrorCode.COMMAND_CANCELLED,
                f"FlexConnect function invocation was cancelled. Invocation task was: '{task_id}'.",
            ).to_server_error()

        result = task_result.result
        assert isinstance(result, FlightDataTaskResult)

        return pyarrow.flight.FlightInfo(
            schema=result.get_schema(),
            descriptor=pyarrow.flight.FlightDescriptor.for_command(task_result.cmd),
            endpoints=[
                pyarrow.flight.FlightEndpoint(
                    ticket=pyarrow.flight.Ticket(ticket=orjson.dumps({"task_id": task_id})),
                    locations=[self._ctx.location],
                )
            ],
            total_records=-1,
            total_bytes=-1,
        )

    def _get_flight_info_no_polling(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        """
        Basic DoGetInfo flow with no polling extension.
        This conforms to the mainline Arrow Flight RPC specification.
        """
        structlog.contextvars.bind_contextvars(peer=context.peer())
        invocation = extract_submit_invocation_from_descriptor(descriptor)

        task: Optional[FlexConnectFunctionTask] = None

        try:
            task = self._prepare_task(context, invocation)
            self._ctx.task_executor.submit(task)

            try:
                task_result = self._ctx.task_executor.wait_for_result(task.task_id, self._call_deadline)
            except TaskWaitTimeoutError:
                cancelled = self._ctx.task_executor.cancel(task.task_id)
                _LOGGER.warning(
                    "flexconnect_fun_call_timeout", task_id=task.task_id, fun=task.fun_name, cancelled=cancelled
                )

                raise ErrorInfo.for_reason(
                    ErrorCode.TIMEOUT, f"GetFlightInfo timed out while waiting for task {task.task_id}."
                ).to_timeout_error()

            # if this bombs then there must be something really wrong because the task
            # was clearly submitted and code was waiting for its completion. this invariant
            # should not happen in this particular code path. The None return value may
            # be applicable one day when polling is in use and a request comes to check whether
            # particular task id finished
            assert task_result is not None

            return self._prepare_flight_info(task_id=task.task_id, task_result=task_result)
        except Exception:
            if task is not None:
                _LOGGER.error(
                    "get_flight_info_failed", task_id=task.task_id, fun=task.fun_name, exc_info=True, polling=False
                )
            else:
                _LOGGER.error("flexconnect_fun_submit_failed", exc_info=True, polling=False)
            raise

    def _get_flight_info_polling(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        """
        DoGetInfo flow with polling extension.
        This extends the mainline Arrow Flight RPC specification with polling capabilities using the RetryInfo
        encoded into the FlightTimedOutError.extra_info.
        Ideally, we would use the mainline PollFlightInfo, but that has yet to be implemented in the PyArrow library.
        """
        structlog.contextvars.bind_contextvars(peer=context.peer())
        invocation = extract_pollable_invocation_from_descriptor(descriptor)

        task_id: str
        fun_name: Optional[str] = None

        if isinstance(invocation, CancelInvocation):
            # cancel the given task and raise cancellation exception
            if self._ctx.task_executor.cancel(invocation.task_id):
                raise ErrorInfo.for_reason(
                    ErrorCode.COMMAND_CANCELLED, "FlexConnect function invocation was cancelled."
                ).to_cancelled_error()
            raise ErrorInfo.for_reason(
                ErrorCode.COMMAND_CANCEL_NOT_POSSIBLE, "FlexConnect function invocation could not be cancelled."
            ).to_cancelled_error()
        elif isinstance(invocation, RetryInvocation):
            # retry descriptor: extract the task_id, do not submit it again and do one polling iteration
            task_id = invocation.task_id
        elif isinstance(invocation, SubmitInvocation):
            # basic first-time submit: submit the task and do one polling iteration.
            # do not check call deadline to give it a chance to wait for the result at least once
            try:
                task = self._prepare_task(context, invocation)
                self._ctx.task_executor.submit(task)
                task_id = task.task_id
                fun_name = task.fun_name
            except Exception:
                _LOGGER.error("flexconnect_fun_submit_failed", exc_info=True, polling=True)
                raise
        else:
            # can be replaced by assert_never when we are on 3.11
            raise AssertionError

        try:
            task_result = self._ctx.task_executor.wait_for_result(task_id, timeout=self._poll_interval)
            return self._prepare_flight_info(task_id, task_result)
        except TimeoutError:
            # first, check the call deadline for the whole call duration
            task_timestamp = self._ctx.task_executor.get_task_submitted_timestamp(task_id)
            if task_timestamp is not None and time.perf_counter() - task_timestamp > self._call_deadline:
                self._ctx.task_executor.cancel(task_id)
                raise ErrorInfo.for_reason(
                    ErrorCode.TIMEOUT, f"GetFlightInfo timed out while waiting for task {task_id}."
                ).to_timeout_error()

            # if the result is not ready, and we still have time, indicate to the client
            # how to poll for the results
            raise _prepare_poll_error(task_id)
        except Exception:
            _LOGGER.error("get_flight_info_failed", task_id=task_id, fun=fun_name, exc_info=True, polling=True)
            raise

    ###################################################################
    # Implementation of Flight RPC methods
    ###################################################################

    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        structlog.contextvars.bind_contextvars(peer=context.peer())
        _LOGGER.info("list_flights", available_funs=self._registry.function_names)

        return (self._create_fun_info(fun) for fun in self._registry.functions.values())

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        structlog.contextvars.bind_contextvars(peer=context.peer())

        headers = self.call_info_middleware(context).headers
        allow_polling = headers.get(POLLING_HEADER_NAME) is not None

        if allow_polling:
            return self._get_flight_info_polling(context, descriptor)
        else:
            return self._get_flight_info_no_polling(context, descriptor)

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

            return self.do_get_task_result(context, self._ctx.task_executor, task_id)
        except Exception:
            _LOGGER.error("do_get_failed", exc_info=True)
            raise


_FLEX_CONNECT_CONFIG_SECTION = "flexconnect"
_FLEX_CONNECT_FUNCTION_LIST = "functions"
_FLEX_CONNECT_CALL_DEADLINE_MS = "call_deadline_ms"
_FLEX_CONNECT_POLLING_INTERVAL_MS = "polling_interval_ms"
_DEFAULT_FLEX_CONNECT_CALL_DEADLINE_MS = 180_000
_DEFAULT_FLEX_CONNECT_POLLING_INTERVAL_MS = 2000


def _read_call_deadline_ms(ctx: ServerContext) -> int:
    call_deadline = ctx.settings.get(f"{_FLEX_CONNECT_CONFIG_SECTION}.{_FLEX_CONNECT_CALL_DEADLINE_MS}")
    if call_deadline is None:
        return _DEFAULT_FLEX_CONNECT_CALL_DEADLINE_MS

    try:
        call_deadline_ms = int(call_deadline)
        if call_deadline_ms <= 0:
            raise ValueError()

        return call_deadline_ms
    except ValueError:
        raise ValueError(
            f"Value of {_FLEX_CONNECT_CONFIG_SECTION}.{_FLEX_CONNECT_CALL_DEADLINE_MS} must "
            f"be a positive number - duration, in milliseconds, that FlexConnect function "
            f"calls are expected to run."
        )


def _read_polling_interval_ms(ctx: ServerContext) -> int:
    polling_interval = ctx.settings.get(f"{_FLEX_CONNECT_CONFIG_SECTION}.{_FLEX_CONNECT_POLLING_INTERVAL_MS}")
    if polling_interval is None:
        return _DEFAULT_FLEX_CONNECT_POLLING_INTERVAL_MS

    try:
        polling_interval = int(polling_interval)
        if polling_interval <= 0:
            raise ValueError()
        return polling_interval
    except ValueError:
        raise ValueError(
            f"Value of {_FLEX_CONNECT_CONFIG_SECTION}.{_FLEX_CONNECT_POLLING_INTERVAL_MS} must "
            f"be a positive number - duration, in milliseconds, that FlexConnect function "
            f"waits for the result during one polling iteration."
        )


@flight_server_methods
def create_flexconnect_flight_methods(ctx: ServerContext) -> FlightServerMethods:
    """
    This factory creates implementation of Flight RPC methods that realize the FlexConnect server.

    FlexConnect Server hosts one or more functions developed externally, and linked to the server
    at runtime - during startup.

    :param ctx: server's context
    :return: new instance of Flight RPC server methods to integrate into the server
    """
    modules = list(ctx.settings.get(f"{_FLEX_CONNECT_CONFIG_SECTION}.{_FLEX_CONNECT_FUNCTION_LIST}") or [])
    call_deadline_ms = _read_call_deadline_ms(ctx)
    polling_interval_ms = _read_polling_interval_ms(ctx)

    _LOGGER.info("flexconnect_init", modules=modules)
    registry = FlexConnectFunctionRegistry().load(ctx, modules)

    return _FlexConnectServerMethods(ctx, registry, call_deadline_ms, polling_interval_ms)
