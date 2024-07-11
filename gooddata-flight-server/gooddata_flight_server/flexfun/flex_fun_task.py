#  (C) 2024 GoodData Corporation
from typing import Iterable, Optional, Union

import pyarrow

from gooddata_flight_server.flexfun.flex_fun import FlexFun
from gooddata_flight_server.tasks.base import ArrowData
from gooddata_flight_server.tasks.task import Task
from gooddata_flight_server.tasks.task_error import TaskError
from gooddata_flight_server.tasks.task_result import FlightDataTaskResult, TaskResult


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

    def run(self) -> Union[TaskResult, TaskError]:
        result = self._fun.call(parameters=self._parameters, columns=self._columns, headers=self._headers)

        return _FlexFunResult(result)

    def on_task_cancel(self) -> None:
        self._fun.cancel()
