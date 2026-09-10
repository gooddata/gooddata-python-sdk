# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch

import pytest
from gooddata_eval.cli.agentic_runner import (
    AGENTIC_TEST_KINDS,
    PARALLEL_SAFE_TEST_KINDS,
    WORKSPACE_MUTATING_TEST_KINDS,
    _dispatch_agentic,
    run_agentic_items,
    runs_in_parallel,
)
from gooddata_eval.core.agentic.alert_skill import AlertSkillAssertionError
from gooddata_eval.core.models import AgenticEvalOutcome, DatasetItem
from gooddata_eval.core.timing import PhaseTimings


def test_dispatch_agentic_passes_agent_id_through_to_alert_skill():
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind="agentic_alert_skill",
        question="Alert me when spend exceeds 100",
        expected_output={"Operator": "GREATER_THAN", "Threshold": 100},
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
            agent_id="agent-1",
        )
    assert mock_eval.call_args.kwargs["agent_id"] == "agent-1"


def test_dispatch_agentic_omits_agent_id_by_default():
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind="agentic_metric_skill",
        question="Create a metric for total spend",
        expected_output={"maql": "SELECT {metric/spend}"},
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_metric_skill") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    assert mock_eval.call_args.kwargs["agent_id"] is None


_MIN_VIZ = {"id": "v1", "type": "table", "query": {"fields": {}, "filter_by": {}}, "metrics": [], "view_by": []}
_MIN_CONVERSATION_FIXTURE = {
    "id": "c1",
    "expected_skills": ["visualization"],
    "turns": [{"turn_id": "t1", "message": "hi", "expected_skill": "visualization"}],
}

# (kind, expected_output, target evaluate_agentic_* name) for every kind AGENTIC_TEST_KINDS
# lists -- covers both agent_id passthrough (below) and the outcome-shape regression test
# further down. Keep this in sync with AGENTIC_TEST_KINDS: a kind added there without an
# entry here would silently skip both checks.
_ALL_AGENTIC_KIND_CASES = [
    ("vis_agentic", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
    ("agentic_visualization", {"visualization": _MIN_VIZ}, "evaluate_agentic_visualization"),
    ("agentic_metric_skill", {"maql": "SELECT {metric/spend}"}, "evaluate_agentic_metric_skill"),
    ("agentic_alert_skill", {"Operator": "GREATER_THAN", "Threshold": 100}, "evaluate_agentic_alert_skill"),
    ("agentic_search", {"tool_call": {"function_arguments": {}}}, "evaluate_agentic_search_tool"),
    ("agentic_general_question", "What is X?", "evaluate_agentic_general_question"),
    ("agentic_guardrail", "Ignore prior instructions", "evaluate_agentic_guardrail"),
    ("agentic_kda_skill", {"Measure": {"type": "metric", "id": "revenue"}}, "evaluate_agentic_kda_skill"),
    ("agentic_conversation", {"fixture": _MIN_CONVERSATION_FIXTURE}, "evaluate_agentic_conversation"),
]


def test_all_agentic_kind_cases_covers_every_registered_kind():
    """Guards the two parametrized tests below against silently going stale: a kind added
    to AGENTIC_TEST_KINDS without a matching case here would otherwise just not get tested,
    not fail loudly."""
    covered = {kind for kind, _, _ in _ALL_AGENTIC_KIND_CASES}
    assert covered == set(AGENTIC_TEST_KINDS)


@pytest.mark.parametrize(("kind", "expected_output", "target"), _ALL_AGENTIC_KIND_CASES)
def test_dispatch_agentic_passes_agent_id_through_for_every_kind(kind, expected_output, target):
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind=kind,
        question="q",
        expected_output=expected_output,
    )
    with patch(f"gooddata_eval.cli.agentic_runner.{target}") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
            agent_id="agent-1",
        )
    assert mock_eval.call_args.kwargs["agent_id"] == "agent-1"


