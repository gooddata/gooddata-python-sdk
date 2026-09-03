# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""Tests for the background Langfuse trace-linking pool."""

import ast
import importlib
import inspect
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.cli import agentic_runner
from gooddata_eval.core.agentic import _langfuse, _trace_linker
from gooddata_eval.core.agentic._trace_linker import (
    BackgroundTraceLinker,
    run_trace_link_inline,
    warn_from_worker,
)


def test_submit_returns_before_the_task_completes():
    # The whole point: an item must not sit waiting on its own Langfuse poll. `submit`
    # hands the work off and returns, so the next item's agent call starts immediately.
    release = threading.Event()
    completed = threading.Event()

    def task() -> None:
        release.wait(timeout=5)
        completed.set()

    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(task, item_id="item-1")

    assert not completed.is_set()  # submit did not block on the task

    release.set()
    linker.drain()
    assert completed.is_set()


def test_drain_waits_for_every_submitted_task():
    # Scores must be final before the CLI prints its table or sets an exit code, so the
    # runner drains rather than letting the pool die with the process.
    done: list[int] = []
    linker = BackgroundTraceLinker(max_workers=2)

    for i in range(5):
        linker.submit(lambda i=i: done.append(i), item_id=f"item-{i}")
    linker.drain()

    assert sorted(done) == [0, 1, 2, 3, 4]


def test_a_failing_task_neither_propagates_nor_stops_the_others():
    # Existing invariant across every Langfuse writer in this package: a Langfuse failure
    # warns, it never aborts the eval run. Backgrounding the work must not change that --
    # and an exception swallowed inside a worker must not strand the remaining tasks.
    done: list[str] = []

    def boom() -> None:
        raise RuntimeError("langfuse down")

    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(boom, item_id="bad")
    linker.submit(lambda: done.append("good"), item_id="ok")
    linker.drain()  # must not raise

    assert done == ["good"]


def test_records_each_task_duration_under_its_item_id():
    # Per-item Langfuse cost stays observable even though it is off the critical path --
    # that is the "independently measurable" half of the goal, as distinct from "faster".
    clock = iter([10.0, 12.5]).__next__
    linker = BackgroundTraceLinker(max_workers=1, clock=clock)

    linker.submit(lambda: None, item_id="item-1")
    linker.drain()

    assert linker.durations == {"item-1": 2.5}


def test_duration_is_recorded_even_when_the_task_fails():
    # A poll that exhausts its retries and then fails to score is exactly the case whose
    # cost we most want on the report; losing the timing there would hide the worst items.
    def boom() -> None:
        raise RuntimeError("langfuse down")

    linker = BackgroundTraceLinker(max_workers=1, clock=iter([1.0, 4.0]).__next__)
    linker.submit(boom, item_id="item-1")
    linker.drain()

    assert linker.durations == {"item-1": 3.0}


def test_run_trace_link_inline_runs_the_task_on_the_calling_thread():
    # The default every evaluate_agentic_* keeps when no linker is injected, so direct
    # callers (and every existing test) see today's synchronous behavior unchanged.
    caller = threading.current_thread()
    ran_on: list[threading.Thread] = []

    run_trace_link_inline(lambda: ran_on.append(threading.current_thread()))

    assert ran_on == [caller]


# Every agentic kind reachable from cli.agentic_runner._dispatch_agentic. Kept as an
# explicit list, with the staleness guard below, so a kind added later cannot quietly
# skip the linker and go back to blocking its item on a Langfuse poll.
_EVALUATE_FUNCS = [
    ("general_question", "evaluate_agentic_general_question"),
    ("guardrail", "evaluate_agentic_guardrail"),
    ("metric_skill", "evaluate_agentic_metric_skill"),
    ("alert_skill", "evaluate_agentic_alert_skill"),
    ("search_tool", "evaluate_agentic_search_tool"),
    ("visualization", "evaluate_agentic_visualization"),
    ("kda_skill", "evaluate_agentic_kda_skill"),
    ("conversation", "evaluate_agentic_conversation"),
]


def test_evaluate_funcs_covers_every_function_dispatch_can_call():
    dispatched = {n for n in dir(agentic_runner) if n.startswith("evaluate_agentic_")}
    assert {name for _, name in _EVALUATE_FUNCS} == dispatched


