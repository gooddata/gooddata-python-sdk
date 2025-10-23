# (C) 2024 GoodData Corporation
from functools import partial
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from typing import Any

import structlog

from gooddata_flight_server.health.server_health_monitor import (
    ModuleHealthStatus,
    ServerHealthMonitor,
)

LIVENESS_ENDPOINT_PATH = "/live"
READINESS_ENDPOINT_PATH = "/ready"

SERVER_MODULE_DEBUG_NAME = "server"

LOGGER = structlog.get_logger("gooddata_flight_server.health_check_http_server")


class _HealthCheckHandler(BaseHTTPRequestHandler):
    def __init__(
        self,
        *args: Any,
        server_health_monitor: ServerHealthMonitor,
        **kwargs: Any,
    ):
        self._server_health_monitor = server_health_monitor
        super().__init__(*args, **kwargs)

    def log_message(self, format: str, *args: list) -> None:
        pass

    def do_GET(self) -> None:  # noqa: N802
        if self.path == READINESS_ENDPOINT_PATH:
            self.send_response(HTTPStatus.NO_CONTENT if self.is_ready() else HTTPStatus.INTERNAL_SERVER_ERROR)
        elif self.path == LIVENESS_ENDPOINT_PATH:
            self.send_response(HTTPStatus.NO_CONTENT if self.is_alive() else HTTPStatus.INTERNAL_SERVER_ERROR)
        else:
            self.send_response(HTTPStatus.NOT_FOUND)
        self.end_headers()

    def is_ready(self) -> bool:
        """
        Readiness check inspecting flight server startup state.

        :return: True if instance is ready otherwise False
        """
        LOGGER.debug("checking_flight_server_ready")
        if (
            SERVER_MODULE_DEBUG_NAME in self._server_health_monitor.module_statuses
            and self._server_health_monitor.module_statuses[SERVER_MODULE_DEBUG_NAME] == ModuleHealthStatus.OK
        ):
            LOGGER.debug("flight_server_ready")
            return True
        else:
            LOGGER.warning("flight_server_not_ready")
            return False

    def is_alive(self) -> bool:
        """
        Liveness check inspecting all running modules statuses.

        :return: True if server is healthy otherwise False
        """
        LOGGER.debug("checking_flight_server_healthy")

        for (
            module,
            status,
        ) in self._server_health_monitor.module_statuses.items():
            if status == ModuleHealthStatus.NOT_OK:
                LOGGER.warning("unhealthy_module", module=module)
                return False

        LOGGER.debug("flight_server_healthy")
        return True


class HealthCheckHttpServer:
    """
    HTTP server implementation for health checks mainly usable in k8s environment for readiness
    and liveness probes. Exposes $LIVENESS_ENDPOINT_PATH and $READINESS_ENDPOINT_PATH returning HTTP 200 in
    case of success otherwise HTTP 500.
    """

    def __init__(
        self,
        host: str,
        port: int,
        server_health_monitor: ServerHealthMonitor,
    ):
        handler = partial(_HealthCheckHandler, server_health_monitor=server_health_monitor)
        httpd = HTTPServer((host, port), handler)

        def serve_forever(httpd_instance: HTTPServer) -> None:
            with httpd_instance:
                LOGGER.info("health_check_started", host=host, port=port)
                httpd_instance.serve_forever()

        Thread(target=serve_forever, args=(httpd,), daemon=True).start()
