#  (C) 2024 GoodData Corporation
#
# mypy: no-strict-optional

from threading import Thread
from typing import Optional

import pyarrow.flight
import structlog

from gooddata_flight_server.config.config import AuthenticationMethod, ServerConfig
from gooddata_flight_server.errors.error_code import ErrorCode
from gooddata_flight_server.errors.error_info import ErrorInfo
from gooddata_flight_server.server.auth.auth_middleware import TokenAuthMiddleware, TokenAuthMiddlewareFactory
from gooddata_flight_server.server.auth.token_verifier_factory import create_token_verification_strategy
from gooddata_flight_server.server.base import ServerContext
from gooddata_flight_server.server.flight_rpc.flight_middleware import (
    CallFinalizer,
    CallInfo,
    OtelMiddleware,
)
from gooddata_flight_server.server.flight_rpc.flight_server import FlightServer
from gooddata_flight_server.server.flight_rpc.server_methods import (
    FlightServerMethods,
)


def _get_flight_server_locations(config: ServerConfig) -> tuple[str, str]:
    transport = "grpc+tls" if config.use_tls else "grpc"

    return (
        f"{transport}://{config.listen_host}:{config.listen_port}",
        f"{transport}://{config.advertise_host}:{config.advertise_port}",
    )


class _AvailabilityMiddlewareFactory(pyarrow.flight.ServerMiddlewareFactory):
    """
    Optionally rejects calls with FlightUnavailableError & some reason.

    If unavailable_reason is set -> reject. Otherwise, let the request through.
    """

    def __init__(self, unavailable_reason: Optional[ErrorInfo] = None):
        super().__init__()

        self.unavailable_reason: Optional[ErrorInfo] = unavailable_reason

    def start_call(
        self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]
    ) -> Optional[pyarrow.flight.ServerMiddleware]:
        if self.unavailable_reason is None:
            return None

        raise self.unavailable_reason.to_unavailable_error()


class _CallInfoMiddlewareFactory(pyarrow.flight.ServerMiddlewareFactory):
    def start_call(
        self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]
    ) -> Optional[pyarrow.flight.ServerMiddleware]:
        return CallInfo(info, headers)


class _CallFinalizerMiddlewareFactory(pyarrow.flight.ServerMiddlewareFactory):
    def start_call(
        self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]
    ) -> Optional[pyarrow.flight.ServerMiddleware]:
        return CallFinalizer()


class _OtelMiddlewareFactory(pyarrow.flight.ServerMiddlewareFactory):
    def __init__(self, extract_context: bool) -> None:
        super().__init__()
        self._extract_context = extract_context

    def start_call(
        self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]
    ) -> Optional[pyarrow.flight.ServerMiddleware]:
        return OtelMiddleware(info, headers, self._extract_context)


