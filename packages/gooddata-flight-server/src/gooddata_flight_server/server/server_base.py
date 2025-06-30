# (C) 2024 GoodData Corporation
import abc
import os
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
from gooddata_flight_server.health.health_check_http_server import (
    SERVER_MODULE_DEBUG_NAME,
    HealthCheckHttpServer,
)
from gooddata_flight_server.health.server_health_monitor import (
    ModuleHealthStatus,
    ServerHealthMonitor,
)
from gooddata_flight_server.utils.otel_tracing import SERVER_TRACER

# DEV ONLY - heap usage debugger
#
# uncomment to turn on, then uncomment the dump done at the time of server stop()
# from guppy import hpy
# h = hpy()

DEFAULT_LOGGING_INI = os.path.join(os.path.dirname(__file__), "default.logging.ini")


class ServerBase(abc.ABC):
    """
    Server base class. Template class which takes care of the infrastructure and other boring
    stuff and lets subclasses focus on just the value added services.
    """

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
        self._main_thread = Thread(
            name="gooddata_flight_server.server",
            target=self._server_main,
            daemon=True,
        )

        # main server waits for this condition, once notified, it will stop or abort all sub-services
        self._stop_cond = Condition()
        # main server notifies on this condition once all sub-services are started
        self._start_cond = Condition()
        self._started = False
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
            self._logger.debug(
                "health_check_starting",
                host=self._config.health_check_host,
                port=self._config.health_check_port,
            )

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
            self._logger.debug(
                "metrics_starting",
                host=self._config.metrics_host,
                port=self._config.metrics_port,
            )

            start_http_server(
                addr=self._config.metrics_host,
                port=self._config.metrics_port,
            )

            self._logger.info(
                "metrics_started",
                host=self._config.metrics_host,
                port=self._config.metrics_port,
            )

    def _server_main(self) -> None:
        self._logger.info(
            "server_startup",
            platform=platform.platform(terse=True),
            python_version=platform.python_version(),
            arrow_version=pyarrow.__version__,
            server_version=__version__,
            config=self._config.without_tls(),
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
            self._health.set_module_status(SERVER_MODULE_DEBUG_NAME, ModuleHealthStatus.OK)

            with self._start_cond:
                self._started = True
                self._start_cond.notify_all()

            with self._stop_cond:
                while not self._stop:
                    self._stop_cond.wait()

            if not self._abort:
                self._shutdown_services()
            else:
                self._abort_services()
        except Exception as e:
            self._startup_interrupted = e

            # wake up anyone who may be waiting for the server to start
            with self._start_cond:
                self._start_cond.notify_all()

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

        On hard stop, the server will only try to do bare minimum in an attempt to clean up bare essentials.

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

    def wait_for_start(self, timeout: Optional[float] = None) -> bool:
        """
        Waits until server and all its services are up and running.

        :param timeout: time in fractions of seconds
        :return: true if started, false if not
        """
        with self._start_cond:
            completed = self._start_cond.wait_for(
                lambda: self._started is True or self._startup_interrupted is not None,
                timeout=timeout,
            )
            if not completed:
                return False

            if self._startup_interrupted is not None:
                raise self._startup_interrupted

            return True

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

        :return: nothing
        """

    @abstractmethod
    def _startup_services(self) -> None:
        """
        Create and start up any services that the concrete server type requires. After the method completes,
        the server should be up and running, ready to serve clients.

        If this method raises an exception, then the server start will be interrupted and the server will exit.
        You may gracefully interrupt the server startup if you raise exception created using the `make_interrupt_exc()`
        method.

        :return: nothing
        """
        raise NotImplementedError

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
        Abort services.

        This method is called on unrecoverable errors when server just needs to shut down as soon as possible.
        During abort, the server should try and do most important sanity (if any) and exit asap.

        Attempting more complex and possibly blocking operations is not a good idea.

        :return: nothing
        """
        raise NotImplementedError
