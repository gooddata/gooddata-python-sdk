#  (C) 2023 GoodData Corporation
import abc
import threading
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Optional, TypeAlias, Union, final

import pyarrow.flight
from gooddata_flight_server.errors.error_code import ErrorCode
from gooddata_flight_server.errors.error_info import ErrorInfo
from gooddata_flight_server.tasks.base import ArrowData
from gooddata_flight_server.tasks.task_error import TaskError
from readerwriterlock import rwlock


class FlightDataTaskResult(abc.ABC):
    """
    This class represents a result of a task execution which contains some data
    that can be sent out to clients via DoGet.

    Subclasses should implement methods to get schema of the data, get the actual
    data and perform the cleanup.

    The class provides essential customization and synchronization mechanisms so
    that subclasses can use it to realize:

    - results whose data can only be consumed once
    - results whose data that can be consumed repeatedly
    """

    __slots__ = ("_single_use_data", "_data_lock", "_claim_lock", "_claimed", "_closed")

    def __init__(self, single_use_data: bool = False) -> None:
        self._single_use_data = single_use_data
        self._data_lock: rwlock.RWLockRead = rwlock.RWLockRead()

        self._claim_lock = threading.Lock()
        self._claimed = False
        self._closed = False

    def _acquire_reader(self) -> Optional[rwlock.Lockable]:
        rlock = self._data_lock.gen_rlock()
        if not rlock.acquire(blocking=False):
            # lock cannot be acquired -> means write lock is taken -> means data is being closed
            return None

        if self._closed:
            # lock was obtained by the result was closed already
            rlock.release()
            return None

        if self._single_use_data:
            # if the data is single-use, then the first-reader wins the
            # claim and all others will fail

            if not self._claim_lock.acquire(blocking=True):
                # someone else is already claiming the result -> this reader lost
                rlock.release()
                return None

            if self._claimed:
                # someone else has already claimed the result -> this reader lost
                self._claim_lock.release()
                rlock.release()

                return None

            # this reader has won the claim
            self._claimed = True
            self._claim_lock.release()

        return rlock

    @property
    def single_use_data(self) -> bool:
        """
        Indicates whether the data contained in this result can only be used / consumed once.

        In this type of results, the first caller of `acquire_data` wins and can read the data. Everyone
        else coming later will fail and will not be able to read.

        :return: true if single use, false if not
        """
        return self._single_use_data

    @abc.abstractmethod
    def get_schema(self) -> pyarrow.Schema:
        """
        Gets schema of the result.

        :return: Arrow schema
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _get_data(self) -> Union[Iterable[ArrowData], ArrowData]:
        """
        Gets the data. By default, the method is supposed to return the same data upon
        repeated calls. If the subclass generates result data that can only be consumed
        once, then it must set

        :return: a single record batch, tables, RecordBatchReaders or iterable therefor
         (iterable may contain mixed types)
        """
        raise NotImplementedError

    @abc.abstractmethod
    def _close(self) -> None:
        """
        Implement this method to close / cleanup any resources tied to this result.

        Note: this method is protected from repeated calls. It is guaranteed it will
        be called exactly once.

        :return: nothing
        """
        raise NotImplementedError

    @final
    def acquire_data(
        self,
    ) -> tuple[rwlock.Lockable, Union[Iterable[ArrowData], ArrowData]]:
        """
        Acquires this result's data. This method will first ensure that the data is
        still available for reading:

        1. result was not closed
        2. if the result has single-use data, then the current thread is the first
           to try and consume it

        If these checks succeed, then it returns a tuple of:

        - read lock that is guarding the result from being closed
        - the data itself

        The data can be the following:

        - Arrow RecordBatch, Table or RecordBatchReader
        - Iterable (e.g. generator) of thereof; the iterated elements may be heterogeneous

        IMPORTANT: the caller who acquires the data MUST release the returned read lock after
        it is done with the data.

        :return: tuple of (acquired lock, data)
        :raises: pyarrow.flight.FlightError: when this result's data was single-use and was already consumed;
         the error contains ErrorCode COMMAND_RESULT_CONSUMED.
        """
        rlock = self._acquire_reader()
        if rlock is None:
            raise ErrorInfo.for_reason(
                ErrorCode.COMMAND_RESULT_CONSUMED,
                "Result data was already consumed or closed.",
            ).to_server_error()

        return rlock, self._get_data()

    @final
    def close(self) -> None:
        with self._data_lock.gen_wlock():
            if self._closed:
                return

            self._closed = True

        # this is intentionally done without holding the lock
        # mainly to prevent deadlocks in more complex scenarios where
        # result is 'part of something else' and close() can
        # be called from multiple places and possibly lead
        # to recursion
        self._close()


@dataclass
class ListFlightsTaskResult:
    """
    This class represents a result of a task that listed available flights. The flight
    infos are materialized.
    """

    flight_infos: tuple[pyarrow.flight.FlightInfo, ...]

    def as_generator(self) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        yield from self.flight_infos


TaskResult: TypeAlias = Union[FlightDataTaskResult, ListFlightsTaskResult]


class TaskExecutionResult:
    """
    Represents result of particular task execution. This indicates to the caller
    whether the task finished successfully or not or whether it was cancelled.
    """

    __slots__ = ("_task_id", "_cmd", "_result", "_cancelled", "_error")

    def __init__(
        self,
        task_id: str,
        cmd: bytes,
        result: Optional[TaskResult],
        cancelled: bool,
        error: Optional[TaskError],
    ):
        self._task_id = task_id
        self._cmd = cmd
        self._result = result
        self._cancelled = cancelled
        self._error = error

    @property
    def task_id(self) -> str:
        """
        :return: Task id to which the result pertains.
        """
        return self._task_id

    @property
    def cmd(self) -> bytes:
        """
        :return: command from Flight descriptor which resulted in the creation of the task that
         created this result
        """
        return self._cmd

    @property
    def result(self) -> Optional[TaskResult]:
        """
        :return: result of task's successful execution; None if the task failed or was cancelled
        """
        return self._result

    @property
    def cancelled(self) -> bool:
        """
        :return: indicates whether the task was cancelled; True if cancelled; False if not
        """
        return self._cancelled

    @property
    def error(self) -> Optional[TaskError]:
        """
        :return: error that caused the task to fail; None if the task has not failed
        """
        return self._error
