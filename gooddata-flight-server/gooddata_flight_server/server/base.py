#  (C) 2024 GoodData Corporation
from dataclasses import dataclass
from typing import Protocol

import pyarrow.flight
from dynaconf import Dynaconf

from gooddata_flight_server.config.config import ServerConfig
from gooddata_flight_server.health.server_health_monitor import (
    ServerHealthMonitor,
)
from gooddata_flight_server.server.flight_rpc.server_methods import (
    FlightServerMethods,
)
from gooddata_flight_server.tasks.task_executor import TaskExecutor


@dataclass(frozen=True)
class ServerContext:
    """
    Server's context.
    """

    settings: Dynaconf
    """
    All settings parsed from configuration files and/or environment variables provided at server startup.
    """

    config: ServerConfig
    """
    Server's configuration
    """

    location: pyarrow.flight.Location
    """
    Server's Flight RPC location - this location connectable by clients.
    """

    health: ServerHealthMonitor
    """
    Server's health monitor. Components may register their health into the monitor.

    This monitor is integrated with health check server where the overall status
    is reported using liveness/readiness endpoints.

    If a component is unhealthy, the whole server will be reported as such.
    """

    task_executor: TaskExecutor
    """
    Task Executor can and should be used to implement long running Tasks which generate
    Flight data.
    """


class FlightServerMethodsFactory(Protocol):
    """
    Factory function for server methods. This can be provided to the
    GoodDataFlightServer - the server will invoke the function at the right
    point and then integrate the FlightServerMethods into its Flight RPC service.
    """

    def __call__(self, ctx: ServerContext) -> FlightServerMethods: ...
