#  (C) 2024 GoodData Corporation
from typing import Any, Union

import pyarrow
from typing_extensions import TypeAlias

# TODO: may be move to some more 'common' place
ArrowData: TypeAlias = Union[pyarrow.lib.Table, pyarrow.lib.RecordBatchReader]


class TaskWaitTimeoutError(TimeoutError):
    """
    This exception is thrown when TaskExecutor's wait_for_result() times out.

    The exception includes task identifier and the payload that was used to
    start the task.
    """

    def __init__(self, task_id: str, cmd: Any) -> None:
        self.task_id = task_id
        self.cmd = cmd