class FlightRpcService:
    """
    Service that exposes Flight RPC.

    Handles Flight server start/stop & importantly also allows switching running server from
    available to unavailable state; typical use case is to reject any RPC during startup/shutdown
    of the server or loss of connection to the cluster.
    """

    def __init__(
        self,
        config: ServerConfig,
        methods: FlightServerMethods = FlightServerMethods(),
    ):
        self._config = config
        self._methods = methods

        (
            self._listen_url,
            self._client_url,
        ) = _get_flight_server_locations(config=config)

        self._logger = structlog.get_logger("gooddata_flight_server.rpc")

        self._availability = _AvailabilityMiddlewareFactory(
            unavailable_reason=ErrorInfo.for_reason(ErrorCode.NOT_READY, "Try again later.")
        )
        # internal mutable state
        # server starts immediately when constructed (PyArrow stuff); thus defer
        # construction until start() is called
        self._server: Optional[FlightServer] = None
        self._flight_shutdown_thread: Optional[Thread] = None
        self._stopped = False

    def _initialize_authentication(
        self, ctx: ServerContext
    ) -> Optional[tuple[str, pyarrow.flight.ServerMiddlewareFactory]]:
        if self._config.authentication_method == AuthenticationMethod.NoAuth:
            if self._config.use_mutual_tls:
                return None

            if "127.0.0.1" not in self._config.listen_host and "localhost" not in self._config.listen_host:
                print("!" * 72)
                print("!!! Your server is configured without authentication and ")
                print("!!! it seems it is listening on a non-loopback interface. ")
                print("!!! The server may be reachable from public network. ")
                print(f"!!! Listening on: {self._config.listen_host}. ")
                print("!" * 72)

                self._logger.warning("insecure_warning", listen_url=self._config.listen_host)

            return None

        verification = create_token_verification_strategy(ctx)

        return TokenAuthMiddleware.MiddlewareName, TokenAuthMiddlewareFactory(
            ctx.config.token_header_name, verification
        )

    def _initialize_otel_tracing(
        self, ctx: ServerContext
    ) -> Optional[tuple[str, pyarrow.flight.ServerMiddlewareFactory]]:
        if self._config.otel_config.exporter_type is None:
            return None

        return OtelMiddleware.MiddlewareName, _OtelMiddlewareFactory(
            self._config.otel_config.extract_context_from_headers
        )

    def start(self, ctx: ServerContext) -> None:
        """
        Starts the server. This will start the Flight RPC Server bound to configured host and port.
        The server will be returning UNAVAILABLE for all methods until it is switched to serving.

        See `switch_to_serving`.

        :return:  nothing
        """
        # massaging before sending these out to PyArrow
        tls_certificates = (
            [self._config.tls_cert_and_key]
            if self._config.use_tls and self._config.tls_cert_and_key is not None
            else None
        )

        self._logger.info(
            "flight_service_start",
            listen_url=self._listen_url,
            client_url=self._client_url,
            tls=tls_certificates is not None,
        )

        middleware = {
            "_availability": self._availability,
            CallInfo.MiddlewareName: _CallInfoMiddlewareFactory(),
            CallFinalizer.MiddlewareName: _CallFinalizerMiddlewareFactory(),
        }

        auth_middleware = self._initialize_authentication(ctx)
        if auth_middleware is not None:
            middleware[auth_middleware[0]] = auth_middleware[1]

        otel_middleware = self._initialize_otel_tracing(ctx)
        if otel_middleware is not None:
            middleware[otel_middleware[0]] = otel_middleware[1]

        # server starts right as it is constructed
        # the serve() method does not have to be called; moreover, it should not be called by the server
        # as it makes PyArrow to install signal handlers that interfere with quiver server's handlers
        #
        # see: https://github.com/apache/arrow/issues/11932
        self._server = FlightServer(
            methods=self._methods,
            location=self._listen_url,
            tls_certificates=tls_certificates,
            verify_client=self._config.use_mutual_tls,
            root_certificates=self._config.tls_root_cert,
            middleware=middleware,
        )

    def switch_to_serving(self, methods: FlightServerMethods) -> None:
        """
        Switches the Flight RPC server to serving mode.

        :param methods: implementation of the Flight RPC methods
        :return: nothing
        """
        if self._server is None:
            raise AssertionError("Flight server was never started")

        self._methods = methods
        self._server.switch_methods(methods)
        self._availability.unavailable_reason = None

    def switch_to_unavailable(self, err: ErrorInfo) -> None:
        """
        Switches the Flight RPC server to unavailable mode. All new Flight RPC method
        calls will be returning UNAVAILABLE from now on.

        :param err: error info to include in the FlightUnavailableError
        :return: nothing
        """
        if self._server is None:
            raise AssertionError("Flight server was not started")

        self._availability.unavailable_reason = err

    def stop(self) -> None:
        """
        Stops service. This method will switch the Flight RPC server to return
        'UNAVAILABLE' for all following calls and then initiates shutdown of the server.

        The shutdown is done asynchronously. Use `wait_for_stop` to sync for completion.
        Since the server shutdown will wait until existing clients finish it may take longer.

        :return:
        """
        if self._server is None:
            raise AssertionError("Flight server was never started")

        if self._flight_shutdown_thread is not None:
            return

        # do not handle any more new requests
        self.switch_to_unavailable(ErrorInfo.for_reason(ErrorCode.SHUTTING_DOWN, "Server is shutting down."))

        # trigger server shutdown in separate thread because shutdown blocks and violates the contract
        # for quiver's long-running services
        self._flight_shutdown_thread = Thread(
            name="flight_service_shutdown",
            daemon=True,
            target=self._shutdown_server,
        )
        self._flight_shutdown_thread.start()

    def _shutdown_server(self) -> None:
        self._logger.info("flight_service_shutdown")
        # this will block until server stops
        self._server.shutdown()
        self._logger.info("flight_service_finished")

    def wait_for_stop(self, timeout: Optional[float] = None) -> bool:
        if self._flight_shutdown_thread is None:
            # this is really some mess in the caller code.. did not call stop() but tries to wait for it..
            raise AssertionError("Flight server stop() was not issued yet attempting to wait for the server to stop.")

        if self._flight_shutdown_thread.is_alive():
            self._flight_shutdown_thread.join(timeout=timeout)

        return not self._flight_shutdown_thread.is_alive()

    @property
    def client_url(self) -> str:
        """
        :return: location URL to advertise to clients
        """
        return self._client_url
