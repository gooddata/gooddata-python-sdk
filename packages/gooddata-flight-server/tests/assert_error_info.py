#  (C) 2024 GoodData Corporation
import pyarrow.flight
from gooddata_flight_server.errors.error_code import ErrorCode
from gooddata_flight_server.errors.error_info import ErrorInfo


def assert_error_code(code: int, err: pyarrow.flight.FlightError):
    info = ErrorInfo.maybe_from_pyarrow_error(err)
    assert info is not None, "The error does not contain the ErrorInfo."

    if code != info.code:
        raise AssertionError(f"Expected error code '{ErrorCode.name(code)}'. Got: '{ErrorCode.name(info.code)}'")