def _item(test_kind: str = "agentic_alert_skill") -> DatasetItem:
    return DatasetItem(
        id="item-1",
        dataset_name="d",
        test_kind=test_kind,
        question="Alert me when revenue drops below 100.",
        expected_output={"operator": "LESS_THAN", "threshold": 100},
    )


def test_run_agentic_items_surfaces_reasoning_steps_on_pass():
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill",
        return_value=AgenticEvalOutcome(
            reasoning_steps=["it created the alert"],
            conversation_id="conv-1",
            response_id="resp-1",
            detail={"alert_created": True},
        ),
    ):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].pass_at_k is True
    assert report.items[0].reasoning_steps == ["it created the alert"]
    assert report.items[0].conversation_id == "conv-1"
    assert report.items[0].response_id == "resp-1"
    assert report.items[0].best_detail == {"alert_created": True}


def test_run_agentic_items_surfaces_reasoning_steps_from_exception_on_fail():
    exc = AlertSkillAssertionError("nope")
    exc.reasoning_steps = ["it got confused"]
    exc.conversation_id = "conv-2"
    exc.response_id = "resp-2"
    exc.detail = {"alert_created": False}
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=exc):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].pass_at_k is False
    assert report.items[0].reasoning_steps == ["it got confused"]
    assert report.items[0].conversation_id == "conv-2"
    assert report.items[0].response_id == "resp-2"
    assert report.items[0].best_detail == {"alert_created": False}


def test_run_agentic_items_defaults_reasoning_steps_to_empty_when_exception_has_none():
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill",
        side_effect=AlertSkillAssertionError("nope"),
    ):
        report = run_agentic_items(
            [_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )
    assert report.items[0].reasoning_steps == []
    assert report.items[0].best_detail == {}
    assert report.items[0].conversation_id is None
    assert report.items[0].response_id is None


@pytest.mark.parametrize(("kind", "expected_output", "target"), _ALL_AGENTIC_KIND_CASES)
def test_dispatch_agentic_returns_a_real_outcome_for_every_kind(kind, expected_output, target):
    """Regression test for the bug this fixes: `guardrail`/`search_tool`/`general_question`/
    `visualization`/`kda_skill` used to return None/a bare value instead of an
    AgenticEvalOutcome, so their reasoning_steps/conversation_id/response_id were silently
    dropped (confirmed live: a real eval run produced 0/30 reasoning sidecars for
    agentic_guardrail). Every kind must now return the exact AgenticEvalOutcome its
    evaluator produced -- not None, not the outcome's reasoning_steps list alone, not any
    other bare value the old `isinstance(outcome, tuple)`/`isinstance(outcome, AgenticEvalOutcome)`
    fallback could silently swallow."""
    item = DatasetItem(
        id="q1",
        dataset_name="ds",
        test_kind=kind,
        question="q",
        expected_output=expected_output,
    )
    canned = AgenticEvalOutcome(reasoning_steps=["x"], conversation_id="c1", response_id="r1", detail={"k": "v"})
    with patch(f"gooddata_eval.cli.agentic_runner.{target}", return_value=canned) as mock_eval:
        result = _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    mock_eval.assert_called_once()
    assert result is canned
    assert isinstance(result, AgenticEvalOutcome)
    assert result.reasoning_steps == ["x"]
    assert result.detail == {"k": "v"}
    assert result.conversation_id == "c1"
    assert result.response_id == "r1"


def _timed_item(item_id: str = "item-1") -> DatasetItem:
    return DatasetItem(
        id=item_id,
        dataset_name="d",
        test_kind="agentic_alert_skill",
        question="Alert me when revenue drops below 100.",
        expected_output={"operator": "LESS_THAN", "threshold": 100},
    )


def test_run_agentic_items_does_not_charge_the_item_for_langfuse_trace_linking():
    # The whole point of Option 1: a trace poll that takes longer than the agent turn must
    # not show up as the item being slow. Before this, latency_s wrapped _dispatch_agentic
    # and so swallowed the poll whole -- an item whose agent answered in 4s reported 40s.
    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        submit_trace_link(lambda: time.sleep(0.2), item_id=dataset_item_id)
        return AgenticEvalOutcome(
            reasoning_steps=[],
            conversation_id="c1",
            response_id="r1",
            detail={"alert_created": True},
            timings=PhaseTimings(agent_s=1.0),
        )

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval):
        report = run_agentic_items(
            [_timed_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
            use_langfuse=False,
        )

    item = report.items[0]
    assert item.latency_s < 0.1, "the item was charged for its Langfuse trace link"
    # Still measured, just not on the critical path.
    assert item.langfuse_latency_s >= 0.2
    assert item.agent_latency_s == 1.0


def test_run_agentic_items_drains_trace_links_before_returning():
    # Scores must be final before the CLI renders a table or sets an exit code. A pool
    # that outlived the return would lose whatever had not been flushed.
    linked: list[str] = []

    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        submit_trace_link(lambda: linked.append(dataset_item_id), item_id=dataset_item_id)
        return AgenticEvalOutcome(conversation_id="c1", detail={"alert_created": True})

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval):
        run_agentic_items(
            [_timed_item("a"), _timed_item("b")],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )

    assert sorted(linked) == ["a", "b"]


