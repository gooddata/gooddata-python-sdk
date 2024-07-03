# (C) 2022 GoodData Corporation
from collections.abc import Generator

import pyarrow.flight


class FlightServerMethods:
    """
    Base class for implementations of Flight RPC server methods.

    Typings reverse-engineered from PyArrow's Cython code.
    """

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
        self, context: pyarrow.flight.ServerCallContext, ticket: pyarrow.flight.Ticket
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
        self, context: pyarrow.flight.ServerCallContext, action: pyarrow.flight.Action
    ) -> Generator[pyarrow.flight.Result, None, None]:
        raise NotImplementedError