@pytest.mark.parametrize(("module_name", "func_name"), _EVALUATE_FUNCS)
def test_every_evaluate_agentic_takes_a_trace_linker_defaulting_to_inline(module_name, func_name):
    module = importlib.import_module(f"gooddata_eval.core.agentic.{module_name}")
    param = inspect.signature(getattr(module, func_name)).parameters.get("submit_trace_link")

    assert param is not None, f"{func_name} still blocks its item on Langfuse trace linking"
    # Defaulting to inline is what keeps direct callers behaviour-compatible.
    assert param.default is run_trace_link_inline


def _callee_name(call: ast.Call) -> str:
    """Trailing name of a call target: `now` for both `now(...)` and `_dt.now(...)`."""
    if isinstance(call.func, ast.Attribute):
        return call.func.attr
    if isinstance(call.func, ast.Name):
        return call.func.id
    return ""


def _deferred_blocks(module_name: str) -> list[ast.FunctionDef]:
    """The kind's scoring closure -- the part that runs on the linker's thread, not the item's."""
    module = importlib.import_module(f"gooddata_eval.core.agentic.{module_name}")
    tree = ast.parse(inspect.getsource(module))
    return [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_write_scores"]


def _clock_reads(node: ast.AST) -> list[ast.Call]:
    return [
        n
        for n in ast.walk(node)
        if isinstance(n, ast.Call) and _callee_name(n) in ("now", "utcnow", "utc_now", "monotonic")
    ]


@pytest.mark.parametrize(("module_name", "_func_name"), _EVALUATE_FUNCS)
def test_every_kind_hands_a_pinned_window_to_the_linker(module_name, _func_name):
    """The query window must be captured on the calling thread, not inside the deferred task.

    Checked structurally because the failure is silent: a kind that reads the clock once its
    task is already running still works, it just queries a window that widened by however
    long the task sat in the pool. Nothing fails loudly, the scores just go missing.
    """
    module = importlib.import_module(f"gooddata_eval.core.agentic.{module_name}")
    tree = ast.parse(inspect.getsource(module))

    submits = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and _callee_name(n) == "submit_trace_scoring"]
    assert submits, f"{module_name} no longer defers its Langfuse block to the linker"
    for call in submits:
        assert any(kw.arg == "window_end" for kw in call.keywords), (
            f"{module_name} leaves window_end to drift to the task's run time"
        )

    blocks = _deferred_blocks(module_name)
    assert blocks, f"{module_name} has no deferred _write_scores block"
    for block in blocks:
        assert not _clock_reads(block), (
            f"{module_name}'s _write_scores reads the clock itself, so anything it derives from "
            f"that widens with however long the task waited in the pool"
        )


@pytest.mark.parametrize(("module_name", "_func_name"), _EVALUATE_FUNCS)
def test_every_kind_captures_the_window_before_deferring(module_name, _func_name):
    # The other half: window_end must actually be a captured timestamp. Passing a name that
    # nothing ever assigns would satisfy the check above while sending None to the query.
    module = importlib.import_module(f"gooddata_eval.core.agentic.{module_name}")
    tree = ast.parse(inspect.getsource(module))
    blocks = _deferred_blocks(module_name)
    assert blocks, f"{module_name} has no deferred _write_scores block"
    inside = {id(n) for block in blocks for n in ast.walk(block)}

    pins = [
        n
        for n in ast.walk(tree)
        if isinstance(n, ast.Assign)
        and id(n) not in inside
        and any(isinstance(t, ast.Name) and t.id == "window_end" for t in n.targets)
        and isinstance(n.value, ast.Call)
        and _callee_name(n.value) in ("now", "utcnow", "utc_now")
    ]
    assert pins, f"{module_name} never captures window_end from the clock outside _write_scores"


def test_the_linker_polls_the_window_it_was_given_instead_of_reading_the_clock():
    """The single place the deferred poll is now issued, so this invariant lives here once.

    Every kind pins its own window (above) and hands it over; if ``submit_trace_scoring``
    then re-read the clock, all eight would silently widen again.
    """
    tree = ast.parse(inspect.getsource(_trace_linker))
    blocks = [n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "_link_traces"]
    assert blocks, "submit_trace_scoring no longer defers the trace lookup"

    for block in blocks:
        assert not _clock_reads(block), "the deferred lookup reads the clock instead of the pinned window"
        lookups = [
            n for n in ast.walk(block) if isinstance(n, ast.Call) and _callee_name(n) == "find_traces_per_conversation"
        ]
        assert lookups, "the deferred task does not look up traces at all"
        for call in lookups:
            assert len(call.args) >= 4 or any(kw.arg == "window_end" for kw in call.keywords), (
                "the deferred lookup drops window_end, so its query window drifts to run time"
            )