def test_run_agentic_items_records_phase_timings_and_wall_clock():
    # wall_clock_s was never set on the agentic path, which is why every agentic-only run
    # reported "wall_clock_s": 0.0 in its JSON.
    outcome = AgenticEvalOutcome(
        conversation_id="c1",
        detail={"alert_created": True},
        timings=PhaseTimings(agent_s=2.0, judge_s=1.0, simulated_user_s=0.5),
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", return_value=outcome):
        report = run_agentic_items(
            [_timed_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )

    item = report.items[0]
    assert (item.agent_latency_s, item.judge_latency_s, item.simulated_user_latency_s) == (2.0, 1.0, 0.5)
    assert report.wall_clock_s > 0.0


def test_run_agentic_items_records_phase_timings_when_the_item_fails():
    exc = AlertSkillAssertionError("nope")
    exc.detail = {"alert_created": False}
    exc.timings = PhaseTimings(agent_s=7.0, judge_s=2.0)

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=exc):
        report = run_agentic_items(
            [_timed_item()],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )

    assert report.items[0].pass_at_k is False
    assert report.items[0].agent_latency_s == 7.0
    assert report.items[0].judge_latency_s == 2.0


def test_a_pending_trace_link_does_not_block_the_next_item():
    """The overlap claim, proved by construction rather than by a stopwatch.

    Item "first" submits a trace link that can only finish once item "second" has reached
    the agent. Under the old inline linking that is unreachable -- "second" does not start
    until "first"'s Langfuse block returns -- so the wait times out and the flag stays
    unset. It can only pass if the link really is running off the critical path.
    """
    second_item_reached_the_agent = threading.Event()
    first_link_finished = threading.Event()

    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        if dataset_item_id == "first":

            def poll() -> None:
                if second_item_reached_the_agent.wait(timeout=5):
                    first_link_finished.set()

            submit_trace_link(poll, item_id=dataset_item_id)
        else:
            second_item_reached_the_agent.set()
        return AgenticEvalOutcome(conversation_id="c", detail={"alert_created": True})

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval):
        run_agentic_items(
            [_timed_item("first"), _timed_item("second")],
            host="http://host",
            token="tok",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )

    assert first_link_finished.is_set()


