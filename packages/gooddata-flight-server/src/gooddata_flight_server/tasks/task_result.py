#  (C) 2024 GoodData Corporation
import abc
import threading
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from typing import Callable, Optional, Union, final

import pyarrow.flight
import structlog
from readerwriterlock import rwlock
from typing_extensions import TypeAlias

from gooddata_flight_server.errors.error_code import ErrorCode
from gooddata_flight_server.errors.error_info import ErrorInfo
from gooddata_flight_server.tasks.base import ArrowData
from gooddata_flight_server.tasks.task_error import TaskError

OnCloseCallback: TypeAlias = Callable[[], None]


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

    __slots__ = (
        "_single_use_data",
        "_data_lock",
        "_claim_lock",
        "_claimed",
        "_closed",
    )

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

    @staticmethod
    def for_table(table: pyarrow.Table, on_close: Optional[OnCloseCallback] = None) -> "FlightDataTaskResult":
        """
        Factory to create result for an Arrow table. This result allows for repeated
        reads.

        :param table: table with result's data
        :param on_close: optionally provide a callback function that will be
         invoked when the result is closed; you may find this useful if your service
         needs to do additional cleanup / release resources bound with the result
        :return: a new instance of result
        """
        return _TableTaskResult(table, on_close=on_close)

    @staticmethod
    def for_reader(
        reader: pyarrow.RecordBatchReader, on_close: Optional[OnCloseCallback] = None
    ) -> "FlightDataTaskResult":
        """
        Factory to create result for an RecordBatchReader. The created result will
        be 'single use' - the data from the reader can only be consumed once. After that,
        the result will be closed. Useful when your service creates streams of Arrow data.

        :param reader: reader result's data
        :param on_close: optionally provide a callback function that will be
         invoked when the result is closed; you may find this useful if your service
         needs to do additional cleanup / release resources bound with the result
        :return: a new instance of result
        """
        return _ReaderTaskResult(reader, on_close=on_close)

    @staticmethod
    def for_data(data: ArrowData, on_close: Optional[OnCloseCallback] = None) -> "FlightDataTaskResult":
        """
        Convenience factory function to create result from either Arrow Table or RecordBatchReader.

        See `for_table` and `for_reader` for further detail.

        :param data: either Arrow Table or RecordBatchReader
        :param on_close: optionally provide a callback function that will be
         invoked when the result is closed; you may find this useful if your service
         needs to do additional cleanup / release resources bound with the result
        :return: a new instance of result
        """
        if isinstance(data, pyarrow.Table):
            return FlightDataTaskResult.for_table(data, on_close=on_close)
        elif isinstance(data, pyarrow.RecordBatchReader):
            return FlightDataTaskResult.for_reader(data, on_close=on_close)

        raise ValueError(
            f"Unexpected type of 'data': {type(data).__name__}. Expected Arrow Table or RecordBatchReader."
        )


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


_LOGGER = structlog.get_logger("gooddata_flight_server.task_executor")


class _TableTaskResult(FlightDataTaskResult):
    def __init__(self, table: pyarrow.Table, on_close: Optional[OnCloseCallback] = None) -> None:
        super().__init__(single_use_data=False)

        self._table: pyarrow.Table = table
        self._on_close = on_close

    def get_schema(self) -> pyarrow.Schema:
        return self._table.schema

    def _get_data(self) -> Union[Iterable[ArrowData], ArrowData]:
        return self._table

    def _close(self) -> None:
        del self._table

        try:
            if self._on_close is not None:
                self._on_close()
        except Exception:
            _LOGGER.warning("reader_on_close_failed", exc_info=True)


class _ReaderTaskResult(FlightDataTaskResult):
    def __init__(self, reader: pyarrow.RecordBatchReader, on_close: Optional[OnCloseCallback] = None) -> None:
        super().__init__(single_use_data=True)

        self._reader = reader
        self._on_close = on_close

    def get_schema(self) -> pyarrow.Schema:
        return self._reader.schema

    def _get_data(self) -> Union[Iterable[ArrowData], ArrowData]:
        return self._reader

    def _close(self) -> None:
        try:
            self._reader.close()
        except Exception:
            _LOGGER.warning("reader_close_failed", exc_info=True)
        finally:
            self._reader = None

        try:
            if self._on_close is not None:
                self._on_close()
        except Exception:
            _LOGGER.warning("reader_on_close_failed", exc_info=True)
