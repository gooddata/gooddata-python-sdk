#  (C) 2024 GoodData Corporation
import base64
import traceback
from typing import Callable, Optional, Union, cast

import orjson
import pyarrow.flight

from gooddata_flight_server.errors.error_code import ErrorCode

_ERROR_INFO_MAX_MSG = 256
_ERROR_INFO_MAX_DETAIL = 512


def _truncate_str_value(val: Optional[str], max_len: int) -> Optional[str]:
    if val is None:
        return None

    if len(val) <= max_len:
        return val

    # no big deal that the actual max length is slightly exceeded
    # all this truncating happens because ErrorInfo is eventually
    # passed via gRPC headers which have 16k hard limit
    return val[:max_len] + " [truncated]"


class ErrorInfo:
    """
    Error info that should be used to construct Flight RPC errors. Never create Flight RPC Errors directly, instead use
    this class to construct a detailed error and then use one of the to_*_error() factories.
    """

    def __init__(
        self,
        msg: str,
        detail: Optional[str] = None,
        body: Optional[bytes] = None,
        code: int = 0,
    ) -> None:
        self._msg = cast(str, _truncate_str_value(msg, _ERROR_INFO_MAX_MSG))
        self._detail: Optional[str] = _truncate_str_value(detail, _ERROR_INFO_MAX_DETAIL)
        self._body: Optional[bytes] = body
        self._code: int = code

    @property
    def msg(self) -> str:
        """
        :return: human-readable error message
        """
        return self._msg

    @property
    def code(self) -> int:
        """
        :return: error code for categorization; see ErrorCode for more
        """
        return self._code

    @property
    def detail(self) -> Optional[str]:
        """
        :return: a human-readable error detail; if included may help with error diagnostics
        """
        return self._detail

    @property
    def body(self) -> Optional[bytes]:
        """
        :return: error body, suitable for programmatic consumption; used by server to send structured information
         which the client code may want to work with
        """
        return self._body

    def with_msg(self, msg: str) -> "ErrorInfo":
        """
        Updates error message.

        :param msg: new message, up to 256 characters; will be truncated if the limit is exceeded
        :return: self, for call chaining sakes
        """
        self._msg = cast(str, _truncate_str_value(msg, _ERROR_INFO_MAX_MSG))

        return self

    def with_detail(self, detail: Optional[str] = None) -> "ErrorInfo":
        """
        Updates or resets the error detail.

        :param detail: detail to set; if None, the detail stored in the meta will be removed; default is None;
         detail can be up to 512 characters; will be truncated if the limit is exceeded
        :return: self, for call chaining sakes
        """
        self._detail = _truncate_str_value(detail, _ERROR_INFO_MAX_DETAIL)

        return self

    def with_body(self, body: Optional[Union[bytes, str]]) -> "ErrorInfo":
        """
        Updates or resets the error body.

        IMPORTANT: the ErrorInfo (and thus the contents of `body`) are passed out via FlightError.extra_info
        property. The Flight RPC implementations pass the `extra_info` via gRPC headers. In turn, the gRPC headers
        do have size limit. Keep this in mind when designing the value of `body`.

        If you set body that is too large, you will run into problems like this:
         https://github.com/grpc/grpc/issues/37852.

        :param body: body to set; if None, the body stored in the meta will be removed; default is None
        :return: self, for call chaining sakes
        """
        if isinstance(body, str):
            self._body = body.encode("utf-8")
        else:
            self._body = body

        return self

    def with_code(self, code: int = 0) -> "ErrorInfo":
        """
        Updates or resets the error code.

        Resetting error code means setting the code to 0 - the error code for unknown errors.

        :param code: code to set; default is 0
        :return: self, for call chaining sakes
        """
        self._code = code
        return self

    def to_bytes(self) -> bytes:
        """
        :return: binary representation of the meta; this can be sent over the wire (for instance in extra_info)
        """
        _json = {
            "msg": self._msg,
            "detail": self._detail,
            "code": self._code,
            "body": base64.b64encode(self._body).decode("ascii") if self._body else None,
        }

        return orjson.dumps(_json)

    def to_user_error(self) -> pyarrow.flight.FlightError:
        """
        Returns this error meta wrapped into a flight error that communicates failure due to bad user input.

        Since the Flight RPC does not have a dedicated user error, this method creates a FlightServerError.
        For a long time the code was creating FlightCancelledError - which somewhat fits (server cancels
        request because it is wrong) - it is saner to only use FlightCancelledError for the actual
        cancellation as it is described by Flight RPC itself.

        :return: this error meta wrapped into a Flight Error that communicates user error
        """
        return pyarrow.flight.FlightServerError(self.msg, extra_info=self.to_bytes())

    def to_server_error(self) -> pyarrow.flight.FlightServerError:
        """
        :return: this error meta wrapped into a FlightServerError
        """
        return pyarrow.flight.FlightServerError(self.msg, extra_info=self.to_bytes())

    def to_timeout_error(self) -> pyarrow.flight.FlightTimedOutError:
        """
        :return: this error meta wrapped into a FlightTimedOutError
        """
        return pyarrow.flight.FlightTimedOutError(self.msg, extra_info=self.to_bytes())

    def to_internal_error(self) -> pyarrow.flight.FlightInternalError:
        """
        :return: this error meta wrapped into a FlightInternalError
        """
        return pyarrow.flight.FlightInternalError(self.msg, extra_info=self.to_bytes())

    def to_cancelled_error(self) -> pyarrow.flight.FlightCancelledError:
        """
        :return: this error meta wrapped into a FlightCancelledError
        """
        return pyarrow.flight.FlightCancelledError(self.msg, extra_info=self.to_bytes())

    def to_unavailable_error(self) -> pyarrow.flight.FlightUnavailableError:
        """
        :return: this error meta wrapped into a FlightUnavailableError
        """
        return pyarrow.flight.FlightUnavailableError(self.msg, extra_info=self.to_bytes())

    def to_unauthenticated_error(
        self,
    ) -> pyarrow.flight.FlightUnauthenticatedError:
        """
        :return: this error meta wrapped into a FlightUnauthenticatedError
        """
        return pyarrow.flight.FlightUnauthenticatedError(self.msg, extra_info=self.to_bytes())

    def to_unauthorized_error(self) -> pyarrow.flight.FlightUnauthorizedError:
        """
        :return: this error meta wrapped into a FlightUnauthorizedError
        """
        return pyarrow.flight.FlightUnauthorizedError(self.msg, extra_info=self.to_bytes())

    def to_flight_error(
        self,
        error_factory: Callable[[str, Optional[bytes]], pyarrow.flight.FlightError],
    ) -> pyarrow.flight.FlightError:
        """
        Uses the provided error factory - which can be for example the FlightError subclass, to create an
        exception.

        :param error_factory: factory to create FlightError
        :return: new instance of error
        """
        return error_factory(self.msg, self.to_bytes())

    @staticmethod
    def from_bytes(val: bytes) -> "ErrorInfo":
        """
        Read error metadata from binary representation.

        :param val: binary representation
        :return: new error meta
        """
        try:
            _json = orjson.loads(val)
            body: Optional[bytes] = base64.b64decode(_json["body"]) if _json.get("body") is not None else None

            return ErrorInfo(
                msg=_json.get("msg"),
                detail=_json.get("detail"),
                body=body,
                code=_json.get("code"),
            )
        except Exception as e:
            raise ValueError(f"Unable to parser ErrorInfo from binary representation: '{str(e)}'.")

    @staticmethod
    def from_pyarrow_error(error: pyarrow.flight.FlightError) -> "ErrorInfo":
        """
        Reads ErrorInfo that is serialized inside the provided PyArrows FlightError (extra_info).
        If the extra error info is not included or is malformed, a placeholder with error code unknown will
        be returned.

        :param error: flight error
        :return: new instance
        """
        extra_info = error.extra_info

        if extra_info is None or not len(extra_info):
            return ErrorInfo(
                msg=f"Call failed with error that does not contain ErrorInfo. The error message was: {str(error)}"
            )

        try:
            return ErrorInfo.from_bytes(extra_info)
        except Exception:
            return ErrorInfo(
                msg=f"Call failed with error that does not contain ErrorInfo. The error message was: {str(error)}"
            )

    @staticmethod
    def maybe_from_pyarrow_error(
        error: pyarrow.flight.FlightError,
    ) -> Optional["ErrorInfo"]:
        """
        Reads ErrorInfo that may be serialized inside the provided PyArrow's FlightError (in extra_info).
        This method will return None if the error info is not present.

        :param error: flight error
        :return: new instance, None if the flight error info is not included
        """
        extra_info = error.extra_info

        if extra_info is None or not len(extra_info):
            # careful: when there is no extra info available, PyArrow will return
            # empty bytes. testing for both scenarios just in case
            return None

        try:
            return ErrorInfo.from_bytes(extra_info)
        except Exception:
            return None

    @staticmethod
    def for_exc(
        code: int,
        e: BaseException,
        extra_msg: Optional[str] = None,
        include_traceback: bool = True,
    ) -> "ErrorInfo":
        """
        A convenience factory which creates error meta as a response to some exception happening.

        The meta msg will be set to message included in the exception; this can be optionally augmented
        using extra_msg parameter. If extra_msg is present then:

        - if the message in the exception is empty, the extra msg will be used as-is
        - if the message in the exception is not empty, the extra msg will serve as prefix, or a lead in
          and the resulting msg in meta will be in format "extra_msg: exception_msg"

        Note: the above implies that it is better not to include trailing punctuation in the extra_msg.

        The traceback from the exception will be included automatically - unless you pass the include_traceback
        as False.

        :param code: error code
        :param e: exception that caused this whole unfortunate situation
        :param extra_msg: extra message to using during construction of error msg (see method docs for more info)
        :param include_traceback: whether to include exception traceback as the error detail; default is true
        :return: new error meta
        """
        msg = str(e)
        if not len(msg) and extra_msg is not None:
            msg = extra_msg + "."
        elif len(msg) and extra_msg is not None:
            msg = f"{extra_msg}: {msg}"

        if include_traceback:
            detail: Optional[str] = "".join(traceback.format_exception(None, e, e.__traceback__))
        else:
            detail = None

        return ErrorInfo(msg=msg, detail=detail, code=code)

    @staticmethod
    def for_reason(code: int, msg: str) -> "ErrorInfo":
        """
        A convenience factory which creates error meta that should be included in errors that fail
        request for some arbitrary reason. For example server does input validation and finds
        it incorrect.

        :param code: error code
        :param msg: error message, will be used as-is
        :return: new error meta
        """
        return ErrorInfo(msg=msg, code=code)

    @staticmethod
    def for_response(code: int, msg: str, body: bytes) -> "ErrorInfo":
        """
        A convenience factory which creates error meta that should be included in errors for which
        server wants to send some structured body to the client - so that client can inspect the body
        and act accordingly.

        For example client comes to get data with some ticket. The request times out and the server
        wants to tell the client to retry the DoGet later but with a different ticket.

        :param code: error code
        :param msg: error message, will be used as-is
        :param body: response body
        :return: new error meta
        """
        return ErrorInfo(msg=msg, body=body, code=code)

    @staticmethod
    def bad_argument(msg: str) -> pyarrow.flight.FlightError:
        """
        A convenience factory that creates a flight error as a response to bad input received from the user.

        :param msg: message to use as-is in the error
        :return: an instance of FlightError - ready to raise
        """
        return ErrorInfo(msg=msg, code=ErrorCode.BAD_ARGUMENT).to_user_error()

    @staticmethod
    def poll(
        flight_info: Optional[pyarrow.flight.FlightInfo] = None,
        retry_descriptor: Optional[pyarrow.flight.FlightDescriptor] = None,
        cancel_descriptor: Optional[pyarrow.flight.FlightDescriptor] = None,
    ) -> pyarrow.flight.FlightTimedOutError:
        """
        Convenience factory that creates FlightTimedOut error with POLL error code and `RetryInfo` which
        includes the provided values.

        :param flight_info: flight info available so far
        :param retry_descriptor: descriptor to use for retry
        :param cancel_descriptor: descriptor to use for cancellation
        :return: new flight error - ready to raise
        """
        retry_info = RetryInfo(
            flight_info=flight_info,
            retry_descriptor=retry_descriptor,
            cancel_descriptor=cancel_descriptor,
        )

        return ErrorInfo(
            msg="Work in progress. Retry.",
            code=ErrorCode.POLL,
            body=retry_info.to_bytes(),
        ).to_timeout_error()