def test_warn_from_worker_emits_each_message_as_a_single_write():
    # print() writes the text and the newline separately. Trace-link warnings now come
    # from worker threads while the main thread is printing per-item progress, so two
    # writes can interleave and split a progress line in half. One write cannot.
    writes: list[str] = []

    class _Stream:
        def write(self, s: str) -> None:
            writes.append(s)

        def flush(self) -> None:
            pass

    with patch("sys.stdout", _Stream()):
        warn_from_worker("[langfuse] WARNING: no trace found for conversation abc")

    assert writes == ["[langfuse] WARNING: no trace found for conversation abc\n"]


def test_submitted_links_do_not_run_until_drain():
    # Batched deliberately. A poll fired immediately after its own conversation is the one
    # most likely to miss, because Langfuse ingestion lag (35s to minutes on us.cloud) has
    # barely started. Holding the whole queue until the agent phase is over gives every
    # trace the length of the run to be ingested, so early items hit on their first attempt
    # instead of burning their retry budget.
    ran: list[str] = []
    linker = BackgroundTraceLinker()

    linker.submit(lambda: ran.append("a"), item_id="a")
    assert linker.pending == 1, "the link did not stay queued for the batch"
    assert ran == [], "the link started on submit instead of waiting for the batch"

    linker.drain()
    assert ran == ["a"]


def test_drain_runs_the_whole_queue_in_parallel():
    # Every queued link blocks until all of them have started, which only completes if the
    # pool is wide enough to run them together. One trace poll is almost entirely waiting,
    # so running them one at a time would multiply the run's tail by the item count.
    n = 12
    barrier = threading.Barrier(n, timeout=5)
    ok: list[int] = []
    linker = BackgroundTraceLinker()

    for i in range(n):
        linker.submit(lambda: (barrier.wait(), ok.append(1)), item_id=f"item-{i}")
    linker.drain()

    assert len(ok) == n


def test_an_interrupt_mid_drain_cancels_the_polls_that_have_not_started():
    """The drain pool needs the same cancellation the item pool got.

    A trace poll is almost entirely time.sleep, so a `with ThreadPoolExecutor` here means
    an interrupt arriving mid-batch waits out ceil(N/_MAX_WORKERS) x _LINK_BUDGET_SEC of
    pure retry sleeping before it surfaces. abandon() cannot help: drain() has already
    moved the queue into a local by then, so the cancellation has to be on the pool.

    The interrupt has to land in the thread that is WAITING on the batch, which is where a
    real Ctrl-C lands, so it is injected into shutdown(wait=True) rather than into a task.
    """
    release = threading.Event()
    lock = threading.Lock()
    started: list[str] = []
    shutdowns: list[dict] = []
    pools: list[ThreadPoolExecutor] = []
    real_shutdown = ThreadPoolExecutor.shutdown

    def fake_shutdown(self, wait=True, *, cancel_futures=False):
        pools.append(self)
        shutdowns.append({"wait": wait, "cancel_futures": cancel_futures})
        if len(shutdowns) == 1:
            raise KeyboardInterrupt
        return real_shutdown(self, wait=wait, cancel_futures=cancel_futures)

    def poll(item_id: str) -> None:
        with lock:
            started.append(item_id)
        release.wait(timeout=0.5)

    linker = BackgroundTraceLinker(max_workers=2)
    for i in range(6):
        linker.submit(lambda i=i: poll(f"item-{i}"), item_id=f"item-{i}")

    with patch.object(ThreadPoolExecutor, "shutdown", fake_shutdown), pytest.raises(KeyboardInterrupt):
        linker.drain()

    # The interrupt must be answered with a cancelling shutdown, not swallowed or re-waited.
    assert len(shutdowns) == 2, f"the interrupt was not answered with a second shutdown: {shutdowns}"
    assert shutdowns[1] == {"wait": False, "cancel_futures": True}

    release.set()
    # Join the pool for real rather than sleeping and sampling: this is precisely what would
    # let a still-queued poll start, so if none has after it, none ever will.
    real_shutdown(pools[0], wait=True)
    with lock:
        ran = list(started)
    assert len(ran) <= 2, f"a queued poll ran after the drain was interrupted: {ran}"


