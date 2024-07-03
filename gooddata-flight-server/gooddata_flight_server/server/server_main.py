#  (C) 2024 GoodData Corporation
from typing import Optional, Union

import pyarrow.flight
from dynaconf import Dynaconf

from gooddata_flight_server.config.config import ServerConfig, read_config
from gooddata_flight_server.server.flight_rpc.flight_service import FlightRpcService
from gooddata_flight_server.server.flight_rpc.server_methods import FlightServerMethods
from gooddata_flight_server.server.method_factory import FlightServerMethodsFactory, ServerContext
from gooddata_flight_server.server.server_base import DEFAULT_LOGGING_INI, ServerBase
from gooddata_flight_server.tasks.task_executor import TaskExecutor
from gooddata_flight_server.tasks.thread_task_executor import ThreadTaskExecutor
from gooddata_flight_server.utils.logging import init_logging
from gooddata_flight_server.utils.otel_tracing import initialize_otel_tracing


class GoodDataFlightServer(ServerBase):
    def __init__(
        self, settings: Dynaconf, config: ServerConfig, methods: Union[FlightServerMethods, FlightServerMethodsFactory]
    ):
        super().__init__(config)

        self._settings = settings
        self._methods = methods if isinstance(methods, FlightServerMethods) else None
        self._methods_factory = methods if isinstance(methods, FlightServerMethodsFactory) else None

        self._flight_service = FlightRpcService(config=config, methods=methods)
        self._location = pyarrow.flight.Location(self._flight_service.client_url)

        # TODO: make metric prefix configurable
        self._task_executor = ThreadTaskExecutor(
            metric_prefix="gdfs",
            task_threads=config.task_threads,
            result_close_threads=config.task_close_threads,
            keep_results_for=config.task_result_ttl_sec,
        )

    @property
    def location(self) -> pyarrow.flight.Location:
        """
        Server's location - this should be sent in all infos returned via Flight RPC.

        :return: location
        """
        return self._location

    @property
    def task_executor(self) -> TaskExecutor:
        """

        :return:
        """
        return self._task_executor

    def _startup_services(self) -> None:
        self._flight_service.start()

        if self._methods_factory is not None:
            self._methods = self._methods_factory.create_methods(
                ServerContext(
                    settings=self._settings,
                    config=self._config,
                    location=self._location,
                )
            )

        assert self._methods is not None
        self._flight_service.switch_to_serving(self._methods)

    def _shutdown_services(self) -> None:
        self._flight_service.stop()
        self._flight_service.wait_for_stop()

    def _abort_services(self) -> None:
        self._flight_service.stop()


def create_server(
    methods: Optional[Union[FlightServerMethods, FlightServerMethodsFactory]] = None,
    config_files: tuple[str, ...] = (),
    logging_config: Optional[str] = DEFAULT_LOGGING_INI,
    dev_log: bool = True,
) -> "GoodDataFlightServer":
    settings, config = read_config(files=config_files)

    init_logging(
        logging_config,
        dev_log=dev_log,
        event_key=config.log_event_key_name,
        trace_ctx_keys=config.log_trace_keys,
        add_trace_ctx=config.otel_config.exporter_type is not None,
    )

    initialize_otel_tracing(config=config.otel_config)
    # TODO: by default use the factory that supports pluggable functions
    _methods = methods or FlightServerMethods()

    return GoodDataFlightServer(settings=settings, config=config, methods=_methods)