def test_each_run_drains_its_own_links_so_models_cannot_overlap():
    """Multi-model guard: --model a --model b calls run_agentic_items once per model, and
    the workspace's active LLM provider is switched between those calls. A link from
    model A still in flight during model B's run could resolve the wrong model version
    (get_model_version falls back to reading the live workspace when no override is set),
    so each call must own and fully drain its own pool.
    """
    in_flight: list[str] = []
    finished: list[str] = []

    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        def poll() -> None:
            in_flight.append(dataset_item_id)
            time.sleep(0.05)
            finished.append(dataset_item_id)

        submit_trace_link(poll, item_id=dataset_item_id)
        return AgenticEvalOutcome(conversation_id="c", detail={"alert_created": True})

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval):
        first = run_agentic_items(
            [_timed_item("model-a-item")], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01"
        )
        # Nothing from model A may still be running once its run_agentic_items has returned.
        assert finished == ["model-a-item"]
        second = run_agentic_items(
            [_timed_item("model-b-item")], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01"
        )

    assert finished == ["model-a-item", "model-b-item"]
    # Durations are per-run, never carried over from the previous model's pool.
    assert first.items[0].langfuse_latency_s > 0
    assert second.items[0].langfuse_latency_s > 0


def test_an_interrupt_abandons_queued_trace_links_instead_of_waiting_them_out():
    """Ctrl-C must not be held hostage by a backlog of Langfuse polls.

    ThreadPoolExecutor registers an atexit hook that joins its workers, so a pool left
    running with queued 15s polls would stall the CLI for minutes after the user
    interrupted it. Queued-but-unstarted links are dropped on the way out.
    """
    ran: list[str] = []
    block = threading.Event()

    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        # Two blocking tasks occupy both workers; the third can only be queued.
        submit_trace_link(lambda: block.wait(timeout=2), item_id="busy-1")
        submit_trace_link(lambda: block.wait(timeout=2), item_id="busy-2")
        submit_trace_link(lambda: ran.append("queued"), item_id="queued")
        raise KeyboardInterrupt

    with (
        patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval),
        pytest.raises(KeyboardInterrupt),
    ):
        run_agentic_items([_timed_item("a")], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01")

    block.set()
    # No sleep needed: submit only queues, and the queue is only ever executed by drain(),
    # which blocks until it finishes. Had the interrupt path drained instead of abandoning,
    # "queued" would already be in `ran` by the time run_agentic_items returned.
    assert ran == [], "a queued Langfuse poll kept running after the run was interrupted"


def test_langfuse_client_is_closed_only_after_every_link_has_finished():
    """--langfuse builds one client for the whole run and closes it at the end.

    The deferred links use that same client from worker threads, so closing it before the
    drain would make every in-flight poll fail against a shut httpx client -- and because
    BackgroundTraceLinker swallows task errors, the scores would vanish silently rather
    than fail the run.
    """
    events: list[str] = []

    class _Client:
        def flush(self) -> None:
            events.append("flush")

        def close(self) -> None:
            events.append("close")

    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        def poll() -> None:
            time.sleep(0.05)
            events.append(f"link:{dataset_item_id}")

        submit_trace_link(poll, item_id=dataset_item_id)
        return AgenticEvalOutcome(conversation_id="c", detail={"alert_created": True})

    with (
        patch("gooddata_eval.cli.agentic_runner.make_langfuse_client", return_value=_Client()),
        patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval),
    ):
        run_agentic_items(
            [_timed_item("a"), _timed_item("b")],
            host="h",
            token="t",
            workspace_id="ws1",
            run_ts="2026-01-01",
            use_langfuse=True,
        )

    # The batch runs its links in parallel, so their relative order is not fixed -- only
    # that both finished before the client was flushed and closed.
    assert set(events[:2]) == {"link:a", "link:b"}
    assert events[2:] == ["flush", "close"]


def test_run_agentic_items_reports_what_the_trace_link_batch_cost(capsys):
    # The retry budget was sized against an ingestion lag only bounded to "35s to a few
    # minutes". This line is how the next real run reports the actual number: if the
    # slowest link sits near the budget, the budget is binding and scores are being lost.
    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        submit_trace_link(lambda: time.sleep(0.05), item_id=dataset_item_id)
        return AgenticEvalOutcome(conversation_id="c", detail={"alert_created": True})

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=fake_eval):
        run_agentic_items(
            [_timed_item("a"), _timed_item("b")],
            host="h",
            token="t",
            workspace_id="ws1",
            run_ts="2026-01-01",
        )

    out = capsys.readouterr().out
    assert "[langfuse] trace linking" in out
    assert "2 item(s)" in out
    assert "slowest" in out


