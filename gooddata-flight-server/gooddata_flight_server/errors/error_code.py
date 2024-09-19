#  (C) 2024 GoodData Corporation
from typing import Any, Literal, Optional

from typing_extensions import TypeAlias

_CUSTOM_ERROR_START = 1000
_ERROR_CODE_MASK = 0x0000_FFFF
_ERROR_FLAGS_MASK = 0xFFFF_0000

_RETRY_HERE_FLAG = 0x0001_0000
"""
Request that failed should be retried on the same node where the call failed
"""

_RETRY_OTHER_FLAG = 0x0002_0000
"""
Request that failed should be retried on other applicable nodes.
"""

_RETRY_ANY_FLAG = 0x0003_0000
"""
Request that failed can be retried either on this node or any other applicable node.
"""


def _init_names(cls: Any) -> Any:
    cls._init_names()
    return cls


_RetryFlagsLiteral: TypeAlias = Literal["any", "other", "here"]
_FlagsMapping: dict[_RetryFlagsLiteral, int] = {
    "any": _RETRY_ANY_FLAG,
    "here": _RETRY_HERE_FLAG,
    "other": _RETRY_OTHER_FLAG,
}


def _get_flags(retry: Optional[_RetryFlagsLiteral] = None) -> int:
    if retry is None:
        return 0x0
    return _FlagsMapping.get(retry, 0x0)


def _error_code(code: int, retry: Optional[_RetryFlagsLiteral] = None) -> int:
    return _get_flags(retry) | code


# TODO: revisit codes
@_init_names
class ErrorCode:
    """
    Error codes for different failures that may occur while servicing requests.
    """

    UNKNOWN = 0
    """
    Unknown error. Probably something very bad happened on the server. The message and detail of the error should
    contain diagnostic information.
    """

    BAD_ARGUMENT = _error_code(1)
    """
    User error: input received from the client failed server-side validations.
    """

    BAD_REQUEST = _error_code(2)
    """
    User error: client sent request to a node that just does not know how to deal with it at all.
    """

    UNSUPPORTED_SERVICE = _error_code(3)
    """
    User error: client wants to generate data using a service that is not running on the contacted server.
    """

    INVALID_TICKET = _error_code(4)
    """
    User error: client wants to get data using an invalid ticket.
    """

    COMMAND_FAILED = _error_code(5)
    """
    Service run into an error while performing the command.
    """

    COMMAND_CANCELLED = _error_code(6)
    """
    Command was cancelled by the user.
    """

    COMMAND_CANCEL_NOT_POSSIBLE = _error_code(7)
    """
    User wanted to cancel the command but it was not possible - probably because the
    command already finished or is at a stage where it cannot be cancelled.
    """

    COMMAND_RESULT_CONSUMED = _error_code(8)
    """
    User wanted to cancel the command but it was not possible - probably because the
    command already finished or is at a stage where it cannot be cancelled.
    """

    TIMEOUT = _error_code(100)
    """
    Request has timed out.
    """

    POLL = _error_code(101, retry="here")
    """
    Request has timed out but can be retried on the same node using the contents of RetryInfo,
    which are serialized and stored in the error body.
    """

    BACKPRESSURE = _error_code(102, retry="any")
    """
    Server dropped the request as it is currently in state where it must exert backpressure.
    """

    INTERNAL_ERROR = _error_code(500, retry="other")
    """
    Internal server error.
    """

    NOT_READY = _error_code(501, retry="any")
    """
    Server is not yet ready to serve requests.
    """

    SHUTTING_DOWN = _error_code(502, retry="other")
    """
    Server is shutting down.
    """

    NOT_IMPLEMENTED = _error_code(503)
    """
    Functionality not implemented
    """

    @classmethod
    def name(cls, code: int) -> str:
        """
        Gets error name for the provided code. This may be used for debug purposes or when printing
        somewhat more meaningful error messages to the end users.

        :param code: error code
        :return: error name
        """
        if code < 0:
            return f"unknown ({code})"

        status = code & _ERROR_CODE_MASK
        res = cls._GENERATED_NAMES.get(status, "unknown")  # type: ignore

        if status >= _CUSTOM_ERROR_START:
            res = "custom"

        return f"{res} ({status})"

    @classmethod
    def is_retry_here(cls, code: int) -> bool:
        """
        :param code: error code
        :return: true if the request can be retried either on the node where it originally failed
         or on any other applicable node
        """
        return code & _RETRY_HERE_FLAG == _RETRY_HERE_FLAG

    @classmethod
    def is_retry_other(cls, code: int) -> bool:
        """
        :param code: error code
        :return: true if the request can be retried, but only on other nodes - e.g. not on the same
         node where it just failed
        """
        return code & _RETRY_OTHER_FLAG == _RETRY_OTHER_FLAG

    @classmethod
    def is_retry_any(cls, code: int) -> bool:
        """
        :param code: error code
        :return: true if the request can be retried on any node; both the original node where the
         call failed and the other applicable are valid candidates
        """
        return code & _RETRY_ANY_FLAG == _RETRY_ANY_FLAG

    @classmethod
    def is_retryable(cls, code: int) -> bool:
        """
        :param code: error code
        :return: true if the request can be retried - either on the node where it originally failed
         or on other applicable nodes
        """
        return code & _RETRY_ANY_FLAG > 0

    @classmethod
    def _init_names(cls) -> None:
        names = {}
        codes = {}

        for key in dir(cls):
            value = getattr(cls, key)
            if isinstance(value, int) and not key.startswith("_"):
                status = value & _ERROR_CODE_MASK
                names[status] = key.lower()
                codes[key] = value

        setattr(cls, "_GENERATED_NAMES", names)
        setattr(cls, "_CODE_MAPPING", codes)
