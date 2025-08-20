#  (C) 2024 GoodData Corporation
import pyarrow.flight
from gooddata_flight_server.errors.error_info import ErrorInfo, RetryInfo


def test_serde_error_info1():
    error = ErrorInfo.for_reason(666, "error")
    serialized = error.to_bytes()

    deserialized = ErrorInfo.from_bytes(serialized)
    assert deserialized.code == error.code
    assert deserialized.msg == error.msg


def test_serde_error_info2():
    error = ErrorInfo.for_reason(666, "error").with_detail("detail")
    serialized = error.to_bytes()

    deserialized = ErrorInfo.from_bytes(serialized)
    assert deserialized.code == error.code
    assert deserialized.msg == error.msg
    assert deserialized.detail == error.detail


def test_error_info_limits1():
    error = ErrorInfo.for_reason(666, "error" * 500).with_detail("detail" * 500)

    assert "truncated" in error.msg
    assert "truncated" in error.detail

    error = ErrorInfo(code=666, msg="error" * 500, detail="detail" * 500)
    assert "truncated" in error.msg
    assert "truncated" in error.detail


def test_serde_retry_info1():
    retry = RetryInfo(
        flight_info=None,
        retry_descriptor=pyarrow.flight.FlightDescriptor.for_command(b"retry-cmd"),
        cancel_descriptor=pyarrow.flight.FlightDescriptor.for_command(b"cancel-cmd"),
    )
    serialized = retry.to_bytes()

    deserialized = RetryInfo.from_bytes(serialized)
    assert deserialized.flight_info == retry.flight_info
    assert deserialized.retry_descriptor == retry.retry_descriptor
    assert deserialized.cancel_descriptor == retry.cancel_descriptor


def test_serde_error_with_retry():
    retry = RetryInfo(
        flight_info=None,
        retry_descriptor=pyarrow.flight.FlightDescriptor.for_command(b"retry-cmd"),
        cancel_descriptor=pyarrow.flight.FlightDescriptor.for_command(b"cancel-cmd"),
    )
    serialized = retry.to_bytes()
    error = ErrorInfo.for_reason(666, "polling").with_body(serialized)

    serialized = error.to_bytes()
    deserialized = ErrorInfo.from_bytes(serialized)
    assert deserialized.code == error.code
    assert deserialized.msg == error.msg
    assert deserialized.detail == error.detail
    assert deserialized.body == error.body

    deserialized_retry = RetryInfo.from_bytes(deserialized.body)
    assert deserialized_retry.flight_info == retry.flight_info
    assert deserialized_retry.retry_descriptor == retry.retry_descriptor
    assert deserialized_retry.cancel_descriptor == retry.cancel_descriptor


def test_to_and_from_pyarrow1():
    error = ErrorInfo.for_reason(666, "error")
    pe = error.to_server_error()

    deserialized = ErrorInfo.from_pyarrow_error(pe)
    assert deserialized.code == error.code
    assert deserialized.msg == error.msg
    assert deserialized.detail == error.detail
    assert deserialized.body == error.body


def test_to_and_from_pyarrow2():
    deserialized = ErrorInfo.from_pyarrow_error(pyarrow.flight.FlightServerError("arrow_msg"))
    assert deserialized.code == 0
    assert len(deserialized.msg)
    assert "arrow_msg" in deserialized.msg


def test_to_and_from_pyarrow3():
    deserialized = ErrorInfo.maybe_from_pyarrow_error(pyarrow.flight.FlightServerError("arrow_msg"))
    assert deserialized is None
