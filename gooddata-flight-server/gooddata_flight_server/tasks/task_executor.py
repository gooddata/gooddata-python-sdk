#  (C) 2024 GoodData Corporation
import abc
from typing import Optional

from gooddata_flight_server.tasks.task import Task
from gooddata_flight_server.tasks.task_result import TaskExecutionResult


class TaskAttributes:
    TaskId = "gooddata_flight_server.task_id"
    TaskCancelled = "gooddata_flight_server.task_cancelled"
    TaskError = "gooddata_flight_server.task_error"
    TaskErrorCode = "gooddata_flight_server.task_error.code"
    TaskErrorMsg = "gooddata_flight_server.task_error.msg"
    TaskErrorDetail = "gooddata_flight_server.task_error.detail"


class TaskExecutor(abc.ABC):
    """
    Declares interface for Task Executors. These allow asynchronous execution
    of tasks which 'somehow' generate flight data.

    The methods on this interface are designed to support a pollable
    GetFlightInfo -> DoGet flows. A task can be submitted, polled for
    completion or cancelled.

    Once the task finishes (with any outcome), a TaskExecutionResult is available
    and describes the outcome. On success, the execution result contains
    a reference to task's actual result.

    The execution result and the task's actual result are retained in the
    executor for a limited (configurable) amount of time.

    The actual task result is either:

    - FlightDataTaskResult - which represents data that was 'generated' by the task
      somehow and is available for single or repeated reads
    - FlightPathTaskResult - which represent data stored under some flight path;
      typically, flight commands include option to sink result under a flight path and
      if that is the case the task will generate data and store it and then return
      the pointer
    """

    @abc.abstractmethod
    def submit(
        self,
        task: Task,
    ) -> None:
        """
        Submit a new task that will perform all work as described in the provided command.

        :param task: task to run
        :return: nothing, task is always submitted
        """
        raise NotImplementedError

    @abc.abstractmethod
    def wait_for_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[TaskExecutionResult]:
        """
        Wait for the task with the provided task id to finish.

        If a task already finished and this service still has records describing it's result, then
        the saved result is returned immediately.

        Otherwise, if a task is pending, the method will block (optionally with timeout) until
        the task completes. If it does not complete in given timeframe, the code will raise TimeoutError.

        Note: if the task was cancelled, the result will have 'cancelled' indicator flag set to True.

        :param task_id: task id to wait for
        :param timeout: time to wait for completion
        :raise TaskWaitTimeoutError: if the wait for task completion timed out
        :return: result or None if there is no such task
        """
        raise NotImplementedError

    @abc.abstractmethod
    def cancel(self, task_id: str) -> bool:
        """
        Try to cancel a task - either by dropping it from the task queue or by cancelling
        a running task or dropping a result of already finished task.

        :param task_id: task id to cancel
        :return: true if cancelled, false if cancel not possible (no such task or task not cancellable anymore)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def close_result(self, task_id: str) -> bool:
        """
        Try to close result of a previously completed task.

        :param task_id: task id, whose result to close
        :return: true if result closed, false if no result for that task id
        """
        raise NotImplementedError
