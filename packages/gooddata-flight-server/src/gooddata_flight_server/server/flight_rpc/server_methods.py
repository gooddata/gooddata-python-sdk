# (C) 2024 GoodData Corporation
from collections.abc import Generator
from typing import Optional

import pyarrow.flight
import structlog

from gooddata_flight_server.errors.error_info import ErrorCode, ErrorInfo
from gooddata_flight_server.server.flight_rpc.flight_middleware import (
    CallFinalizer,
    CallInfo,
)
from gooddata_flight_server.tasks.task_executor import TaskExecutor
from gooddata_flight_server.tasks.task_result import FlightDataTaskResult

_LOGGER = structlog.get_logger("gooddata_flight_server.rpc")


class FlightServerMethods:
    """
    Base class for implementations of Flight RPC server methods. This class contains a couple of utility
    methods that may be useful in subclasses.

    Typings reverse-engineered from PyArrow's Cython code.
    """

    @staticmethod
    def call_info_middleware(
        from_context: pyarrow.flight.ServerCallContext,
    ) -> CallInfo:
        """
        Utility method to obtain CallInfo middleware from the call context. The
        CallInfo middleware can be used to access Flight's CallInfo AND all headers
        that were passed during the call.

        :param from_context: server call context
        :return: middleware
        """
        mw = from_context.get_middleware(CallInfo.MiddlewareName)
        assert isinstance(mw, CallInfo)

        return mw

    @staticmethod
    def call_finalizer_middleware(
        from_context: pyarrow.flight.ServerCallContext,
    ) -> CallFinalizer:
        """
        Utility method to obtain CallFinalizer middleware from the call context. The
        CallFinalizer middleware can be used to register functions that should be
        called after the entire Flight RPC completes.

        See CallFinalizer documentation for more details..

        :param from_context: server call context
        :return: middleware
        """
        mw = from_context.get_middleware(CallFinalizer.MiddlewareName)
        assert isinstance(mw, CallFinalizer)

        return mw

    @staticmethod
    def do_get_task_result(
        context: pyarrow.flight.ServerCallContext, task_executor: TaskExecutor, task_id: str
    ) -> pyarrow.flight.FlightDataStream:
        """
        Utility method that creates a FlightDataStream from a result of a task that was
        previously executed. You typically want to use this in implementation of `do_get`.

        This method ensures that once the data is sent out, all necessary locks it previously
        acquired to protect the data are freed. Single-use results will be closed once they
        are sent out. The method uses current's call finalizer middleware to accomplish this.

        :param context: server call context
        :param task_executor: task executor where the task run
        :param task_id: task identifier
        :return: FlightDataStream, can be returned as-is as result of do_get
        """
        try:
            task_result = task_executor.wait_for_result(task_id)
            if task_result is None:
                raise ErrorInfo.for_reason(
                    ErrorCode.INVALID_TICKET,
                    f"Unable to serve data for task '{task_id}'. The task result is not present.",
                ).to_user_error()

            if task_result.error is not None:
                raise task_result.error.as_flight_error()

            if task_result.cancelled:
                raise ErrorInfo.for_reason(
                    ErrorCode.COMMAND_CANCELLED,
                    f"FlexConnect function invocation was cancelled. Invocation task was: '{task_result.task_id}'.",
                ).to_server_error()

            result = task_result.result
            if not isinstance(result, FlightDataTaskResult):
                raise ErrorInfo.for_reason(
                    ErrorCode.INTERNAL_ERROR,
                    f"An internal error has occurred while attempting read result for '{task_id}'."
                    f"While the result exists, it is of an unexpected type: {type(result).__name__} ",
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

            finalizer = FlightServerMethods.call_finalizer_middleware(context)
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

    ###################################################################
    # Flight RPC methods - to be implemented as needed by
    # subclasses.
    ###################################################################

    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        raise NotImplementedError

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        raise NotImplementedError

    def get_schema(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.SchemaResult:
        raise NotImplementedError

    def do_put(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.FlightMetadataWriter,
    ) -> None:
        raise NotImplementedError

    def do_get(
        self,
        context: pyarrow.flight.ServerCallContext,
        ticket: pyarrow.flight.Ticket,
    ) -> pyarrow.flight.FlightDataStream:
        raise NotImplementedError

    def do_exchange(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.MetadataRecordBatchWriter,
    ) -> None:
        raise NotImplementedError

    def list_actions(self, context: pyarrow.flight.ServerCallContext) -> list[tuple[str, str]]:
        raise NotImplementedError

    def do_action(
        self,
        context: pyarrow.flight.ServerCallContext,
        action: pyarrow.flight.Action,
    ) -> Generator[pyarrow.flight.Result, None, None]:
        raise NotImplementedError
