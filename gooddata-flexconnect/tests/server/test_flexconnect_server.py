#  (C) 2024 GoodData Corporation
import orjson
import pyarrow.flight
import pytest
from gooddata_flight_server import ErrorCode

from tests.assert_error_info import assert_error_code
from tests.server.conftest import flexconnect_server


def test_basic_function():
    with flexconnect_server(["tests.server.funs.fun1"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        fun_infos = list(c.list_flights())
        assert len(fun_infos) == 1
        fun_info: pyarrow.flight.FlightInfo = fun_infos[0]

        assert fun_info.schema.names == ["col1", "col2", "col3"]
        assert fun_info.descriptor.command is not None
        assert len(fun_info.descriptor.command)
        cmd = orjson.loads(fun_info.descriptor.command)
        assert cmd["functionName"] == "SimpleFun1"

        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps(
                {
                    "functionName": "SimpleFun1",
                    "parameters": {"test1": 1, "test2": 2, "test3": 3},
                }
            )
        )
        info = c.get_flight_info(descriptor)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_function_with_on_load():
    """
    Function with `on_load` doing some essential initialization is handled correctly.

    The testing `fun2` is implemented in a way that is sets up the data to serve in the
    on_load. If on_load does not happen, the GetFlightInfo->DoGet would fail
    """
    with flexconnect_server(["tests.server.funs.fun2"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps(
                {
                    "functionName": "SimpleFun2",
                    "parameters": {"test1": 1, "test2": 2, "test3": 3},
                }
            )
        )

        info = c.get_flight_info(descriptor)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_basic_function_tls(tls_ca_cert):
    with flexconnect_server(["tests.server.funs.fun1"], tls=True) as s:
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        fun_infos = list(c.list_flights())
        assert len(fun_infos) == 1
        fun_info: pyarrow.flight.FlightInfo = fun_infos[0]

        assert fun_info.schema.names == ["col1", "col2", "col3"]
        assert fun_info.descriptor.command is not None
        assert len(fun_info.descriptor.command)
        cmd = orjson.loads(fun_info.descriptor.command)
        assert cmd["functionName"] == "SimpleFun1"

        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps(
                {
                    "functionName": "SimpleFun1",
                    "parameters": {"test1": 1, "test2": 2, "test3": 3},
                }
            )
        )
        info = c.get_flight_info(descriptor)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_function_with_call_deadline():
    """
    Flight RPC implementation that invokes FlexConnect can be setup with
    deadline for the invocation duration (done by GetFlightInfo).

    If the function invocation (or wait for the invocation) exceeds the
    deadline, the GetFlightInfo will fail with timeout and the underlying
    task will be cancelled (if possible).

    In these cases, the GetFlightInfo raises FlightTimedOutError with
    appropriate error code.
    """
    with flexconnect_server(["tests.server.funs.fun3"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps(
                {
                    "functionName": "LongRunningFun",
                    "parameters": {"test1": 1, "test2": 2, "test3": 3},
                }
            )
        )

        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(descriptor)

        assert_error_code(ErrorCode.TIMEOUT, e.value)
