#  (C) 2023 GoodData Corporation
import threading
from typing import Union

import pyarrow.flight
import pytest
from gooddata_flight_server import ErrorCode, ErrorInfo, FlightDataTaskResult, Task, TaskError, TaskResult
from gooddata_flight_server.tasks.base import TaskWaitTimeoutError
from gooddata_flight_server.tasks.thread_task_executor import ThreadTaskExecutor

_TEST_TABLE = pyarrow.table({"col1": list(range(100))})


class _SuccessTaskWithLiveData(Task):
    def __init__(self) -> None:
        super().__init__(cmd=b"", cancellable=True, task_id=None)

    def run(self) -> Union[TaskResult, TaskError]:
        return FlightDataTaskResult.for_data(_TEST_TABLE.to_reader())


class _FailWithRaiseTask(Task):
    def __init__(self, error=ValueError("test error")) -> None:
        super().__init__(cmd=b"", cancellable=True, task_id=None)
        self.error = error

    def run(self) -> Union[TaskResult, TaskError]:
        raise self.error


class _FailWithTaskError(Task):
    def __init__(self) -> None:
        super().__init__(cmd=b"", cancellable=True, task_id=None)

    def run(self) -> Union[TaskResult, TaskError]:
        return TaskError(
            error_info=ErrorInfo.for_reason(ErrorCode.COMMAND_FAILED, "Something went wrong."),
            error_factory=pyarrow.flight.FlightServerError,
        )


class _BlockingTask(Task):
    def __init__(self) -> None:
        super().__init__(cmd=b"", cancellable=True, task_id=None)
        self.lock = threading.Lock()

    def run(self) -> Union[TaskResult, TaskError]:
        with self.lock:
            self.check_cancelled()

            return FlightDataTaskResult.for_data(_TEST_TABLE)


@pytest.fixture
def te_fixture() -> ThreadTaskExecutor:
    executor = ThreadTaskExecutor(
        task_threads=1,
        metric_prefix="test",
        keep_results_for=30,
    )

    return executor


def test_task_wait_for_success(te_fixture):
    task = _SuccessTaskWithLiveData()
    te_fixture.submit(task)

    exec_result = te_fixture.wait_for_result(task.task_id)

    assert exec_result is not None
    assert exec_result.error is None
    assert exec_result.cancelled is False
    assert exec_result.result is not None


def test_completed_task_result_cancellation1(te_fixture):
    task = _SuccessTaskWithLiveData()
    te_fixture.submit(task)

    # task completes and there is a result
    exec_result = te_fixture.wait_for_result(task.task_id)
    assert exec_result is not None

    # cancelling the task will lead to result being thrown away; because the
    # result is backed by live data which is now thrown away, the cancel
    # is treated as being successful
    assert te_fixture.cancel(task.task_id) is True

    # subsequent call will not have anything for the task anymore
    # because it is not running and the result is gone as well
    assert te_fixture.wait_for_result(task.task_id) is None


def test_task_wait_for_error1(te_fixture):
    task = _FailWithRaiseTask()
    te_fixture.submit(task)
    exec_result = te_fixture.wait_for_result(task.task_id)

    assert exec_result is not None
    assert exec_result.error is not None
    assert exec_result.cancelled is False
    assert exec_result.result is None


def test_task_wait_for_error2(te_fixture):
    task = _FailWithTaskError()
    te_fixture.submit(task)
    exec_result = te_fixture.wait_for_result(task.task_id)

    assert exec_result is not None
    assert exec_result.error is not None
    assert exec_result.cancelled is False
    assert exec_result.result is None


def test_task_wait_when_missing(te_fixture):
    result = te_fixture.wait_for_result("nonsense")

    assert result is None


def test_task_cancel_while_pending(te_fixture):
    # a task that blocks the one and only executor thread is submitted first
    # this means any other tasks will be stuck in the queue
    blocking_task = _BlockingTask()
    blocking_task.lock.acquire()
    te_fixture.submit(task=blocking_task)

    try:
        # now submit some other task - this will be waiting in queue forever
        success_task = _SuccessTaskWithLiveData()
        te_fixture.submit(task=success_task)

        # trying to get its result times out
        with pytest.raises(TaskWaitTimeoutError):
            te_fixture.wait_for_result(task_id=success_task.task_id, timeout=0.001)

        # cancel is successful
        assert te_fixture.cancel(task_id=success_task.task_id) is True

        # after that the wait returns a result describing cancellation
        exec_result = te_fixture.wait_for_result(task_id=success_task.task_id)

        assert exec_result.cancelled is True
        assert exec_result.error is None
        assert exec_result.result is None
    finally:
        # unblock the first task so that tests don't hang forever
        blocking_task.lock.release()


def test_task_cancel_while_running(te_fixture):
    blocking_task = _BlockingTask()
    blocking_task.lock.acquire()
    te_fixture.submit(task=blocking_task)

    # task is doing some blocking operation within the run() method - waiting for result times out
    with pytest.raises(TaskWaitTimeoutError):
        te_fixture.wait_for_result(task_id=blocking_task.task_id, timeout=0.001)

    # cancel is successful
    assert te_fixture.cancel(task_id=blocking_task.task_id) is True

    # release the lock that blocks the task run(), now it gets to execute and should
    # run into cancel notification
    blocking_task.lock.release()

    exec_result = te_fixture.wait_for_result(task_id=blocking_task.task_id)
    assert exec_result.cancelled is True
    assert exec_result.result is None
    assert exec_result.error is None


@pytest.fixture
def te_error_fixture(te_fixture):
    def _factory(error) -> tuple[ThreadTaskExecutor, str]:
        task = _FailWithRaiseTask(error=error)
        te_fixture.submit(task)

        return te_fixture, task.task_id

    return _factory


def test_task_error_handling1(te_error_fixture):
    """
    Value error is converted to BAD_ARGUMENT (user error)
    """
    te, task_id = te_error_fixture(error=ValueError("bad argument"))
    exec_result = te.wait_for_result(task_id=task_id)

    assert exec_result.error is not None
    assert exec_result.error.error_info.code == ErrorCode.BAD_ARGUMENT
    assert exec_result.error.error_info.msg == "bad argument"


def test_task_error_handling2(te_error_fixture):
    """
    Flight Errors with quiver error codes in them are propagated as-is.
    """
    te, task_id = te_error_fixture(
        error=ErrorInfo.for_reason(ErrorCode.NOT_READY, "some other error").to_unavailable_error()
    )
    exec_result = te.wait_for_result(task_id=task_id)

    assert exec_result.error is not None
    assert exec_result.error.error_info.code == ErrorCode.NOT_READY


def test_task_error_handling3(te_error_fixture):
    """
    Bare-bone flight errors are wrapped into unknown errors. Perhaps worth revisiting and converting
    to internal errors?
    """
    te, task_id = te_error_fixture(error=pyarrow.flight.FlightServerError("problem"))
    exec_result = te.wait_for_result(task_id=task_id)

    assert exec_result.error is not None
    assert exec_result.error.error_info.code == ErrorCode.UNKNOWN


def test_task_error_handling4(te_error_fixture):
    """
    Other errors are converted to COMMAND_FAILED
    """
    te, task_id = te_error_fixture(error=AssertionError("Some runtime error"))
    exec_result = te.wait_for_result(task_id=task_id)

    assert exec_result.error is not None
    assert exec_result.error.error_info.code == ErrorCode.COMMAND_FAILED