def test_drain_still_waits_for_the_whole_batch_when_nothing_interrupts_it():
    # The cancellation path must not have made the normal path lossy: scores still have to
    # be final before the runner reports.
    done: list[int] = []
    linker = BackgroundTraceLinker(max_workers=3)
    for i in range(9):
        linker.submit(lambda i=i: done.append(i), item_id=f"item-{i}")

    linker.drain()

    assert sorted(done) == list(range(9))


def test_abandon_drops_the_queue_so_a_later_drain_runs_nothing():
    """Direct coverage of abandon(), which had none.

    The interrupt test below reaches abandon() only via a path where drain() is never
    called, so `ran == []` holds there whether abandon works or not -- replacing its body
    with `pass` left the whole suite green. This fails immediately if it stops clearing.
    """
    ran: list[str] = []
    linker = BackgroundTraceLinker()
    linker.submit(lambda: ran.append("a"), item_id="a")
    linker.submit(lambda: ran.append("b"), item_id="b")
    assert linker.pending == 2

    linker.abandon()

    assert linker.pending == 0, "abandon() left the queue in place"
    linker.drain()  # nothing should be left for it to run
    assert ran == [], "a task survived abandon() and ran on the next drain"


def test_abandon_on_an_empty_queue_is_harmless():
    linker = BackgroundTraceLinker()
    linker.abandon()
    linker.abandon()
    assert linker.pending == 0


def test_no_cancellation_signal_exists_outside_a_drain():
    """Scoped to one batch on purpose.

    A module-level Event left permanently in place would let one run's Ctrl-C stop the next
    --model pass's polls before they started.
    """
    assert _trace_linker.link_cancel_event() is None

    seen: list[object] = []
    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(lambda: seen.append(_trace_linker.link_cancel_event()), item_id="a")
    linker.drain()

    assert seen and seen[0] is not None, "a running poll cannot be told to stop"
    assert not seen[0].is_set(), "an uninterrupted drain must not look cancelled"
    assert _trace_linker.link_cancel_event() is None, "the signal outlived its drain"


def test_an_interrupt_signals_cancellation_before_it_shuts_the_pool_down():
    """Order matters: cancel_futures only drops what has not started.

    A poll already running sits in find_traces_per_conversation's backoff, and the
    interpreter joins executor workers at exit -- so without this signal a Ctrl-C waits out
    the rest of the batch budget (measured: 110s, against 0.5s with it).
    """
    events: list[str] = []
    started = threading.Event()
    release = threading.Event()
    seen: list[threading.Event | None] = []
    real_shutdown = ThreadPoolExecutor.shutdown

    def poll() -> None:
        # The signal is visible on the worker's own thread, so the worker reports it.
        seen.append(_trace_linker.link_cancel_event())
        started.set()
        release.wait(timeout=5)

    def fake_shutdown(self, wait=True, *, cancel_futures=False):
        assert started.wait(timeout=5), "the poll never started"
        cancel = seen[0]
        events.append(
            f"shutdown(wait={wait},cancel_futures={cancel_futures},signalled={cancel is not None and cancel.is_set()})"
        )
        if wait:
            raise KeyboardInterrupt
        return real_shutdown(self, wait=wait, cancel_futures=cancel_futures)

    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(poll, item_id="a")
    try:
        with patch.object(ThreadPoolExecutor, "shutdown", fake_shutdown), pytest.raises(KeyboardInterrupt):
            linker.drain()
    finally:
        release.set()

    assert events == [
        "shutdown(wait=True,cancel_futures=False,signalled=False)",
        "shutdown(wait=False,cancel_futures=True,signalled=True)",
    ], events


def test_a_cancelled_poll_stops_instead_of_finishing_its_retry_ladder():
    """The behaviour the signal buys, measured in sleep rather than wall time."""
    slept: list[float] = []

    class _Clock:
        now = 1000.0

        def monotonic(self):
            return self.now

        def sleep(self, seconds):
            slept.append(seconds)
            self.now += seconds

    cancelled = threading.Event()
    cancelled.set()
    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[]),
        patch("gooddata_eval.core.agentic._langfuse.time", _Clock()),
        patch("gooddata_eval.core.agentic._langfuse.link_cancel_event", return_value=cancelled),
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker"),
    ):
        result = _langfuse.find_traces_per_conversation(MagicMock(), ["c1", "c2"], datetime.now(timezone.utc))

    assert sum(slept) == 0.0, f"a cancelled poll kept sleeping: {slept}"
    # Every conversation still reports, so callers see None rather than a missing key.
    assert set(result) == {"c1", "c2"}