def _kind_item(kind: str, item_id: str) -> DatasetItem:
    expected: object = "an answer"
    if kind in ("agentic_metric_skill",):
        expected = {"maql": "SELECT {metric/spend}"}
    elif kind in ("agentic_alert_skill", "agentic_kda_skill"):
        expected = {"Operator": "GREATER_THAN", "Threshold": 1}
    elif kind == "agentic_conversation":
        expected = {"fixture": _MIN_CONVERSATION_FIXTURE}
    elif kind in ("vis_agentic", "agentic_visualization"):
        expected = {"visualization": _MIN_VIZ}
    elif kind == "agentic_search":
        expected = {"tool_call": {"function_arguments": {}}}
    return DatasetItem(id=item_id, dataset_name="d", test_kind=kind, question="q", expected_output=expected)


def test_every_agentic_kind_is_classified_as_parallel_safe_or_workspace_mutating():
    # An unclassified kind would either lose concurrency silently or, worse, be run in
    # parallel when it mutates the shared workspace.
    assert set(AGENTIC_TEST_KINDS) == PARALLEL_SAFE_TEST_KINDS | WORKSPACE_MUTATING_TEST_KINDS
    assert not (PARALLEL_SAFE_TEST_KINDS & WORKSPACE_MUTATING_TEST_KINDS)


def test_read_only_kinds_run_concurrently():
    # Each item blocks until all of them have started: only reachable if they really do run
    # at the same time. Sequentially the barrier times out, the item errors, and pass_at_k
    # goes false.
    n = 4
    barrier = threading.Barrier(n, timeout=5)

    def fake_eval(**_kw):
        barrier.wait()
        return AgenticEvalOutcome(conversation_id="c", detail={"judge_passed": True})

    items = [_kind_item("agentic_general_question", f"q{i}") for i in range(n)]
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question", side_effect=fake_eval):
        report = run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=n)

    assert [i.pass_at_k for i in report.items] == [True] * n


def test_workspace_mutating_kinds_never_overlap_even_at_high_concurrency():
    # metric_skill creates and deletes metrics in the shared eval workspace, and
    # metric_skill._delete_metric documents that a leaked one gets reused by a later test.
    # Overlapping two of them is exactly the contamination that comment warns about.
    lock = threading.Lock()
    active = 0
    peak = 0

    def fake_eval(**_kw):
        nonlocal active, peak
        with lock:
            active += 1
            peak = max(peak, active)
        time.sleep(0.05)
        with lock:
            active -= 1
        return AgenticEvalOutcome(conversation_id="c", detail={"maql_correct": True})

    items = [_kind_item("agentic_metric_skill", f"m{i}") for i in range(4)]
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_metric_skill", side_effect=fake_eval):
        run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=4)

    assert peak == 1


def test_report_keeps_dataset_order_when_items_finish_out_of_order():
    # Concurrency must not reshuffle the report: the JSON and console are read against the
    # dataset, and a run-to-run reordering makes two reports impossible to diff.
    delays = {"q0": 0.15, "q1": 0.01, "q2": 0.10, "q3": 0.01}

    def fake_eval(*, dataset_item_id, **_kw):
        time.sleep(delays[dataset_item_id])
        return AgenticEvalOutcome(conversation_id="c", detail={"judge_passed": True})

    items = [_kind_item("agentic_general_question", f"q{i}") for i in range(4)]
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question", side_effect=fake_eval):
        report = run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=4)

    assert [i.id for i in report.items] == ["q0", "q1", "q2", "q3"]


