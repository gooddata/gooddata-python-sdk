# (C) 2026 GoodData Corporation
from gooddata_eval.core.evaluators import supported_test_kinds
from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.runner import run_items


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

    def ask(self, question: str) -> ChatResult:
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
        def ask(self, question: str) -> ChatResult:
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
    expected_kinds = {"visualization", "metric_skill", "alert_skill", "search_tool", "general_question", "guardrail"}
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