def test_cancelling_mid_backoff_stops_the_poll_without_finishing_the_sleep():
    """The sliced wait itself, not the check at the top of the conversation loop.

    A poll that is already asleep is the case that hung: cancel_futures cannot touch it and
    the interpreter joins the worker at exit. Measured end to end, this was 110s before the
    wait was served in slices and 0.5s after -- so the test pins the mechanism, by cancelling
    only once the poll is already sleeping.
    """
    cancelled = threading.Event()
    slept: list[float] = []

    class _Clock:
        now = 1000.0

        def monotonic(self):
            return self.now

        def sleep(self, seconds):
            slept.append(seconds)
            self.now += seconds
            cancelled.set()  # the interrupt lands while this poll is mid-backoff

    with (
        patch("gooddata_eval.core.agentic._langfuse._fetch_traces_for_session", return_value=[]),
        patch("gooddata_eval.core.agentic._langfuse.time", _Clock()),
        patch("gooddata_eval.core.agentic._langfuse.link_cancel_event", return_value=cancelled),
        patch("gooddata_eval.core.agentic._langfuse.warn_from_worker"),
    ):
        _langfuse.find_traces_per_conversation(MagicMock(), ["c1"], datetime.now(timezone.utc))

    # One slice, then it noticed. Without slicing it would sleep the whole backoff ladder up
    # to _LINK_BUDGET_SEC before looking at the flag again.
    assert slept == [_langfuse._CANCEL_CHECK_SEC], slept


def test_an_interrupted_drain_leaves_the_cancellation_visible_to_late_workers():
    """shutdown(wait=False) returns before the workers notice.

    A worker that reaches its next wait only after drain() has already raised must still
    read a SET event, or it goes back to an uninterruptible sleep for the rest of its budget.
    The signal lives on the worker's own thread, so nothing is left behind on the caller's:
    the next drain starts clean.
    """
    started = threading.Event()
    release = threading.Event()
    done = threading.Event()
    late: list[bool] = []
    real_shutdown = ThreadPoolExecutor.shutdown

    def poll() -> None:
        started.set()
        release.wait(timeout=5)  # still running when drain() raises
        cancel = _trace_linker.link_cancel_event()
        late.append(cancel is not None and cancel.is_set())
        done.set()

    def fake_shutdown(self, wait=True, *, cancel_futures=False):
        if wait:
            assert started.wait(timeout=5), "the poll never started"
            raise KeyboardInterrupt
        return real_shutdown(self, wait=wait, cancel_futures=cancel_futures)

    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(poll, item_id="a")
    with patch.object(ThreadPoolExecutor, "shutdown", fake_shutdown), pytest.raises(KeyboardInterrupt):
        linker.drain()

    assert _trace_linker.link_cancel_event() is None, "the interrupt leaked onto the calling thread"
    release.set()
    assert done.wait(timeout=5), "the late worker never finished"
    assert late == [True], "a late worker stopped seeing the interrupt"

    # And the next drain is unaffected by it.
    fresh: list[bool] = []
    second = BackgroundTraceLinker(max_workers=1)
    second.submit(lambda: fresh.append(_trace_linker.link_cancel_event().is_set()), item_id="b")
    second.drain()
    assert fresh == [False], "the previous run's interrupt leaked into this drain"
    assert _trace_linker.link_cancel_event() is None


def test_an_interrupted_drain_does_not_cancel_a_later_inline_link():
    """A caller that survives the interrupt -- the test suite, or a library user catching
    KeyboardInterrupt -- must still be able to link inline afterwards. Kept in a module
    global, the set event was read by run_trace_link_inline, and
    find_traces_per_conversation broke before its first fetch, orphaning every score.
    """
    real_shutdown = ThreadPoolExecutor.shutdown

    def fake_shutdown(self, wait=True, *, cancel_futures=False):
        if wait:
            raise KeyboardInterrupt
        return real_shutdown(self, wait=wait, cancel_futures=cancel_futures)

    linker = BackgroundTraceLinker(max_workers=1)
    linker.submit(lambda: None, item_id="a")
    with patch.object(ThreadPoolExecutor, "shutdown", fake_shutdown), pytest.raises(KeyboardInterrupt):
        linker.drain()

    seen: list[threading.Event | None] = []
    run_trace_link_inline(lambda: seen.append(_trace_linker.link_cancel_event()))

    assert seen == [None], "an inline link inherited the interrupted drain's cancellation"