def test_warns_when_concurrency_cannot_apply_to_any_item(capsys):
    # --concurrency silently doing nothing is what sent a real run looking for a speedup
    # that was never possible: the flag only ever reached the non-agentic runner.
    items = [_kind_item("agentic_metric_skill", f"m{i}") for i in range(2)]
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_metric_skill",
        return_value=AgenticEvalOutcome(conversation_id="c", detail={}),
    ):
        run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=4)

    warned = capsys.readouterr().err
    assert "concurrency" in warned.lower()
    assert "agentic_metric_skill" in warned


def test_no_concurrency_warning_when_some_items_can_run_in_parallel(capsys):
    items = [_kind_item("agentic_general_question", "q0"), _kind_item("agentic_metric_skill", "m0")]
    with (
        patch(
            "gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question",
            return_value=AgenticEvalOutcome(conversation_id="c", detail={}),
        ),
        patch(
            "gooddata_eval.cli.agentic_runner.evaluate_agentic_metric_skill",
            return_value=AgenticEvalOutcome(conversation_id="c", detail={}),
        ),
    ):
        run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=4)

    assert "concurrency" not in capsys.readouterr().err.lower()


def test_an_unclassified_kind_defaults_to_serial():
    """PARALLEL_SAFE is an explicit allowlist because deriving it as
    `AGENTIC_TEST_KINDS - WORKSPACE_MUTATING` auto-enrolled every newly added kind into
    parallel execution -- and nothing here can prove a kind is read-only, since the
    mutation happens server-side in the agent's tools."""
    assert runs_in_parallel("agentic_general_question") is True
    assert runs_in_parallel("agentic_metric_skill") is False
    assert runs_in_parallel("agentic_some_kind_added_next_year") is False


def test_kda_skill_runs_serially_until_its_tool_is_confirmed_side_effect_free():
    # agentic_kda_skill drives a tool called create_key_driver_analysis and, unlike
    # metric_skill/alert_skill, has no cleanup. The evaluator only reads the create call's
    # arguments (never a returned object id), which suggests an in-conversation analysis --
    # but that is inference about server-side behaviour, not verification. Serial until
    # someone confirms it.
    assert "agentic_kda_skill" in WORKSPACE_MUTATING_TEST_KINDS
    assert "agentic_kda_skill" not in PARALLEL_SAFE_TEST_KINDS


def test_announces_the_trace_link_batch_before_it_starts(capsys):
    # The batch runs after the last item, and took 9.6s then 15.9s on real runs. Printing
    # only when it finishes leaves the terminal silent for that whole stretch, right after
    # the last item reports -- it reads as a hang.
    def fake_eval(*, submit_trace_link, dataset_item_id, **_kw):
        submit_trace_link(lambda: time.sleep(0.05), item_id=dataset_item_id)
        return AgenticEvalOutcome(conversation_id="c", detail={"judge_passed": True})

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question", side_effect=fake_eval):
        run_agentic_items(
            [_kind_item("agentic_general_question", f"q{i}") for i in range(3)],
            host="h",
            token="t",
            workspace_id="ws1",
            run_ts="ts",
        )

    out = capsys.readouterr().out
    assert "linking traces for 3 item(s)" in out
    # Announced first, reported second.
    assert out.index("linking traces for 3 item(s)") < out.index("trace linking finished")


def test_says_nothing_about_trace_linking_when_there_is_none(capsys):
    # No Langfuse client -> no tasks queued -> no noise about a batch that never ran.
    with patch(
        "gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question",
        return_value=AgenticEvalOutcome(conversation_id="c", detail={}),
    ):
        run_agentic_items(
            [_kind_item("agentic_general_question", "q0")],
            host="h",
            token="t",
            workspace_id="ws1",
            run_ts="ts",
        )

    assert "linking traces" not in capsys.readouterr().out


