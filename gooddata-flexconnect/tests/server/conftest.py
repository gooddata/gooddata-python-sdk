#  (C) 2024 GoodData Corporation
import contextlib
import os
import socket
from collections.abc import Iterable
from contextlib import closing
from pathlib import Path
from typing import Union

import pytest
from gooddata_flexconnect.function.flight_methods import (
    create_flexconnect_flight_methods,
)
from gooddata_flight_server import FlightServerMethods, FlightServerMethodsFactory, GoodDataFlightServer, create_server

_CURRENT_DIR = Path(__file__).parent
_TLS_DIR = _CURRENT_DIR / "tls"


def _find_free_port():
    """
    see: https://stackoverflow.com/a/45690594
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


def _clean_env_vars():
    to_drop = [key for key in os.environ if key.startswith("GOODDATA_FLIGHT")]

    for key in to_drop:
        os.environ.pop(key, None)


@contextlib.contextmanager
def server(
    methods: Union[FlightServerMethods, FlightServerMethodsFactory],
    tls: bool = False,
    mtls: bool = False,
) -> GoodDataFlightServer:
    port = _find_free_port()
    os.environ["GOODDATA_FLIGHT_SERVER__LISTEN_PORT"] = str(port)
    os.environ["GOODDATA_FLIGHT_SERVER__ADVERTISE_HOST"] = "localhost"

    if tls:
        cert = os.path.join(_TLS_DIR, "server-cert.pem")
        key = os.path.join(_TLS_DIR, "server-key.pem")
        os.environ["GOODDATA_FLIGHT_SERVER__USE_TLS"] = "TRUE"
        os.environ["GOODDATA_FLIGHT_SERVER__TLS_CERTIFICATE"] = f"@{cert}"
        os.environ["GOODDATA_FLIGHT_SERVER__TLS_PRIVATE_KEY"] = f"@{key}"

    if mtls:
        ca_cert = os.path.join(_TLS_DIR, "ca-cert.pem")
        os.environ["GOODDATA_FLIGHT_SERVER__TLS_ROOT_CERTIFICATE"] = f"@{ca_cert}"

    _server = create_server(methods)
    _server.start()

    # started = _server.wait_for_start(timeout=5.0)
    started = _server.wait_for_start()
    if not started:
        raise AssertionError(f"Test fixture unable to start server in time on port {port}.")

    yield _server

    _clean_env_vars()
    _server.stop()
    _server.wait_for_stop()


@contextlib.contextmanager
def flexconnect_server(
    modules: Iterable[str],
    tls: bool = False,
    mtls: bool = False,
) -> GoodDataFlightServer:
    funs = ", ".join([f'"{module}"' for module in modules])
    funs = f"[{funs}]"

    os.environ["GOODDATA_FLIGHT_FLEXCONNECT__FUNCTIONS"] = funs
    os.environ["GOODDATA_FLIGHT_FLEXCONNECT__CALL_DEADLINE_MS"] = "500"

    with server(create_flexconnect_flight_methods, tls, mtls) as s:
        yield s


@pytest.fixture(scope="session")
def tls_ca_cert():
    with open(os.path.join(_TLS_DIR, "ca-cert.pem"), "rb") as f:
        return f.read()


@pytest.fixture(scope="session")
def tls_client_cert():
    with open(os.path.join(_TLS_DIR, "client-cert.pem"), "rb") as f:
        return f.read()


@pytest.fixture(scope="session")
def tls_client_key():
    with open(os.path.join(_TLS_DIR, "client-key.pem"), "rb") as f:
        return f.read()
