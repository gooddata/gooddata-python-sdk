# (C) 2022 GoodData Corporation
import platform
import signal
from abc import abstractmethod
from threading import Condition, Thread
from typing import Any, Optional

import pyarrow
import structlog
from prometheus_client import start_http_server

from gooddata_flight_server._version import __version__
from gooddata_flight_server.config.config import ServerConfig
from gooddata_flight_server.health.health_check_http_server import HealthCheckHttpServer
from gooddata_flight_server.health.server_health_monitor import ServerHealthMonitor
from gooddata_flight_server.utils.otel_tracing import SERVER_TRACER

# DEV ONLY - heap usage debugger
#
# uncomment to turn on, then uncomment the dump done at the time of server stop()
# from guppy import hpy
# h = hpy()


class ServerStartupInterrupted(Exception):
    """
    This exception is thrown when server startup was interrupted due to unrecoverable condition. Different init and
    preparation logic may raise this to stop the server startup. The message included in the exception will be
    printed to stderr and server stops with exit code 1.
    """


class GoodDataFlightServer:
    def __init__(
        self,
        config: ServerConfig,
    ):
        self._logger = structlog.get_logger("gooddata_flight_server.server")
        self._config = config
        self._health = ServerHealthMonitor(
            trim_interval=config.malloc_trim_interval_sec,
        )

        # main server thread; this is responsible for starting all sub-services,
        # don't want the main thread to be blocked
        self._main_thread = Thread(name="gooddata_flight_server.server", target=self._server_main, daemon=True)

        # main server waits for this condition, once notified, it will stop or abort all sub-services
        self._stop_cond = Condition()
        # main server notifies on this condition once all sub-services are started
        self._start_cond = Condition()
        self._startup_interrupted: Optional[Exception] = None
        self._stop = False
        self._abort = False

    #
    # Server template
    #

    def _sig_handler(self, sig: Any, frame: Any) -> None:
        self._logger.info("server_shutdown_initiated")
        self.stop()

    def _health_check_http_server_start(self) -> None:
        """
        If configured, start health checks HTTP server.

        :return: nothing
        """
        if self._config.health_check_host is not None:
            HealthCheckHttpServer(
                host=self._config.health_check_host,
                port=self._config.health_check_port,
                server_health_monitor=self._health,
            )

    def _metrics_server_start(self) -> None:
        """
        If configured, start Prometheus metric server.

        :return: nothing
        """
        if self._config.metrics_host is not None:
            start_http_server(
                port=self._config.metrics_port,
                addr=self._config.metrics_host,
            )

    def _server_main(self) -> None:
        self._logger.info(
            "server_startup",
            platform=platform.platform(terse=True),
            python_version=platform.python_version(),
            arrow_version=pyarrow.__version__,
            server_version=__version__,
        )

        try:
            self._pre_startup()
        except Exception as e:
            self._startup_interrupted = e
            return

        with self._stop_cond:
            if self._stop:
                return

        try:
            self._metrics_server_start()
            self._health_check_http_server_start()
            self._startup_services()

            # event handler to start event processing and then start cluster connection's
            # event stream. this way, if cluster connection emits large number of events (for
            # example describing existing flights), those events will not be accumulated
            with self._start_cond:
                self._start_cond.notify_all()

            self._finalize_startup()

            with self._stop_cond:
                while not self._stop:
                    self._start_cond.wait()

            if not self._abort:
                self._shutdown_services()
            else:
                self._abort_services()
        except Exception as e:
            self._startup_interrupted = e
            return
        finally:
            self._logger.info("server_main_finished")

    #
    # Context
    #

    @property
    def logger(self) -> structlog.stdlib.BoundLogger:
        """
        :return: server's main logger
        """
        return self._logger

    @property
    def health(self) -> ServerHealthMonitor:
        """
        :return: server's health monitor, this is initialized from the very beginning of the server's life
        """
        return self._health

    #
    # Lifecycle
    #
    @SERVER_TRACER.start_as_current_span("server_start")
    def start(self) -> None:
        """
        Starts the server. This spins of the main server thread where it all happens. The start() method
        returns immediately.

        :return: nothing
        """
        signal.signal(signal.SIGINT, self._sig_handler)
        signal.signal(signal.SIGTERM, self._sig_handler)

        self._main_thread.start()

    def stop(self) -> None:
        """
        Gracefully stops the server. This method will not block; see wait_for_stop().

        :return: nothing
        """
        # DEV ONLY - heap usage debugger; also uncomment the imports
        # print(h.heap())

        with self._stop_cond:
            self._stop = True
            self._stop_cond.notify_all()

    def abort(self) -> None:
        """
        Triggers hard-stop of the server. This is typically done as a response to unrecoverable failure that
        warrants for quick and dirty shutdown.

        On hard stop, the server will only try to do bare minimum - stop any new requests & then unregister itself
        from the cluster.

        :return:
        """
        with self._stop_cond:
            self._abort = True
            self._stop = True
            self._stop_cond.notify_all()

    def aborted(self) -> bool:
        """
        :return: True if the server aborted due to some serious failure
        """
        return self._abort

    def wait_for_stop(self, timeout: Optional[float] = None) -> bool:
        """
        Waits until the main server thread stops. If the server startup encountered error (and never started), then
        that error will be raised.

        :param timeout: time to wait
        :return: True if the main server thread finished; false if it is still running
        """
        self._main_thread.join(timeout=timeout)

        if self._startup_interrupted is not None:
            self._logger.fatal("server_startup_interrupted", exc_info=self._startup_interrupted)

            raise self._startup_interrupted

        return not self._main_thread.is_alive()

    #
    # template methods to be implemented by subclasses
    #

    def _pre_startup(self) -> None:
        """
        Perform any work before the actual startup logic is initiated. This may gracefully interrupt the server
        startup if you raise exception created using the `_make_interrupt_exc()` method.

        :return: optionally return cluster connection options to use; if None is returned, then the default
         options will be used
        """

    @abstractmethod
    def _startup_services(self) -> None:
        """
        Create and start up any services that the concrete server type requires. Unless you implement the
        `_finalize_startup()` method, the server should be running and ready to serve clients at this point.

        If this method raises an exception, then the server start will be interrupted and the server will exit.
        You may gracefully interrupt the server startup if you raise exception created using the `make_interrupt_exc()`
        method.

        This method is called _after_ the cluster connection is successfully initialized and established.

        After this method completes successfully, the server will start processing events as they arrive via the
        cluster connection. It is thus essential that all your custom services that are interested in the events are
        registered as event processors or add event handlers.

        :return: nothing
        """
        raise NotImplementedError

    def _finalize_startup(self) -> None:
        """
        Perform any work to finalize server's startup. This method will be called _after_ the server processes
        all events that describe the state of the cluster at the time it connected.

        There are several cases when you may want to implement this method:

        - some of your services need to synchronize with cluster events during their startup. The server's event loop
          is started after a successful call to `_startup_services()`. So during the startup services you typically
          create the event-based services and register them with the server - this ensures the server's event loop (
          separate thread) is pushing events to them. Then, in this method you actually start the service and wait
          for its successful startup.

        - you want to hold off the time when server starts serving the clients until all sub-services are successfully
          started

        Example that covers both of the above: server that uses Quiver's storage service wants to hold off serving
        the clients until storage service is fully initialized. During storage service initialization, the service
        uses cluster events to boot up storage classes and most importantly, connect the network attached durable
        storages. Server should wait until all durable storage is initialized before accepting any client requests.

        :return: Nothing
        """

    @abstractmethod
    def _shutdown_services(self) -> None:
        """
        Gracefully shutdown any services that the concrete server type uses. This method should block until all
        the necessary services are stopped.

        :return: nothing
        """
        raise NotImplementedError

    @abstractmethod
    def _abort_services(self) -> None:
        """
        Abort services. This method is called on unrecoverable errors when server just needs to shut down as soon
        as possible. During abort, the server should try and do most important sanity (if any) and exit asap. Attempting
        more complex operations that require communication with the cluster is not a good idea because the
        cluster connection may be defunct.

        :return: nothing
        """
        raise NotImplementedError
