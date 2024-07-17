#  (C) 2024 GoodData Corporation
import abc
import threading
import uuid
from concurrent.futures import CancelledError
from typing import Optional, Union, final

from gooddata_flight_server.tasks.task_error import TaskError
from gooddata_flight_server.tasks.task_result import TaskResult


class Task(abc.ABC):
    """
    Abstract base class for executable tasks.

    This class provides the essential boilerplate and declares a single `run` method which
    should be implemented by subclasses. The `run` does the actual work and returns its
    result.

    The Task design is such that it allows for runtime cancel-ability:

    - task can be flagged as cancellable or not (default is True)
    - when cancellable, the `cancel` method can be used to indicate that the task
      should cancel
    - this turns on the cancelled indicator

    A cancellable task should test the cancelled indicator after each significant
    step and bail-out by raising CancelledError

    If the `run` method is entering a point of no return (e.g. cancel / rollback is
    no longer feasible), then it must first switch the task to be non-cancellable
    using the `switch_non_cancellable` - this may raise CancelledError if the `run`
    was raced and someone cancelled the task.
    """

    __slots__ = (
        "_task_id",
        "_cmd",
        "_cancel_lock",
        "_cancelled",
        "_cancellable",
        "_triggers",
    )

    def __init__(
        self,
        cmd: bytes,
        cancellable: bool = True,
        task_id: Optional[str] = None,
    ):
        self._task_id = task_id or uuid.uuid4().hex
        self._cmd = cmd
        self._cancel_lock = threading.Lock()
        self._cancelled = False
        self._cancellable = cancellable

    @final
    @property
    def task_id(self) -> str:
        return self._task_id

    @final
    @property
    def cmd(self) -> bytes:
        return self._cmd

    @final
    @property
    def cancelled(self) -> bool:
        """
        :return: true if the running task was cancelled
        """
        with self._cancel_lock:
            return self._cancelled

    def check_cancelled(self) -> None:
        """
        Checks whether task got cancelled - if so, raises CancelledError.

        This is utility method that may be used in Task.run() to perform
        cancellation checks.

        :return: nothing
        """
        if self.cancelled:
            raise CancelledError()

    @final
    def cancel(self) -> bool:
        """
        Try to cancel an *already running* task. Depending on the state of the task,
        this may or may not be possible.

        If the cancel succeeds, it is guaranteed that the task has no side-effects on
        the rest of the system - it is as if it never run.

        :return: True if cancel was successful, False if not
        """
        with self._cancel_lock:
            if not self._cancellable:
                return False

            first_cancel = not self._cancelled
            self._cancelled = True

            if first_cancel:
                try:
                    self.on_task_cancel()
                except Exception:
                    pass

            return True

    @final
    def switch_non_cancellable(self) -> None:
        """
        Switch the task to non-cancellable state.

        If the task got cancelled, raises CancelledError() at this point.
        Otherwise, sets the non-cancellable flag and returns.

        :return: nothing
        :raises: CancelledError if the switch is not possible because the task got cancelled already
        """
        with self._cancel_lock:
            if self._cancelled:
                raise CancelledError()

            self._cancellable = False

    def on_task_cancel(self) -> None:
        """
        This method will be called when a task is cancelled. That is, when it is still in
        cancellable state and someone calls the cancel() for the first time.

        The concrete implementation may optionally override this method to do something
        special on cancellation - like cascading the cancellation to further sub-components.

        Important: this method should not block.

        :return: nothing
        """
        return

    def on_task_error(self, error: TaskError) -> Optional[TaskError]:
        """
        This method will be called when a task fails with and raises an exception. It
        will be called after executor creates an instance of TaskError from the
        exception, and BEFORE it performs logging / tracking of the exception.

        The concrete implementation may optionally override this method to do something
        with the TaskError that was created by the executor. For example:

        - intercept automatically generated TaskError and replace / modify it
          (for example categorize client errors)

        - do custom logging / tracking of the error

        For convenience, if this method returns None, the executor will use the original
        task error instance as-is.

        :param error: TaskError as categorized by the executor
        :return: None if the original `error` should be used, otherwise an instance of
         TaskError
        """
        return error

    @abc.abstractmethod
    def run(self) -> Union[TaskResult, TaskError]:
        """
        Runs the task.

        This method should be implemented by subclasses and do work according to payload
        included in the `cmd`. Upon successful completion, the method should return a
        TaskResult - either FlightPathTaskResult (when task produced a flight path) or
        FlightDataTaskResult (when task created a live result).

        Upon failure, the task has two options - use whichever is more convenient:

        - either raise an exception: in this case the TaskExecutor will analyze and
          convert the exception to TaskError (with error codes and everything) using
          the built-in logic; the Task's `on_task_error` method will be called with
          the TaskError created using the standard error handling logic

        - return TaskError: this will be used by the TaskExecutor as-is. This option
          is useful in situations when the task wants to do more elaborate
          error handling / logging / reporting.

        :return: result of the task
        :raise Exception
        :raise CancelledError: when the task's run was cancelled
        """
        raise NotImplementedError
