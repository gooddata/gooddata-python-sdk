#  (C) 2024 GoodData Corporation

import orjson
import pyarrow.flight
import pytest
from gooddata_flexconnect.function.flight_methods import POLLING_HEADER_NAME
from gooddata_flight_server import ErrorCode, ErrorInfo, RetryInfo

from tests.assert_error_info import assert_error_code
from tests.server.conftest import flexconnect_server


@pytest.fixture
def call_options_with_polling():
    return pyarrow.flight.FlightCallOptions(headers=[(POLLING_HEADER_NAME.encode(), b"true")])


def test_basic_function():
    """
    This function should return immediately when called, no polling allowed.
    """
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


def test_cancellable_function(call_options_with_polling):
    """
    This function should return immediately when called, no polling necessary even if enabled.
    """
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
        info = c.get_flight_info(descriptor, call_options_with_polling)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_cancellable_function_tls(tls_ca_cert, call_options_with_polling):
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
        info = c.get_flight_info(descriptor, call_options_with_polling)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]


def test_cancellable_function_with_polling(call_options_with_polling):
    """
    Flight RPC implementation that invokes FlexConnect can return a polling info.

    This way, the client can poll for results that take longer to complete.
    """
    with flexconnect_server(["tests.server.funs.fun4"]) as s:
        c = pyarrow.flight.FlightClient(s.location)
        descriptor = pyarrow.flight.FlightDescriptor.for_command(
            orjson.dumps(
                {
                    "functionName": "PollableFun",
                    "parameters": {"test1": 1, "test2": 2, "test3": 3},
                }
            )
        )

        # the function is set to sleep a bit longer than the polling interval,
        # so the first iteration returns retry info in the exception
        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.POLL, e.value)

        error_info = ErrorInfo.from_bytes(e.value.extra_info)
        retry_info = RetryInfo.from_bytes(error_info.body)

        # use the retry info to poll again for the result,
        # now it should be ready and returned normally
        info = c.get_flight_info(retry_info.retry_descriptor, call_options_with_polling)
        data: pyarrow.Table = c.do_get(info.endpoints[0].ticket).read_all()

        assert len(data) == 3
        assert data.column_names == ["col1", "col2", "col3"]

        # also check that trying to cancel already completed task results in cancelled with correct code
        with pytest.raises(pyarrow.flight.FlightCancelledError) as e:
            c.get_flight_info(retry_info.cancel_descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.COMMAND_CANCELLED, e.value)


def test_cancellable_function_with_call_deadline(call_options_with_polling):
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

        # the initial submit returns polling info
        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.POLL, e.value)

        error_info = ErrorInfo.from_bytes(e.value.extra_info)
        retry_info = RetryInfo.from_bytes(error_info.body)

        # the next poll still returns polling info
        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(retry_info.retry_descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.POLL, e.value)

        # the third one reaches the deadline so the Timeout code is returned instead
        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(retry_info.retry_descriptor, call_options_with_polling)

        assert_error_code(ErrorCode.TIMEOUT, e.value)


def test_cancellable_function_with_cancellation(call_options_with_polling):
    """
    Run a long-running function and cancel it after one poll iteration.
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

        # the initial submit returns polling info
        with pytest.raises(pyarrow.flight.FlightTimedOutError) as e:
            c.get_flight_info(descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.POLL, e.value)

        error_info = ErrorInfo.from_bytes(e.value.extra_info)
        retry_info = RetryInfo.from_bytes(error_info.body)

        # use the poll info to cancel the task
        with pytest.raises(pyarrow.flight.FlightCancelledError) as e:
            c.get_flight_info(retry_info.cancel_descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.COMMAND_CANCELLED, e.value)

        # even multiple cancellations return the same error
        with pytest.raises(pyarrow.flight.FlightCancelledError) as e:
            c.get_flight_info(retry_info.cancel_descriptor, call_options_with_polling)

        assert e.value is not None
        assert_error_code(ErrorCode.COMMAND_CANCELLED, e.value)
