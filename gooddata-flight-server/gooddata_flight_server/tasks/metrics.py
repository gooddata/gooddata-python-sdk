#  (C) 2024 GoodData Corporation
import threading
from typing import Callable, TypeVar

from prometheus_client import Counter, Gauge, Summary
from prometheus_client.metrics import MetricWrapperBase

_TMetric = TypeVar("_TMetric", bound=MetricWrapperBase)


class TaskExecutorMetrics:
    """
    Facade to access prometheus metrics that the task executor maintains.

    Note that this is somewhat more convoluted because:

    1. The TaskExecutor can produce metrics for various task types so metric names have to
       be variable (based on prefix)

    2. Prometheus does not like double-registration of metrics - this is something that
       definitely happens during various tests.

    Thus, for each metric, the class maintains a static mapping (prefix -> actual instance) and
    every time the class is instantiated with particular prefix, the constructor will get existing
    or create new instances.
    """

    _QueueSize: dict[str, Gauge] = {}
    _CloseQueueSize: dict[str, Gauge] = {}
    _WaitTime: dict[str, Summary] = {}
    _TaskE2EDuration: dict[str, Summary] = {}
    _TaskDuration: dict[str, Summary] = {}
    _TaskErrors: dict[str, Counter] = {}
    _TaskCancelled: dict[str, Counter] = {}
    _TaskCompleted: dict[str, Counter] = {}
    _MapLock = threading.Lock()

    @staticmethod
    def _get_or_create(d: dict[str, _TMetric], prefix: str, create_fun: Callable[[], _TMetric]) -> _TMetric:
        with TaskExecutorMetrics._MapLock:
            existing = d.get(prefix)
            if existing is not None:
                return existing

            new = create_fun()
            d[prefix] = new
            return new

    def __init__(self, prefix: str) -> None:
        self._prefix = prefix

        self.queue_size = self._get_or_create(
            TaskExecutorMetrics._QueueSize,
            prefix,
            lambda: Gauge(f"{prefix}_task_queue", "Number of tasks waiting in queue."),
        )

        self.close_queue_size = self._get_or_create(
            TaskExecutorMetrics._CloseQueueSize,
            prefix,
            lambda: Gauge(
                f"{prefix}_close_queue",
                "Number of task execution results waiting in the queue to be closed and cleaned up.",
            ),
        )

        self.wait_time = self._get_or_create(
            TaskExecutorMetrics._WaitTime,
            prefix,
            lambda: Summary(
                f"{prefix}_task_wait",
                "Time a task spends waiting in queue before it is executed.",
            ),
        )

        self.task_duration = self._get_or_create(
            TaskExecutorMetrics._TaskDuration,
            prefix,
            lambda: Summary(
                f"{prefix}_task_duration",
                "Duration of task run itself (does not include wait or prerequisite resolution duration).",
            ),
        )

        self.task_e2e_duration = self._get_or_create(
            TaskExecutorMetrics._TaskE2EDuration,
            prefix,
            lambda: Summary(
                f"{prefix}_task_e2e_duration",
                "End-to-end duration of the task execution. Includes prerequisite resolution duration and "
                "time spent in queue. This is the duration as observed by the callers.",
            ),
        )

        self.task_errors = self._get_or_create(
            TaskExecutorMetrics._TaskErrors,
            prefix,
            lambda: Counter(f"{prefix}_task_error", "Number of failed tasks."),
        )

        self.task_cancelled = self._get_or_create(
            TaskExecutorMetrics._TaskCancelled,
            prefix,
            lambda: Counter(f"{prefix}_task_cancelled", "Number of cancelled tasks."),
        )

        self.task_completed = self._get_or_create(
            TaskExecutorMetrics._TaskCompleted,
            prefix,
            lambda: Counter(
                f"{prefix}_task_completed",
                "Number of completed tasks - this includes all tasks regardless "
                "of how their execution completed (success, failure, cancel).",
            ),
        )
