#  (C) 2024 GoodData Corporation
import abc
import threading
import time
from collections.abc import Generator
from concurrent.futures import CancelledError, Future, ThreadPoolExecutor
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Optional, Union

import opentelemetry.context as otelctx
import pyarrow.flight
import structlog
from opentelemetry import trace

from gooddata_flight_server.errors.error_code import ErrorCode
from gooddata_flight_server.errors.error_info import ErrorInfo
from gooddata_flight_server.tasks.base import TaskWaitTimeoutError
from gooddata_flight_server.tasks.metrics import TaskExecutorMetrics
from gooddata_flight_server.tasks.task import Task
from gooddata_flight_server.tasks.task_error import TaskError
from gooddata_flight_server.tasks.task_executor import (
    TaskAttributes,
    TaskExecutor,
)
from gooddata_flight_server.tasks.task_result import (
    FlightDataTaskResult,
    TaskExecutionResult,
    TaskResult,
)
from gooddata_flight_server.tasks.temporal_container import TemporalContainer
from gooddata_flight_server.utils.otel_tracing import SERVER_TRACER


@dataclass()
class _TaskExecutionStats:
    """
    Container for task execution statistics.

    Most of the fields here are optional. When the task completes, only fields
    that describe work that was actually done will be set (e.g. so say prereq fields
    will not be set if the task had no prerequisites).
    """

    created: float
    """
    time when the task was created
    """

    run_submitted: Optional[float] = None
    """
    time when task was submitted to thread pool to invoke the run()
    """

    run_started: Optional[float] = None
    """
    time when some thread actually started the run()
    """

    run_completed: Optional[float] = None
    """
    time when the run() completed (regardless of the result)
    """

    completed: Optional[float] = None
    """
    time when all work for task execution completed. if the task was actually run,
    then this value is same as `run_completed`. if the task failed/was cancelled
    during prerequisite resolution, then this will be equal to `prereq_completed`.
    """

    @property
    def run_waited_duration(self) -> float:
        if self.run_submitted is None or self.run_started is None:
            return -1

        return self.run_started - self.run_submitted

    @property
    def run_duration(self) -> float:
        if self.run_started is None or self.run_completed is None:
            return -1

        return self.run_completed - self.run_started

    @property
    def duration(self) -> float:
        if self.completed is None:
            return -1

        return self.completed - self.created

    @property
    def durations_to_dict(self) -> dict[str, float]:
        return {
            "run_waited_duration": self.run_waited_duration,
            "run_duration": self.run_duration,
            "duration": self.duration,
        }


class _TaskExecutionCallbacks(abc.ABC):
    """
    This is an interface between ThreadTaskExecutor and the TaskExecution. The TaskExecution
    orchestrates work for a particular task while the ThreadTaskExecutor knows how to actually
    do the work.
    """

    def run_task(
        self,
        task_execution: "_TaskExecution",
    ) -> Future:
        """
        Asynchronously run the task.

        :param task_execution: task execution whose task is now ready to run
        :return: future result of the task run
        """
        raise NotImplementedError

    def process_task_result(
        self,
        task_execution: "_TaskExecution",
        result: Future,
    ) -> TaskExecutionResult:
        """
        This will be called when the task run itself completes. It is guaranteed
        that the `result` future is completed.

        Errors (including cancellation) are propagated either as the special TaskError
        return value or by raising exception. The method must be prepared for this and
        handle both cases.

        After this method completes, the task executor must have a result associated
        with the task and must be able to return it to the callers who come asking for it.

        :param task_execution: task_execution whose task run finished
        :param result: completed future
        :return: task's execution result
        """
        raise NotImplementedError


