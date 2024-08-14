# (C) 2024 GoodData Corporation
from typing import Generator

import pyarrow.flight

from gooddata_flight_server.server.flight_rpc.flight_middleware import (
    CallFinalizer,
    CallInfo,
)


class FlightServerMethods:
    """
    Base class for implementations of Flight RPC server methods.

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