class RetryInfo:
    """
    This message is included in the body of ErrorInfo when the GetFlightInfo fails with
    'POLL' error code.

    This happens for long-running commands which are submitted via GetFlightInfo
    and take arbitrary time to complete. Clients typically do not want to wait forever
    and instead poll on the status of the work

    It includes the information necessary for the client to either continue or cancel.
    """

    def __init__(
        self,
        flight_info: Optional[pyarrow.flight.FlightInfo] = None,
        retry_descriptor: Optional[pyarrow.flight.FlightDescriptor] = None,
        cancel_descriptor: Optional[pyarrow.flight.FlightDescriptor] = None,
    ) -> None:
        self._flight_info = flight_info
        self._retry_descriptor = retry_descriptor
        self._cancel_descriptor = cancel_descriptor

    @property
    def flight_info(self) -> Optional[pyarrow.flight.FlightInfo]:
        """
        FlightInfo available at the time of the poll timeout. The information
        may be incomplete. The full FlightInfo is built in cumulative fashion - the subsequent
        retries will add more information as it becomes available.

        Note: this is always full image of the FlightInfo available at the moment. It is
        not a delta containing just the new information available since the last call.

        :return: flight info
        """
        return self._flight_info

    @property
    def retry_descriptor(self) -> Optional[pyarrow.flight.FlightDescriptor]:
        """
        Returns descriptor that the client should use to retry the GetFlightInfo call
        in order to see whether the command has completed.

        Note: the retry descriptor will not be present if the command has completed.

        :return: flight descriptor if retry is possible
        """
        return self._retry_descriptor

    @property
    def cancel_descriptor(self) -> Optional[pyarrow.flight.FlightDescriptor]:
        """
        Returns descriptor that the client can use to cancel the command that is
        in progress.

        Note: the retry descriptor will not be present if the command is not cancellable.

        :return: flight descriptor if cancellation is possible
        """
        return self._cancel_descriptor

    def to_bytes(self) -> bytes:
        """
        :return: binary representation of the retry info
        """
        _json = {
            "flight_info": base64.b64encode(self._flight_info.serialize()).decode("ascii")
            if self._flight_info is not None
            else None,
            "retry_descriptor": base64.b64encode(self._retry_descriptor.serialize()).decode("ascii")
            if self._retry_descriptor is not None
            else None,
            "cancel_descriptor": base64.b64encode(self._cancel_descriptor.serialize()).decode("ascii")
            if self._cancel_descriptor is not None
            else None,
        }

        return orjson.dumps(_json)

    @staticmethod
    def from_bytes(val: bytes) -> "RetryInfo":
        """
        Reads the retry info from binary representation, as received in the error body.

        :param val: binary representation
        :return: new instance of retry info
        """
        _json = orjson.loads(val)
        try:
            flight_info = (
                pyarrow.flight.FlightDescriptor.deserialize(base64.b64decode(_json["flight_info"]))
                if _json.get("flight_info") is not None
                else None
            )
            retry_descriptor = (
                pyarrow.flight.FlightDescriptor.deserialize(base64.b64decode(_json["retry_descriptor"]))
                if _json.get("retry_descriptor") is not None
                else None
            )
            cancel_descriptor = (
                pyarrow.flight.FlightDescriptor.deserialize(base64.b64decode(_json["cancel_descriptor"]))
                if _json.get("cancel_descriptor") is not None
                else None
            )

            return RetryInfo(
                flight_info=flight_info,
                retry_descriptor=retry_descriptor,
                cancel_descriptor=cancel_descriptor,
            )
        except Exception as e:
            raise ValueError(f"Unable to decode retry info from binary representation: {str(e)}")
