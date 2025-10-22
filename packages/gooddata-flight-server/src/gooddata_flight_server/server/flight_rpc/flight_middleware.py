#  (C) 2024 GoodData Corporation
from typing import Any, Callable, Optional

import opentelemetry.context as otelctx
import opentelemetry.propagate as otelpropagate
import pyarrow.flight
import structlog
from opentelemetry import trace
from opentelemetry.semconv.trace import SpanAttributes
from opentelemetry.trace import SpanKind, StatusCode, use_span
from typing_extensions import TypeAlias

from gooddata_flight_server.utils.otel_tracing import SERVER_TRACER

_LOGGER = structlog.get_logger("gooddata_flight_server.rpc")


class CallInfo(pyarrow.flight.ServerMiddleware):
    """
    Call Info middleware holds information about the current call:

    - RPC method info
    - headers used on RPC Call
    """

    MiddlewareName = "call_info"

    def __init__(self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]):
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
    def headers(self) -> dict[str, list[str]]:
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

        self._on_end: list[OnEndCallbackFn] = []

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


class OtelMiddleware(pyarrow.flight.ServerMiddleware):
    MiddlewareName = "otel_middleware"

    def __init__(
        self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]], extract_context: bool = False
    ) -> None:
        super().__init__()
        method_name = info.method.name

        if extract_context:
            self._otel_ctx = otelpropagate.extract(headers)
        else:
            self._otel_ctx = otelctx.get_current()

        self._otel_span = SERVER_TRACER.start_span(
            f"{method_name}",
            kind=SpanKind.SERVER,
            context=self._otel_ctx,
            attributes={
                SpanAttributes.RPC_SYSTEM: "grpc",
                SpanAttributes.RPC_SERVICE: "FlightRPC",
                SpanAttributes.RPC_METHOD: method_name,
            },
        )

        # note: the code does not set context / use span at this point because
        # the middleware creation is done in a separate call, before the actual
        # method invocation.
        #
        # the context has to be set & span used during the actual Flight RPC
        # method handling

    @property
    def call_tracing(self) -> tuple[otelctx.Context, trace.Span]:
        """
        :return: tracing context & span for the current call
        """
        return self._otel_ctx, self._otel_span

    def call_completed(self, exception: Optional[pyarrow.lib.ArrowException]) -> None:
        # OpenTelemetry context/span restore;
        #
        # this has to happen because this method is done from thread managed
        # by gRPC server / Flight & during a separate call after the request handling
        # completes - any context juggling done previously is lost.
        #
        # - attach context extracted over the wire (see constructor)
        # - use current method call's span (created during middleware init)
        #
        # code can then complete the span accordingly and finally detach the context
        old_ctx = otelctx.attach(self._otel_ctx)
        try:
            with use_span(
                self._otel_span,
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            ):
                if exception is None:
                    self._otel_span.set_status(StatusCode.OK)
                else:
                    self._otel_span.set_status(StatusCode.ERROR)
                    self._otel_span.record_exception(exception)

                self._otel_span.end()
        finally:
            otelctx.detach(old_ctx)
