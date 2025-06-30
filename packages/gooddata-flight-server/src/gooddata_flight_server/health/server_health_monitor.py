# (C) 2024 GoodData Corporation
import enum
import threading
import time

import structlog

from gooddata_flight_server.metrics import ServerMetrics
from gooddata_flight_server.utils.libc_utils import LibcUtils


class ModuleHealthStatus(enum.Enum):
    """
    This enum lists health status of a module
    """

    OK = "ok"
    NOT_OK = "not_ok"


class ServerHealthMonitor:
    """
    Server health monitor and maintenance.

    The monitor includes a thread doing regular maintenance - namely periodically performing
    malloc trim() to make system throw away the garbage. This is essential to survive in runtime environments
    that impose memory (RSS) limits and kill the server if it exceeds it - the malloc does not
    free the used memory back to the system; the RSS keeps growing and growing until the server
    gets killed. The trim() call makes malloc drop all unneeded allocations.
    """

    def __init__(
        self,
        trim_interval: int = 30,
    ) -> None:
        self._logger = structlog.get_logger("gooddata_flight_server.maintenance")
        self._libc = LibcUtils()
        self._trim_interval = trim_interval
        self._module_statuses: dict[str, ModuleHealthStatus] = {}

        self._thread = threading.Thread(
            name="gooddata_flight_server.maintenance",
            target=self._maintenance,
            daemon=True,
        )
        self._thread.start()

        self._logger.info("server_health_monitor_started")

    def _maintenance(self) -> None:
        last_trim = time.time()

        while True:
            if time.time() - last_trim > self._trim_interval:
                try:
                    trim_start = time.perf_counter()
                    self._libc.malloc_trim()
                    duration = time.perf_counter() - trim_start

                    ServerMetrics.TRIM_SUMMARY.observe(duration)
                    self._logger.debug(
                        "server_maintenance",
                        op="malloc_trim",
                        duration=duration,
                    )
                except Exception:
                    ServerMetrics.TRIM_ERROR_COUNT.inc()
                    self._logger.error("malloc_trim_failed", exc_info=True)

                last_trim = time.time()

            time.sleep(1.0)

    @property
    def module_statuses(self) -> dict[str, ModuleHealthStatus]:
        return self._module_statuses

    def set_module_status(self, name: str, status: ModuleHealthStatus) -> None:
        """
        :param name: name of the module to which the status belongs
        :param status: health status of the module
        """
        self._module_statuses[name] = status