class _TaskExecution:
    """
    This class represents a task execution and is responsible for its orchestration.

    The class itself does not do any heavy lifting, but keeps track of the task execution
    state and interacts with TaskExecutor to actually perform the next steps (e.g. running
    prereq resolution, running task itself, processing results / errors etc)
    """

    __slots__ = (
        "_task",
        "_cb",
        "_logging_ctx",
        "_trace_exec",
        "_result_future",
        "_lock",
        "_completed",
        "_stats",
    )

    def __init__(
        self,
        task: Task,
        cb: _TaskExecutionCallbacks,
    ) -> None:
        self._task = task
        self._cb = cb
        self._logging_ctx = structlog.contextvars.get_contextvars() or {}
        self._trace_exec = (
            otelctx.get_current(),
            SERVER_TRACER.start_span(
                "task_execution",
                attributes={TaskAttributes.TaskId: self._task.task_id},
            ),
        )

        self._stats = _TaskExecutionStats(created=time.perf_counter())
        # lock for state synchro, intentionally reused in conditional variable
        #
        # note: reentrant lock is necessary because of the cancel() method:
        # - future cancellation happens while holding this lock
        # - during future cancellation, the code in Future invokes the
        #   registered callbacks and these also use this same lock
        self._lock = threading.RLock()

        # all these are protected using the lock
        self._result_future: Optional[Future[Union[TaskResult, TaskError]]] = None
        self._completed: threading.Condition = threading.Condition(self._lock)

    @property
    def task(self) -> Task:
        return self._task

    @property
    def task_id(self) -> str:
        return self._task.task_id

    @property
    def stats(self) -> _TaskExecutionStats:
        return self._stats

    @property
    def logging_ctx(self) -> dict[str, Any]:
        return self._logging_ctx

    def _complete_execution_span(self, execution_result: TaskExecutionResult) -> None:
        execution_span = self._trace_exec[1]

        if execution_result.error is not None:
            task_error = execution_result.error
            execution_span.set_status(trace.StatusCode.ERROR)

            execution_span.add_event(
                TaskAttributes.TaskError,
                attributes={
                    TaskAttributes.TaskErrorCode: ErrorCode.name(task_error.error_info.code),
                    TaskAttributes.TaskErrorMsg: task_error.error_info.msg,
                    TaskAttributes.TaskErrorDetail: task_error.error_info.detail or "",
                },
            )
        elif execution_result.cancelled:
            execution_span.set_status(trace.StatusCode.OK)
            execution_span.add_event(TaskAttributes.TaskCancelled)
        else:
            execution_span.set_status(trace.StatusCode.OK)

        execution_span.end()

    def on_result_done(self, fut: Future) -> None:
        assert fut == self._result_future

        with self._lock:
            execution_result = self._cb.process_task_result(self, self._result_future)
            self._completed.notify_all()

        self._complete_execution_span(execution_result)

    @contextmanager
    def use_execution_span(self) -> Generator[trace.Span, None, None]:
        prev_otel_ctx = otelctx.attach(self._trace_exec[0])
        try:
            with trace.use_span(
                self._trace_exec[1],
                end_on_exit=False,
                record_exception=False,
                set_status_on_exception=False,
            ) as span:
                yield span
        finally:
            otelctx.detach(prev_otel_ctx)

    def start(self) -> None:
        """
        Starts the task execution:

        - submits the task for execution & sets up callbacks

        Note: this method is called at point where noone else yet knows about the
        task. Thus, there is no need for synchro.
        """
        assert self._result_future is None

        self._result_future = self._cb.run_task(self)
        self._result_future.add_done_callback(self.on_result_done)

    def cancel(self) -> bool:
        """
        Cancels the execution.

        IMPORTANT: task executor must not hold any locks at the time of cancellation.

        :return: True if cancel was successful, false if it was not possible
        """
        assert self._result_future is not None

        with self._lock:
            if self._result_future.cancel():
                # if future cancel() succeeded, it means the task never run, it was just
                # sitting in the queue and got dropped; note: the done callback registered
                # on the future itself will take care of cleaning the books
                return True

            # otherwise, the task must be running already, so try to force cancel
            # as it is running; depending on the state of the task, this may or
            # may not be possible
            return self._task.cancel()

    def wait_for_completion(self, timeout: Optional[float] = None) -> None:
        with self._lock:
            completed = self._completed.wait(timeout=timeout)

        if not completed:
            raise TaskWaitTimeoutError(task_id=self._task.task_id, cmd=self._task.cmd)


def _create_task_error(e: Exception) -> TaskError:
    if isinstance(e, pyarrow.flight.FlightError):
        error_info = ErrorInfo.from_pyarrow_error(e)

        # propagate any captured flight errors as-is
        return TaskError(
            error_info=error_info,
            error_factory=type(e),
        )
    elif isinstance(e, ValueError):
        return TaskError(
            error_info=ErrorInfo.for_reason(ErrorCode.BAD_ARGUMENT, str(e)),
            error_factory=pyarrow.flight.FlightServerError,
        )

    # other, non-flight errors are bundled into a more generic FlightServerError with
    # COMMAND_FAILED error code.
    extra_msg = "There was an error while running task"

    error_info = ErrorInfo.for_exc(
        ErrorCode.COMMAND_FAILED,
        e=e,
        extra_msg=extra_msg,
        include_traceback=True,
    )

    return TaskError(
        error_info=error_info,
        error_factory=pyarrow.flight.FlightServerError,
    )


