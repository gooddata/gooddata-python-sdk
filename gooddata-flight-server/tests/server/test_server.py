#  (C) 2024 GoodData Corporation
import os
from collections.abc import Generator

import pyarrow.flight
import pytest
from gooddata_flight_server.server.flight_rpc.server_methods import (
    FlightServerMethods,
)
from pyarrow._flight import FlightCallOptions

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
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        listing = tuple(c.list_flights())

        assert len(listing) == len(_LISTING)


def test_smoke_with_auth_fail1(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_ENUMERATED_TOKENS__TOKENS"] = '["t1", "t2"]'

    with server(_TestingMethods(), tls=True) as s, pytest.raises(pyarrow.flight.FlightUnauthenticatedError):
        list(pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert).list_flights())


def test_smoke_with_auth_fail2(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_ENUMERATED_TOKENS__TOKENS"] = '["t1", "t2"]'

    # important: header names must be lowercase
    opts = FlightCallOptions(headers=[(b"authorization", b"Bearer 123")])
    with server(_TestingMethods(), tls=True) as s, pytest.raises(pyarrow.flight.FlightUnauthenticatedError):
        list(pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert).list_flights(b"", opts))


def test_smoke_with_auth1(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_ENUMERATED_TOKENS__TOKENS"] = '["t1", "t2"]'

    opts = FlightCallOptions(headers=[(b"authorization", b"Bearer t1")])
    with server(_TestingMethods(), tls=True) as s:
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        listing = tuple(c.list_flights(b"", opts))

        assert len(listing) == len(_LISTING)


def test_smoke_with_custom_auth1(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_HEADER_NAME"] = "x-custom-token-header"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_VERIFICATION"] = "tests.server.testing_token_verifier"

    opts = FlightCallOptions(headers=[(b"x-custom-token-header", b"test_token")])
    with server(_TestingMethods(), tls=True) as s:
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        listing = tuple(c.list_flights(b"", opts))

        assert len(listing) == len(_LISTING)


def test_smoke_with_custom_auth_fail1(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_HEADER_NAME"] = "x-custom-token-header"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_VERIFICATION"] = "tests.server.testing_token_verifier"

    opts = FlightCallOptions(headers=[(b"x-some-bad-header", b"test_token")])
    with server(_TestingMethods(), tls=True) as s, pytest.raises(pyarrow.flight.FlightUnauthenticatedError):
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        tuple(c.list_flights(b"", opts))


def test_smoke_with_custom_auth_fail2(tls_ca_cert):
    os.environ["GOODDATA_FLIGHT_SERVER__AUTHENTICATION_METHOD"] = "token"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_HEADER_NAME"] = "x-custom-token-header"
    os.environ["GOODDATA_FLIGHT_SERVER__TOKEN_VERIFICATION"] = "tests.server.testing_token_verifier"

    opts = FlightCallOptions(headers=[(b"x-custom-token-header", b"invalid")])
    with server(_TestingMethods(), tls=True) as s, pytest.raises(pyarrow.flight.FlightUnauthenticatedError):
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        tuple(c.list_flights(b"", opts))
