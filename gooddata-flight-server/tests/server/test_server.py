#  (C) 2024 GoodData Corporation
from typing import Generator

import pyarrow.flight
from gooddata_flight_server.server.flight_rpc.server_methods import FlightServerMethods

from tests.server.conftest import server

_DATA1 = pyarrow.table(
    data={"col1": list(range(100))},
)

_DATA2 = pyarrow.table(
    data={"col1": list(range(100)), "col2": [f"val{x}" for x in range(100)]},
)

_DATA: dict[bytes, pyarrow.Table] = {b"data1": _DATA1, b"data2": _DATA2}

_LISTING = {
    data_id: pyarrow.flight.FlightInfo(
        schema=table.schema,
        descriptor=pyarrow.flight.FlightDescriptor.for_command(data_id),
        endpoints=[],
        total_bytes=-1,
        total_records=-1,
    )
    for data_id, table in _DATA.items()
}


class _TestingMethods(FlightServerMethods):
    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        yield from _LISTING.values()


def test_smoke():
    with server(_TestingMethods()) as s:
        c = pyarrow.flight.FlightClient(s.location)
        listing = tuple(c.list_flights())

        assert len(listing) == len(_LISTING)


def test_smoke_tls(tls_ca_cert):
    with server(_TestingMethods(), tls=True) as s:
        print(s.location)
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        listing = tuple(c.list_flights())

        assert len(listing) == len(_LISTING)