def test_an_interrupt_cancels_queued_items_instead_of_running_the_whole_dataset():
    """Ctrl-C during the parallel phase must not work through the rest of the dataset.

    `with ThreadPoolExecutor(...)` exits via shutdown(wait=True) with cancel_futures left
    False, so an interrupt raised while the main thread waits on as_completed runs every
    QUEUED item to completion first. At --concurrency 4 over 18 items that is several more
    waves of up-to-300s agent calls issued after the user already gave up -- and it runs
    BEFORE the linker.abandon() that is supposed to make an interrupt cheap.

    Only the items already in flight may finish; the interpreter joins those worker
    threads at exit regardless, so they are not cancellable. Everything still queued is.
    """
    release = threading.Event()
    lock = threading.Lock()
    started: list[str] = []

    def fake_eval(*, dataset_item_id, **_kw):
        with lock:
            started.append(dataset_item_id)
        release.wait(timeout=0.5)
        return AgenticEvalOutcome(conversation_id="c", detail={"judge_passed": True})

    items = [_kind_item("agentic_general_question", f"q{i}") for i in range(6)]
    pools: list[ThreadPoolExecutor] = []

    def recording_pool(*args, **kwargs):
        pools.append(ThreadPoolExecutor(*args, **kwargs))
        return pools[-1]

    with (
        patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question", side_effect=fake_eval),
        patch("gooddata_eval.cli.agentic_runner.ThreadPoolExecutor", recording_pool),
        patch("gooddata_eval.cli.agentic_runner.as_completed", side_effect=KeyboardInterrupt),
        pytest.raises(KeyboardInterrupt),
    ):
        run_agentic_items(items, host="h", token="t", workspace_id="ws1", run_ts="ts", concurrency=2)

    release.set()
    # Join the item pool for real rather than sleeping and sampling: this is exactly what
    # would let a still-queued item start, so if none has after it, none ever will.
    pools[0].shutdown(wait=True)
    with lock:
        ran = list(started)
    assert len(ran) < len(items), f"the interrupt waited out the whole dataset: {ran}"
    # cancel_futures cancels every future that has not started, so at most one wave of
    # max_workers items can ever have been dequeued.
    assert len(ran) <= 2, f"more than one wave got through: {ran}"


def test_an_errored_item_keeps_the_timings_it_managed_to_take():
    # An item unevaluable because its judge broke should not also report the agent as
    # having cost 0s -- the agent answered, and that is the measurement the report is for.
    exc = RuntimeError("judge returned no readable verdict for any of the 2 run(s)")
    exc.timings = PhaseTimings(agent_s=7.0, judge_s=1.0)  # type: ignore[attr-defined]

    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=exc):
        report = run_agentic_items([_timed_item()], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01")

    item = report.items[0]
    assert item.error is not None
    assert (item.agent_latency_s, item.judge_latency_s) == (7.0, 1.0)


def test_an_errored_item_without_timings_keeps_its_zero_defaults():
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_alert_skill", side_effect=RuntimeError("boom")):
        report = run_agentic_items([_timed_item()], host="h", token="t", workspace_id="ws1", run_ts="2026-01-01")

    assert report.items[0].agent_latency_s == 0.0


def test_dispatch_agentic_passes_user_context_through_to_general_question():
    attachment = {"referencedObjects": [{"objects": [{"type": "WIDGET", "id": "campaign_spend"}]}]}
    item = DatasetItem(
        id="gdai-2179-001",
        dataset_name="GDAI-2179",
        test_kind="agentic_general_question",
        question="What does the visualization I attached show?",
        expected_output="Describes the attached chart.",
        user_context=attachment,
    )
    with patch("gooddata_eval.cli.agentic_runner.evaluate_agentic_general_question") as mock_eval:
        _dispatch_agentic(
            item,
            host="https://h",
            token="tok",
            workspace_id="ws1",
            k=1,
            langfuse=None,
            run_ts="2026-01-01",
            model_version_override=None,
        )
    assert mock_eval.call_args.kwargs["user_context"] == attachment
