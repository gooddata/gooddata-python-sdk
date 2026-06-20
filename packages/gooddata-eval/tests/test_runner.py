# (C) 2026 GoodData Corporation
import threading
from pathlib import Path
from unittest.mock import patch

from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.evaluators import supported_test_kinds
from gooddata_eval.core.evaluators.summary import _VIOLATION_STEPS
from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.runner import ItemReport, run_items


def _viz_obj():
    return {
        "id": "x",
        "type": "column_chart",
        "query": {
            "fields": {"m_rev": {"using": "metric/revenue"}, "d_q": {"using": "label/date.quarter"}},
            "filter_by": {},
        },
        "metrics": ["m_rev"],
        "view_by": ["d_q"],
    }


def _item():
    return DatasetItem(
        id="i1",
        dataset_name="d",
        test_kind="visualization",
        question="Show revenue by quarter",
        expected_output={"visualization": _viz_obj()},
    )


class _FakeBackend:
    def __init__(self, results):
        self._results = results
        self.calls = 0

    def ask(self, item: DatasetItem) -> ChatResult:
        r = self._results[min(self.calls, len(self._results) - 1)]
        self.calls += 1
        return r


def _chat_with(viz_obj) -> ChatResult:
    return ChatResult.model_validate({"createdVisualizations": {"objects": [viz_obj], "reasoning": ""}})


def _empty_chat() -> ChatResult:
    return ChatResult.model_validate({"textResponse": "which metric?"})


def test_run_items_pass_at_k_true_if_any_run_passes():
    backend = _FakeBackend([_empty_chat(), _chat_with(_viz_obj())])  # run0 fails, run1 passes
    report = run_items([_item()], backend, runs=2)
    assert report.total == 1
    assert report.passed == 1
    assert report.items[0].pass_at_k is True
    assert backend.calls == 2


def test_run_items_marks_unsupported_test_kind_skipped():
    item = DatasetItem(id="s1", dataset_name="d", test_kind="unknown_kind", question="q", expected_output={})
    backend = _FakeBackend([_empty_chat()])
    report = run_items([item], backend, runs=1)
    assert report.skipped == 1
    assert report.items[0].skipped is True
    assert backend.calls == 0


def test_run_items_records_agent_error_without_passing():
    class _BoomBackend:
        def ask(self, item: DatasetItem) -> ChatResult:
            raise RuntimeError("network down")

    report = run_items([_item()], _BoomBackend(), runs=1)
    assert report.errored == 1
    assert report.items[0].pass_at_k is False
    assert "network down" in report.items[0].error


def test_run_items_invokes_progress_callbacks():
    backend = _FakeBackend([_chat_with(_viz_obj())])
    starts: list[tuple] = []
    dones: list[tuple] = []
    report = run_items(
        [_item()],
        backend,
        runs=1,
        on_item_start=lambda i, n, item: starts.append((i, n, item.id)),
        on_item_done=lambda i, n, r: dones.append((i, n, r.id, r.pass_at_k)),
    )
    assert report.total == 1
    assert starts == [(1, 1, "i1")]
    assert dones == [(1, 1, "i1", True)]


def test_run_items_reports_latency_and_per_run_callback():
    backend = _FakeBackend([_empty_chat(), _chat_with(_viz_obj())])  # run0 fail, run1 pass
    runs_seen: list[tuple] = []
    report = run_items(
        [_item()],
        backend,
        runs=2,
        on_run_done=lambda i, n, r, rt, passed, lat: runs_seen.append((i, n, r, rt, passed)),
    )
    item = report.items[0]
    assert item.runs == 2
    assert item.latency_s >= 0.0
    assert report.latency_s == item.latency_s
    assert [s[:4] for s in runs_seen] == [(1, 1, 1, 2), (1, 1, 2, 2)]
    assert [s[4] for s in runs_seen] == [False, True]


def test_run_items_routes_all_supported_kinds():
    expected_kinds = {
        "visualization",
        "metric_skill",
        "alert_skill",
        "search_tool",
        "general_question",
        "guardrail",
        "dashboard_summary",
    }
    assert expected_kinds == supported_test_kinds()


def test_run_items_invokes_langfuse_callback_for_non_skipped_items():
    backend = _FakeBackend([_chat_with(_viz_obj())])
    langfuse_calls: list[tuple] = []
    run_items(
        [_item()],
        backend,
        runs=1,
        on_langfuse_item_done=lambda idx, total, r: langfuse_calls.append((idx, total, r.id)),
    )
    assert langfuse_calls == [(1, 1, "i1")]


def test_run_items_does_not_invoke_langfuse_callback_for_skipped_items():
    item = DatasetItem(id="s1", dataset_name="d", test_kind="unknown_kind", question="q", expected_output={})
    langfuse_calls: list = []
    run_items(
        [item],
        _FakeBackend([_empty_chat()]),
        runs=1,
        on_langfuse_item_done=lambda idx, total, r: langfuse_calls.append(r.id),
    )
    assert langfuse_calls == []