class ThreadTaskExecutor(TaskExecutor, _TaskExecutionCallbacks):
    """
    Implementation of TaskExecutor interface that uses a pluggable TaskFactory
    to create tasks to run and then submits those into a ThreadPoolExecutor.
    """

    def __init__(
        self,
        metric_prefix: str,
        task_threads: int = 4,
        result_close_threads: int = 2,
        keep_results_for: int = 15,
    ) -> None:
        self._logger = structlog.get_logger("gooddata_flight_server.task_executor")
        self._metric_prefix = metric_prefix

        self._metrics = TaskExecutorMetrics(prefix=metric_prefix)
        self._executor = ThreadPoolExecutor(
            max_workers=task_threads,
            thread_name_prefix="gooddata_flight_server.task",
        )
        self._close_executor = ThreadPoolExecutor(
            max_workers=result_close_threads,
            thread_name_prefix="gooddata_flight_server.result_close",
        )

        self._task_lock = threading.Lock()
        self._queue_size: int = 0
        self._executions: dict[str, _TaskExecution] = {}

        self._results: TemporalContainer[TaskExecutionResult] = TemporalContainer(
            logger_name="gooddata_flight_server.result_container",
            grace_period=keep_results_for,
            entry_evict_fun=self._on_finished_task_evicted,
        )

    def _async_close_result(self, task_id: str, task_result: FlightDataTaskResult) -> None:
        self._metrics.close_queue_size.dec()

        try:
            task_result.close()
        except Exception:
            self._logger.warning("expired_result_close_failed", task_id=task_id, exc_info=True)

    def _on_finished_task_evicted(self, result: TaskExecutionResult) -> None:
        """
        When a finished task is evicted from the temporal container, it means the
        GetFlightInfo for this particular task can no longer be answered on this node.
        """
        self._logger.debug(
            "result_evicted",
            task_id=result.task_id,
        )

        task_result = result.result
        if isinstance(task_result, FlightDataTaskResult):
            self._metrics.close_queue_size.inc()
            self._close_executor.submit(self._async_close_result, result.task_id, task_result)

        self._executions.pop(result.task_id, None)

    def _create_task_exec_result(
        self,
        task_execution: _TaskExecution,
        f: Future,
    ) -> TaskExecutionResult:
        assert f.done()

        task = task_execution.task
        durations = task_execution.stats.durations_to_dict
        self._metrics.task_completed.inc()

        try:
            r = f.result()

            if isinstance(r, TaskError):
                task_error = task.on_task_error(r) or r

                if task_error.client_error:
                    self._logger.info("task_failed", task_id=task.task_id, **durations)
                else:
                    self._logger.error("task_failed", task_id=task.task_id, **durations)
                    self._metrics.task_errors.inc()

                return TaskExecutionResult(
                    task_id=task.task_id,
                    cmd=task.cmd,
                    result=None,
                    error=task_error,
                    cancelled=False,
                )

            self._logger.info("task_finished", task_id=task.task_id, **durations)

            return TaskExecutionResult(
                task_id=task.task_id,
                cmd=task.cmd,
                result=r,
                error=None,
                cancelled=False,
            )
        except CancelledError:
            self._metrics.task_cancelled.inc()

            self._logger.info("task_cancelled", task_id=task.task_id, **durations)

            return TaskExecutionResult(
                task_id=task.task_id,
                cmd=task.cmd,
                result=None,
                error=None,
                cancelled=True,
            )
        except Exception as e:
            if isinstance(e, pyarrow.flight.FlightError):
                # the FlightError's usually come when interfacing with other services such as
                # doing DoPut to shard or when doing DoExchange to some worker process.
                #
                # FlightError raised by task will usually (in case of serious, unexpected errors)
                # include additional detail (such as stacktrace) - this is normally omitted when
                # just logging the exception itself because they are part of the extra_info
                #
                # so this code unpack the error and does additional login
                task_error = _create_task_error(e)
                error_data = {
                    "nested_msg": task_error.error_info.msg,
                    "nested_stacktrace": task_error.error_info.detail,
                    "nested_code": ErrorCode.name(task_error.error_info.code),
                }
            else:
                task_error = _create_task_error(e)
                error_data = {}

            try:
                task_error = task.on_task_error(task_error) or task_error
            except Exception:
                pass

            if task_error.client_error:
                self._logger.info(
                    "task_failed",
                    task_id=task.task_id,
                    **durations,
                    **error_data,
                )
            else:
                self._logger.error(
                    "task_failed",
                    task_id=task.task_id,
                    exc_info=e,
                    **durations,
                    **error_data,
                )
                self._metrics.task_errors.inc()

            return TaskExecutionResult(
                task_id=task.task_id,
                cmd=task.cmd,
                result=None,
                cancelled=False,
                error=task_error,
            )

    def _task_run_wrapper(self, task_execution: _TaskExecution) -> Any:
        task = task_execution.task
        logging_ctx = task_execution.logging_ctx
        stats = task_execution.stats

        stats.run_started = time.perf_counter()
        structlog.contextvars.clear_contextvars()
        structlog.contextvars.bind_contextvars(**logging_ctx)

        with (
            task_execution.use_execution_span(),
            SERVER_TRACER.start_as_current_span("task_run", attributes={TaskAttributes.TaskId: task.task_id}),
        ):
            self._logger.info(
                "task_run",
                task_id=task.task_id,
                waited=stats.run_waited_duration,
            )
            self._metrics.wait_time.observe(stats.run_waited_duration)

            try:
                return task.run()
            finally:
                stats.run_completed = time.perf_counter()
                stats.completed = stats.run_completed

                self._metrics.task_duration.observe(stats.run_duration)
                self._metrics.task_e2e_duration.observe(stats.duration)

    def _finish_task_with_result(self, task_execution: "_TaskExecution", result: TaskExecutionResult) -> None:
        task = task_execution.task
        with self._task_lock:
            self._executions.pop(task.task_id)
            self._results[task.task_id] = result
            self._queue_size -= 1

            if self._queue_size < 0:
                self._logger.warning("queue_size_corrupt", queue_size=self._queue_size)

        self._metrics.queue_size.set(self._queue_size)

    def run_task(
        self,
        task_execution: _TaskExecution,
    ) -> Future:
        with task_execution.use_execution_span(), SERVER_TRACER.start_as_current_span("task_run_submit"):
            task_execution.stats.run_submitted = time.perf_counter()

            return self._executor.submit(self._task_run_wrapper, task_execution)

    def process_task_result(
        self,
        task_execution: "_TaskExecution",
        future: Future,
    ) -> TaskExecutionResult:
        result = self._create_task_exec_result(task_execution, future)
        self._finish_task_with_result(task_execution, result)

        return result

    def submit(
        self,
        task: Task,
    ) -> None:
        # note: task execution constructor will snapshot current logging and tracing context
        execution = _TaskExecution(task=task, cb=self)

        with self._task_lock:
            self._queue_size += 1
            self._executions[task.task_id] = execution

        execution.start()
        self._metrics.queue_size.set(self._queue_size)

    def wait_for_result(self, task_id: str, timeout: Optional[float] = None) -> Optional[TaskExecutionResult]:
        with self._task_lock:
            execution = self._executions.get(task_id)
            result = self._results.get_entry(task_id)

        if result is not None:
            return result
        elif execution is not None:
            execution.wait_for_completion(timeout=timeout)

            return self._results.get_entry(task_id)

        return None

    def cancel(self, task_id: str) -> bool:
        with self._task_lock:
            execution = self._executions.get(task_id)
            result = self._results.get_entry(task_id)

        if result is not None:
            # task has already completed and there is a result associated
            #
            # interpret cancel as client not being interested in this anymore
            # and throw the result away
            #
            # unless the task resulted in a flight path (e.g. possibly a persisted
            # result), treat the cancellation as successful
            self._results.evict_entry(task_id)

            return True

        if execution is None:
            # the task was not and is not running - cancel not possible
            return False

        return execution.cancel()

    def close_result(self, task_id: str) -> bool:
        with self._task_lock:
            result = self._results.pop_entry(entry_id=task_id)

        if result is None:
            return False

        self._on_finished_task_evicted(result)
        return True

    def stop(self, cancel_running: bool = True, timeout: Optional[float] = None) -> None:
        """
        Stops the service. Any pending tasks will be immediately cancelled. Tasks that are already executing
        are allowed to complete.

        :param cancel_running: whether to cancel already running tasks
        :param timeout: time to way for all running tasks to finish
        :return: nothing
        """
        self._logger.info("task_exec_stopping", pending_tasks=len(self._executions))
        self._executor.shutdown(wait=False, cancel_futures=True)

        if cancel_running:
            with self._task_lock:
                for task in self._executions.values():
                    task.cancel()

        def _shutdown_executor() -> None:
            self._executor.shutdown(wait=True, cancel_futures=True)

        shutdown_thd = threading.Thread(target=_shutdown_executor)
        shutdown_thd.start()
        shutdown_thd.join(timeout=timeout)

        self._results.close()
