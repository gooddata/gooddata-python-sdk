#  (C) 2024 GoodData Corporation
from typing import Any, Callable, Dict, List, Optional

import pyarrow.flight
import structlog
from typing_extensions import TypeAlias

_LOGGER = structlog.get_logger("gooddata_flight_server.rpc")


class CallInfo(pyarrow.flight.ServerMiddleware):
    """
    Call Info middleware holds information about the current call:

    - RPC method info
    - headers used on RPC Call
    """

    MiddlewareName = "call_info"

    def __init__(self, info: pyarrow.flight.CallInfo, headers: Dict[str, List[str]]):
        super().__init__()

        self._info = info
        self._headers = headers

    @property
    def info(self) -> pyarrow.flight.CallInfo:
        """
        :return: Flight's CallInfo with detail about the current call
        """
        return self._info

    @property
    def headers(self) -> Dict[str, List[str]]:
        """
        :return: headers provided by the caller
        """
        return self._headers


OnEndCallbackFn: TypeAlias = Callable[[Optional[pyarrow.ArrowException]], Any]


class CallFinalizer(pyarrow.flight.ServerMiddleware):
    """
    Call Finalizer middleware can be used by method implementations to register
    functions that should be called after the entire Flight RPC call finishes.

    This may be important especially for the DoGet and DoExchange methods where the
    method implementation prepares the stream and hands it over to PyArrow's Flight RPC.

    It is often the case that the stream is backed by data which has its lifecycle
    managed by the server. In these cases, the server needs to know the data is actually not
    used anymore (so that it can release locks, free up the data or do whatever it needs
    to do).
    """

    MiddlewareName = "call_finalizer"

    def __init__(self) -> None:
        super().__init__()

        self._on_end: List[OnEndCallbackFn] = []

    def register_on_end(self, fun: OnEndCallbackFn) -> None:
        """
        Register a function that should be called once the call completes. It is possible to call this
        multiple times and register multiple functions.

        IMPORTANT: the function that you register here should be quick, do minimal blocking and have low chance
        of hanging. The function will be called out from the gRPC server's thread; if the call hangs, server's thread
        will be blocked.

        :param fun: function to register, it will be called with one argument: exception,
         which is either None on success or pyarrow.ArrowException on failure
        :return: nothing
        """
        self._on_end.append(fun)

    def call_completed(self, exception: Optional[pyarrow.lib.ArrowException]) -> None:
        try:
            for fun in self._on_end:
                fun(exception)
        except Exception:
            _LOGGER.critical("call_finalization_failed", exc_info=True)
