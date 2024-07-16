# (C) 2024 GoodData Corporation
import ctypes
from typing import Any, Union


class NoLibc:
    @staticmethod
    def _noop(*args: Any, **kwargs: Any) -> None:
        return None

    def __getattr__(self, item: Any) -> Any:
        return NoLibc._noop


class LibcUtils:
    """
    Wrapper for calls of libc functions.
    """

    def __init__(self) -> None:
        # also see
        # https://stackoverflow.com/questions/67338017/does-calling-a-c-function-via-ctypes-in-python-release-the-gil-during-execution
        try:
            self._libc: Union[ctypes.CDLL, NoLibc] = ctypes.CDLL("libc.so.6")
        except OSError:
            self._libc = NoLibc()

    def malloc_trim(self) -> None:
        """
        Call malloc_trim - cutting away excess allocations that were not yet returned to the OS.

        See: https://issues.apache.org/jira/browse/ARROW-16697
        :return: nothing
        """
        self._libc.malloc_trim(0)
