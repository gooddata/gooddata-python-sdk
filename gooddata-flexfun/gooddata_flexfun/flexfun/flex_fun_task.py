#  (C) 2024 GoodData Corporation
from collections.abc import Iterable
from typing import Optional, Union

import pyarrow
import structlog
from gooddata_flight_server import ArrowData, FlightDataTaskResult, Task, TaskError, TaskResult

from gooddata_flexfun.flexfun.flex_fun import FlexFun

_LOGGER = structlog.get_logger("gooddata_flexfun.task")


class _FlexFunResult(FlightDataTaskResult):
    __slots__ = ("_result",)

    def __init__(self, result: ArrowData) -> None:
        # if function returns result as a reader, then naturally it can only be
        # consumed once.
        #
        # on the other hand, if the result is table, it can be read as long as
        # the result is present in the system (influenced by result TTL setting)
        super().__init__(single_use_data=isinstance(result, pyarrow.RecordBatchReader))

        self._result = result

    def get_schema(self) -> pyarrow.Schema:
        return self._result.schema

    def _get_data(self) -> Union[Iterable[ArrowData], ArrowData]:
        return self._result

    def _close(self) -> None:
        if isinstance(self._result, pyarrow.RecordBatchReader):
            self._result.close()

        self._result = None


class FlexFunTask(Task):
    __slots__ = ("_fun", "_parameters", "_columns", "_headers")

    def __init__(
        self,
        fun: FlexFun,
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

        _LOGGER.info("flexfun_task_created", fun=fun.Name, task_id=self._task_id)

    @property
    def fun_name(self) -> Optional[str]:
        return self._fun.Name

    def run(self) -> Union[TaskResult, TaskError]:
        structlog.contextvars.bind_contextvars(fun=self._fun.Name, task_id=self._task_id)
        _LOGGER.info("flexfun_task_run")

        result = self._fun.call(
            parameters=self._parameters,
            columns=self._columns,
            headers=self._headers,
        )

        return _FlexFunResult(result)

    def on_task_cancel(self) -> None:
        _LOGGER.info("flexfun_task_cancel", fun=self._fun.Name, task_id=self._task_id)

        self._fun.cancel()