def test_run_items_concurrency_produces_all_results_in_order():
    """With concurrency > 1 all items still appear in input order."""
    items = [
        DatasetItem(
            id=f"item-{i}",
            dataset_name="d",
            test_kind="visualization",
            question=f"q{i}",
            expected_output={"visualization": _viz_obj()},
        )
        for i in range(6)
    ]
    backend = _FakeBackend([_chat_with(_viz_obj())] * 6)
    report = run_items(items, backend, runs=1, concurrency=3)
    assert report.total == 6
    assert [r.id for r in report.items] == [f"item-{i}" for i in range(6)]
    assert all(r.pass_at_k for r in report.items)


def test_run_items_concurrency_1_and_sequential_produce_same_results():
    """concurrency=1 and the default sequential path give identical reports."""
    items = [
        DatasetItem(
            id=f"i{i}",
            dataset_name="d",
            test_kind="visualization",
            question="q",
            expected_output={"visualization": _viz_obj()},
        )
        for i in range(4)
    ]
    backend_a = _FakeBackend([_chat_with(_viz_obj())] * 4)
    backend_b = _FakeBackend([_chat_with(_viz_obj())] * 4)
    report_seq = run_items(items, backend_a, runs=1)
    report_par = run_items(items, backend_b, runs=1, concurrency=1)
    assert [r.id for r in report_seq.items] == [r.id for r in report_par.items]
    assert [r.pass_at_k for r in report_seq.items] == [r.pass_at_k for r in report_par.items]


def test_run_items_concurrency_errored_item_does_not_crash_pool():
    """An errored item is recorded but does not abort a concurrent run."""

    class _BoomBackend:
        def ask(self, question: str) -> ChatResult:
            raise RuntimeError("agent down")

    items = [
        DatasetItem(
            id=f"e{i}",
            dataset_name="d",
            test_kind="visualization",
            question="q",
            expected_output={"visualization": _viz_obj()},
        )
        for i in range(4)
    ]
    report = run_items(items, _BoomBackend(), runs=1, concurrency=3)
    assert report.total == 4
    assert report.errored == 4
    assert [r.id for r in report.items] == [f"e{i}" for i in range(4)]


def test_run_items_concurrency_callbacks_fire_for_all_items():
    """on_item_done is called exactly once per item under concurrency > 1."""
    backend = _FakeBackend([_chat_with(_viz_obj())] * 5)
    lock = threading.Lock()
    done_ids: list = []

    def on_done(index: int, total: int, report: ItemReport) -> None:
        with lock:
            done_ids.append(report.id)

    items = [
        DatasetItem(
            id=f"c{i}",
            dataset_name="d",
            test_kind="visualization",
            question="q",
            expected_output={"visualization": _viz_obj()},
        )
        for i in range(5)
    ]
    run_items(items, backend, runs=1, concurrency=3, on_item_done=on_done)
    assert sorted(done_ids) == [f"c{i}" for i in range(5)]


def test_run_items_callback_exception_is_logged_not_swallowed(capsys):
    """A raising callback prints a traceback to stderr but the run continues."""
    backend = _FakeBackend([_chat_with(_viz_obj())] * 2)
    items = [
        DatasetItem(
            id=f"x{i}",
            dataset_name="d",
            test_kind="visualization",
            question="q",
            expected_output={"visualization": _viz_obj()},
        )
        for i in range(2)
    ]

    def bad_callback(index, total, report):
        raise RuntimeError("callback bug")

    result = run_items(items, backend, runs=1, on_item_done=bad_callback)
    assert result.total == 2  # run did not abort
    err = capsys.readouterr().err
    assert "RuntimeError" in err or "callback bug" in err  # traceback was printed


class _FakeJudge:
    """Stand-in LLM judge keyed off the evaluation_steps it is built with.

    The summary evaluator builds a positive judge (must_include / rubric) and a
    violation judge (must_not_include). The violation judge must report the
    forbidden characteristic as ABSENT for the item to pass, so it returns
    ``(False, ...)``; every other judge reports a pass.
    """

    def __init__(self, evaluation_steps):
        self._is_violation = evaluation_steps == _VIOLATION_STEPS

    def score(self, *_args, **_kwargs):
        return (False, "absent") if self._is_violation else (True, "ok")


def test_run_items_covers_all_test_kinds_end_to_end(fixtures_dir, passing_backend):
    """Full pipeline over a dataset spanning all 7 test_kinds: runner routes each
    kind to its evaluator and scoring, no item skipped or errored, all pass."""
    items = load_local_dataset(Path(fixtures_dir) / "sample_dataset")
    assert {i.test_kind for i in items} == set(supported_test_kinds())

    with (
        patch("gooddata_eval.core.evaluators.general_question.LLMJudge", _FakeJudge),
        patch("gooddata_eval.core.evaluators.guardrail.LLMJudge", _FakeJudge),
        patch("gooddata_eval.core.evaluators.summary.LLMJudge", _FakeJudge),
    ):
        report = run_items(items, passing_backend, runs=1)

    assert report.total == len(supported_test_kinds())
    assert report.skipped == 0
    assert report.errored == 0
    assert report.passed == report.total, [(i.test_kind, i.pass_at_k, i.error) for i in report.items]
    assert sorted(passing_backend.calls) == sorted(i.id for i in items)
    for item_report in report.items:
        assert item_report.pass_at_k is True
        assert item_report.quality_score > 0.0
