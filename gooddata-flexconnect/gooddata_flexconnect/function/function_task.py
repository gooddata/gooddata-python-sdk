#  (C) 2024 GoodData Corporation
from typing import Optional, Union

import structlog
from gooddata_flight_server import FlightDataTaskResult, Task, TaskError, TaskResult

from gooddata_flexconnect.function.function import FlexConnectFunction

_LOGGER = structlog.get_logger("gooddata_flexconnect.task")


class FlexConnectFunctionTask(Task):
    __slots__ = ("_fun", "_parameters", "_columns", "_headers")

    def __init__(
        self,
        fun: FlexConnectFunction,
        parameters: dict,
        columns: Optional[tuple[str, ...]],
        headers: dict[str, list[str]],
        cmd: bytes,
        cancellable: bool = True,
        task_id: Optional[str] = None,
    ):
        super().__init__(cmd, cancellable, task_id)

        self._fun = fun
        self._parameters = parameters
        self._columns = columns
        self._headers = headers

        _LOGGER.info("flexconnect_task_created", fun=fun.Name, task_id=self._task_id)

    @property
    def fun_name(self) -> Optional[str]:
        return self._fun.Name

    def run(self) -> Union[TaskResult, TaskError]:
        structlog.contextvars.bind_contextvars(fun=self._fun.Name, task_id=self._task_id)
        _LOGGER.info("flexconnect_task_run")

        result = self._fun.call(
            parameters=self._parameters,
            columns=self._columns,
            headers=self._headers,
        )

        return FlightDataTaskResult.for_data(result)

    def on_task_cancel(self) -> None:
        _LOGGER.info("flexconnect_task_cancel", fun=self._fun.Name, task_id=self._task_id)

        self._fun.cancel()
