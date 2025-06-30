#  (C) 2024 GoodData Corporation
import pyarrow.flight
import pytest
from gooddata_flexconnect.function.function_registry import FlexConnectFunctionRegistry
from gooddata_flight_server import ErrorCode, ServerContext

from tests.assert_error_info import assert_error_code
from tests.function.testing_funs import Fun1, Fun2


@pytest.fixture(scope="module")
def fake_ctx():
    # the context is faked for these unit tests and is not really valid.
    # but that is not so important during the registry unit tests that
    # need to ensure that the functions are registered correctly and that
    # their on_load() initializers are called
    return ServerContext(
        config=None,
        location=pyarrow.flight.Location.for_grpc_tcp("localhost", 6666),
        settings=None,
        task_executor=None,
        health=None,
    )


def test_registry1(fake_ctx):
    r = FlexConnectFunctionRegistry()
    r.register(fake_ctx, Fun1)

    assert "fun1" in r.functions


def test_load_from_modules(fake_ctx):
    r = FlexConnectFunctionRegistry()

    # reset the indicator (previous tests may have registered this fun)
    Fun2.OnLoadCalled = False
    r.load(fake_ctx, modules=["tests.function.testing_funs"])

    assert "fun1" in r.functions
    assert "fun2" in r.functions
    assert len(r.functions) == 2
    assert Fun2.OnLoadCalled is True

    assert isinstance(r.create_function("fun1"), Fun1)
    assert isinstance(r.create_function("fun2"), Fun2)


def test_create_when_missing():
    r = FlexConnectFunctionRegistry()

    with pytest.raises(pyarrow.flight.FlightServerError) as e:
        r.create_function("fun1")

    assert_error_code(ErrorCode.BAD_ARGUMENT, e.value)
