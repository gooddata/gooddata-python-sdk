# (C) 2024 GoodData Corporation
import threading
import time
from collections.abc import Iterator
from dataclasses import dataclass
from typing import Any, Callable, Generic, Optional, TypeVar

import structlog
from readerwriterlock import rwlock

T = TypeVar("T")


@dataclass(frozen=True)
class _Entry(Generic[T]):
    value: T
    added: float


class TemporalContainer(Generic[T]):
    """
    Temporal container holds entries for a configured amount of time and then evicts
    them from the container. At the time of eviction, the container will dispatch
    the evicted entry to a callback function where cleanup of the entry can be done.
    """

    def __init__(
        self,
        logger_name: str,
        entry_evict_fun: Callable[[T], Any],
        grace_period: float = 10,
        collector_cycle_time: float = 1,
        start_collector: bool = True,
    ):
        """
        Create a new temporal container.

        :param logger_name: specify logger name where the container should emit logs
        :param entry_evict_fun: specify function to call when the entries are removed via expiration or when
         they are manually evicted using `evict_entry` call. This function should not block. Blocking evictions
         need to be done in a separate thread pool. Note: this method is called in fire-and-forget mode - the
         container does not rely on results of the eviction.
        :param grace_period: duration, in fractions of seconds, for which the entry will stay in the container
        :param collector_cycle_time: number of seconds to sleep the collector thread between collection cycles
        :param start_collector: whether to automatically start the collector
        """
        self._logger = structlog.get_logger(logger_name)
        self._entry_evict_fun = entry_evict_fun
        self._grace_period = grace_period
        self._collector_cycle_time = collector_cycle_time

        self._entries_rwlock: rwlock.RWLockRead = rwlock.RWLockRead()
        self._entries: dict[str, _Entry[T]] = {}

        self._thread: threading.Thread = threading.Thread(daemon=True, target=self._collector)
        self._closed = False

        if start_collector:
            self._thread.start()

    def _collector(self) -> None:
        """
        Collects results that have exceeded the grace period. The code takes advantage
        of the natural ordering of entries in the dict. When iterating dict, older entries are
        always before newer entries.

        So the code first goes read-only through the dict of entries, finds those that are
        expired and halts as soon as first non-expired entry is found. It then removes
        the entries and finally after all removals are done calls the eviction function.
        """
        self._logger.debug(
            "collector_started",
            grace=self._grace_period,
            cycle=self._collector_cycle_time,
        )

        while not self._closed:
            time.sleep(self._collector_cycle_time)
            now = time.time()

            try:
                self._evict_expired_items(now)
            except Exception:
                # log and ignore
                self._logger.error("temporal_entries_evict_failed", exc_info=True)

    def _evict_expired_items(self, now: float) -> list[T]:
        to_remove: list[str] = []

        # first get list of entries to remove in this cycle
        # the dict items are naturally ordered so that older entries
        # come before newer entries
        #
        # thus the identification of entries to remove can break
        # as soon as an item that expires in the future is encountered
        with self._entries_rwlock.gen_rlock():
            for entry_id, entry in self._entries.items():
                expires_at = entry.added + self._grace_period

                if expires_at <= now:
                    to_remove.append(entry_id)
                else:
                    break

        if not len(to_remove):
            return []

        # now go ahead and remove all entries that were identified
        # previously. mind that can happen that a previously identified
        # entry could be removed manually in the meanwhile
        to_evict: list[T] = []
        with self._entries_rwlock.gen_wlock():
            self._logger.debug(
                "temporal_entries_remove",
                collect=len(to_remove),
                out_of=len(self._entries),
            )

            for entry_id in to_remove:
                entry_to_evict = self._entries.pop(entry_id, None)
                if entry_to_evict is None:
                    continue

                to_evict.append(entry_to_evict.value)

        # finally, make the eviction calls
        #
        # this is intentionally done outside the critical section
        for value in to_evict:
            if not self._safe_evict(value):
                self._logger.error("temporal_entries_evict_failed", value=value)

        return to_evict

    def _safe_evict(self, value: T) -> bool:
        try:
            self._entry_evict_fun(value)
            return True
        except Exception:
            return False

    @property
    def entry_timeout(self) -> float:
        """
        :return: timeout for entries; entry is guaranteed to be removed from the container
         after this time
        """
        return self._grace_period + self._collector_cycle_time + 1

    def start_collector(self) -> None:
        assert not self._closed

        if self._thread.is_alive():
            self._thread.start()

    def get_entry(self, entry_id: str) -> Optional[T]:
        """
        :param entry_id: entry identifier
        :return: entry or None if not found
        """
        assert not self._closed

        with self._entries_rwlock.gen_rlock():
            entry = self._entries.get(entry_id)
            if entry is None:
                return None

            return entry.value

    def evict_entry(self, entry_id: str) -> bool:
        """
        Explicitly evicts an entry from the container. This will drop the entry and call
        the eviction function.

        :param entry_id: entry to evict
        :return: true if entry existed and was evicted, false if entry did not exist
        """
        assert not self._closed

        with self._entries_rwlock.gen_wlock():
            entry = self._entries.pop(entry_id, None)
            if entry is None:
                return False

        self._entry_evict_fun(entry.value)
        return True

    def pop_entry(self, entry_id: str) -> Optional[T]:
        """
        Pops an entry out of the container. This will take the entry out and will not
        run the eviction function.

        :param entry_id: id of entry to pop
        :return: None if no entry with the provided id
        """
        assert not self._closed

        with self._entries_rwlock.gen_wlock():
            entry = self._entries.pop(entry_id, None)
            if entry is None:
                return None

            return entry.value

    def close(self) -> None:
        """
        Closes the container. This will evict all entries that are currently in the container
        and halt (eventually) the internal collector thread.

        :return: nothing
        """
        self._closed = True
        with self._entries_rwlock.gen_wlock():
            snapshot = self._entries
            self._entries = {}

        for entry in snapshot.values():
            self._entry_evict_fun(entry.value)

    def __iter__(self) -> Iterator[T]:
        assert not self._closed

        with self._entries_rwlock.gen_rlock():
            value_copy = tuple(entry.value for entry in self._entries.values())

        return value_copy.__iter__()

    def _add_entry(self, key: str, value: T, now: float) -> None:
        """
        Adds entry to the container.

        Note: this method exists to improve testability - so that tests can
        simply 'emulate' time moving forward. It is not intended to be used
        outside the test code: bad use can mess the guarantees provided
        by the container.
        """
        assert not self._closed

        with self._entries_rwlock.gen_wlock():
            self._entries[key] = _Entry(value, now)

    def __setitem__(self, key: str, value: T) -> None:
        self._add_entry(key, value, time.time())

    def __len__(self) -> int:
        with self._entries_rwlock.gen_rlock():
            return len(self._entries)
