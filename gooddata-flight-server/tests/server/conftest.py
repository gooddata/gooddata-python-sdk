#  (C) 2024 GoodData Corporation
import contextlib
import os
import socket
from contextlib import closing
from typing import Union

from gooddata_flight_server.server.flight_rpc.server_methods import FlightServerMethods
from gooddata_flight_server.server.method_factory import FlightServerMethodsFactory
from gooddata_flight_server.server.server_main import GoodDataFlightServer, create_server


def _find_free_port():
    """
    see: https://stackoverflow.com/a/45690594
    """
    with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
        s.bind(("127.0.0.1", 0))
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        return s.getsockname()[1]


@contextlib.contextmanager
def server(methods: Union[FlightServerMethods, FlightServerMethodsFactory]) -> GoodDataFlightServer:
    port = _find_free_port()
    os.environ["GOODDATA_FLIGHT_SERVER__LISTEN_PORT"] = str(port)
    os.environ["GOODDATA_FLIGHT_SERVER__ADVERTISE_HOST"] = "127.0.0.1"

    _server = create_server(methods)
    _server.start()

    started = _server.wait_for_start(timeout=5.0)
    if not started:
        raise AssertionError(f"Test fixture unable to start server in time on port {port}.")

    yield _server

    _server.stop()
    _server.wait_for_stop()
