#  (C) 2023 GoodData Corporation
from collections.abc import Generator

import pyarrow.flight

from gooddata_flight_server.errors.error_info import ErrorInfo
from gooddata_flight_server.server.base.server_methods import FlightServerMethods


class FlightServerUnavailable(FlightServerMethods):
    """
    This implementation of `FlightServerMethods` will raise FlightUnavailableError when handling any RPC
    method.
    """

    def __init__(self, err: ErrorInfo):
        self._err = err

    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        raise self._err.to_unavailable_error()

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        raise self._err.to_unavailable_error()

    def get_schema(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.SchemaResult:
        raise self._err.to_unavailable_error()

    def do_put(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.FlightMetadataWriter,
    ) -> None:
        raise self._err.to_unavailable_error()

    def do_get(
        self, context: pyarrow.flight.ServerCallContext, ticket: pyarrow.flight.Ticket
    ) -> pyarrow.flight.FlightDataStream:
        raise self._err.to_unavailable_error()

    def do_exchange(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.MetadataRecordBatchWriter,
    ) -> None:
        raise self._err.to_unavailable_error()

    def list_actions(self, context: pyarrow.flight.ServerCallContext) -> list[tuple[str, str]]:
        raise self._err.to_unavailable_error()

    def do_action(
        self, context: pyarrow.flight.ServerCallContext, action: pyarrow.flight.Action
    ) -> Generator[pyarrow.flight.Result, None, None]:
        raise self._err.to_unavailable_error()
