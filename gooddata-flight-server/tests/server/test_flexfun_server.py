#  (C) 2024 GoodData Corporation
import orjson
import pyarrow.flight

from tests.server.conftest import flexfun_server


def test_basic_function():
    with flexfun_server(["tests.server.funs.fun1"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        fun_infos = list(c.list_flights())
        assert len(fun_infos) == 1
        fun_info: pyarrow.flight.FlightInfo = fun_infos[0]

        assert fun_info.schema.names == ["col1", "col2", "col3"]
        assert fun_info.descriptor.command is not None
        assert len(fun_info.descriptor.command)
        cmd = orjson.loads(fun_info.descriptor.command)
        assert cmd["function_name"] == "SimpleFun"

        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps({"function_name": "SimpleFun", "parameters": {"test1": 1, "test2": 2, "test3": 3}})
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
    with flexfun_server(["tests.server.funs.fun2"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps({"function_name": "SimpleFun", "parameters": {"test1": 1, "test2": 2, "test3": 3}})
        )

        info = c.get_flight_info(descriptor)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_basic_function_tls(tls_ca_cert):
    with flexfun_server(["tests.server.funs.fun1"], tls=True) as s:
        c = pyarrow.flight.FlightClient(s.location, tls_root_certs=tls_ca_cert)
        fun_infos = list(c.list_flights())
        assert len(fun_infos) == 1
        fun_info: pyarrow.flight.FlightInfo = fun_infos[0]

        assert fun_info.schema.names == ["col1", "col2", "col3"]
        assert fun_info.descriptor.command is not None
        assert len(fun_info.descriptor.command)
        cmd = orjson.loads(fun_info.descriptor.command)
        assert cmd["function_name"] == "SimpleFun"

        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps({"function_name": "SimpleFun", "parameters": {"test1": 1, "test2": 2, "test3": 3}})
        )
        info = c.get_flight_info(descriptor)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]
