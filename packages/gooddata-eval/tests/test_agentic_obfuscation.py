# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json
import re
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import httpx
import pytest
from gooddata_eval.core.agentic import _obfuscation_sinks, obfuscation
from gooddata_eval.core.agentic._obfuscation_check import SINK_CONVERSATION_DB, SINK_LANGFUSE_TRACE
from gooddata_eval.core.agentic._obfuscation_observe import WorkspaceEntities, observe_and_clean, snapshot
from gooddata_eval.core.agentic._obfuscation_sinks import (
    SinkUnavailableError,
    TraceNotFoundError,
    read_conversation_db,
    read_langfuse_session,
)
from gooddata_eval.core.agentic.obfuscation import ObfuscationAssertionError, evaluate_agentic_obfuscation
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.models import ChatResult

_EMAIL = "marie.canary7f3a@example.invalid"
_QUESTION = f"Can you check the recent orders for the account registered to {_EMAIL}?"
_MASKED = "Can you check the recent orders for the account registered to [EMAIL]?"
_EXPECTED: dict[str, Any] = {
    "canaries": [
        {
            "nonce": "canary7f3a",
            "value": _EMAIL,
            "class": "EMAIL",
            "absent_from": [SINK_LANGFUSE_TRACE, SINK_CONVERSATION_DB],
            "mask_marker_present": "[EMAIL]",
        }
    ],
    "status": "enforced",
}


@pytest.fixture(autouse=True)
def _fresh_preflight(monkeypatch):
    """Every test decides its own preflight outcome; none inherits a cached one."""
    monkeypatch.setattr(obfuscation, "_preflight_results", {})
    monkeypatch.setattr(obfuscation, "_PREFLIGHT_RETRY_SEC", 0)
    monkeypatch.setattr(_obfuscation_sinks, "_POLL_INTERVAL_SEC", 0)


def _answer(text: str = "Here are the recent orders.") -> ChatResult:
    return ChatResult.model_validate({"textResponse": text, "toolCallEvents": [], "responseId": "resp-1"})


def _db(*texts: str) -> dict:
    items = [{"role": "user", "content": {"type": "text", "text": t}} for t in texts]
    return {"conversation": {"title": None}, "items": items}


def _trace(*texts: str) -> list:
    return [
        {"id": f"t{i}", "input": json.dumps({"parts": [{"text": t}]}), "observations": []} for i, t in enumerate(texts)
    ]


@contextmanager
def _patched(client, *, db, lf):
    with (
        patch("gooddata_eval.core.agentic.obfuscation.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.obfuscation.read_conversation_db", side_effect=db),
        patch("gooddata_eval.core.agentic.obfuscation.read_langfuse_session", side_effect=lf),
        patch("gooddata_eval.core.agentic.obfuscation._warn_on_scrub_prone_user"),
    ):
        yield


class _Chat:
    """A chat client whose conversations remember the turns sent to them."""

    def __init__(self, fail_with: dict[str, ChatError] | None = None) -> None:
        self.sent: dict[str, list[str]] = {}
        self._n = 0
        self._fail_with = fail_with or {}

    def create_conversation(self) -> str:
        self._n += 1
        conversation_id = f"conv-{self._n}"
        self.sent[conversation_id] = []
        return conversation_id

    def send_message(self, conversation_id: str, question: str) -> ChatResult:
        self.sent.setdefault(conversation_id, []).append(question)
        for marker, exc in self._fail_with.items():
            if marker in question:
                raise exc
        return _answer()

    def delete_conversation(self, conversation_id: str) -> None:
        pass

    def close(self) -> None:
        pass


_ANY_EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")


def _is_probe(chat: _Chat, conversation_id: str) -> bool:
    return "@example.invalid" in chat.sent[conversation_id][0] and "qa.preflight" in chat.sent[conversation_id][0]


def _masking(chat: _Chat, *, leak_into_langfuse: bool = False):
    """Sinks that store the masked copy; optionally let an item's (not the probe's) canary reach Langfuse."""

    def masked(conversation_id: str) -> list[str]:
        return [_ANY_EMAIL.sub("[EMAIL]", t) for t in chat.sent[conversation_id]]

    def db(_http, _url, conversation_id, anchors, **_kw):
        return _db(*masked(conversation_id))

    def lf(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        raw = leak_into_langfuse and not _is_probe(chat, conversation_id)
        return _trace(*(chat.sent[conversation_id] if raw else masked(conversation_id)))

    return db, lf


def _evaluate(**kwargs: Any):
    kwargs.setdefault("expected_output", _EXPECTED)
    return evaluate_agentic_obfuscation(host="https://h", token="tok", workspace_id="ws1", question=_QUESTION, **kwargs)


def test_masked_in_both_sinks_passes():
    chat = _Chat()
    db, lf = _masking(chat)
    with _patched(chat, db=db, lf=lf):
        outcome = _evaluate()
    assert outcome.detail["leak_free"] is True
    assert outcome.detail["trace_found"] is True
    assert outcome.runs_passed == 1


def test_canary_reaching_langfuse_fails_as_a_leak():
    chat = _Chat()
    db, lf = _masking(chat, leak_into_langfuse=True)
    with _patched(chat, db=db, lf=lf), pytest.raises(ObfuscationAssertionError, match="LEAK EMAIL"):
        _evaluate()


def test_preflight_failure_stops_every_item_of_the_workspace_without_retrying_it():
    chat = _Chat()

    def unmasked_db(_http, _url, conversation_id, anchors, **_kw):
        return _db(*chat.sent[conversation_id])

    _, lf = _masking(chat)
    with _patched(chat, db=unmasked_db, lf=lf):
        with pytest.raises(ObfuscationAssertionError, match="preflight failed"):
            _evaluate()
        probes = len(chat.sent)
        with pytest.raises(ObfuscationAssertionError, match="preflight failed"):
            _evaluate()
    assert len(chat.sent) == probes, "the cached verdict must not probe again"
    assert all(_is_probe(chat, c) for c in chat.sent), "no item ran behind a failed preflight"


def test_a_probe_copied_into_a_tool_step_detail_does_not_fail_the_preflight():
    chat = _Chat()
    db, lf = _masking(chat)

    def db_with_step_detail(_http, _url, conversation_id, anchors, **_kw):
        stored = db(_http, _url, conversation_id, anchors)
        if _is_probe(chat, conversation_id):
            found = _ANY_EMAIL.search(chat.sent[conversation_id][0])
            assert found is not None
            raw = found.group(0)
            stored["items"].append({"role": "tool", "detail": {"category": "catalogSearch", "query": [raw]}})
        return stored

    with _patched(chat, db=db_with_step_detail, lf=lf):
        outcome = _evaluate()
    assert outcome.runs_passed == 1, "the item ran and passed behind the preflight"


def test_a_probe_reaching_langfuse_fails_the_preflight():
    chat = _Chat()
    db, _ = _masking(chat)

    def raw_trace(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        return _trace(*chat.sent[conversation_id])

    with _patched(chat, db=db, lf=raw_trace), pytest.raises(ObfuscationAssertionError, match="preflight failed"):
        _evaluate()


def test_refused_turn_is_the_expected_outcome_when_the_item_says_so():
    rejected = ChatError("SSE error 422", status_code=422, reason="DATA_OBFUSCATION_CONTENT_REJECTED")
    chat = _Chat(fail_with={"C:\\Users": rejected})
    expected = {
        "canaries": [{**_EXPECTED["canaries"][0], "mask_marker_present": None}],
        "expected_turn_rejected": {"status_code": 422, "reason": "DATA_OBFUSCATION_CONTENT_REJECTED"},
    }
    db, lf = _masking(chat)

    def no_trace(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        return lf(_langfuse, conversation_id, anchors) if _is_probe(chat, conversation_id) else None

    with _patched(chat, db=db, lf=no_trace):
        outcome = evaluate_agentic_obfuscation(
            host="https://h",
            token="tok",
            workspace_id="ws1",
            question=f"The log line was C:\\Users\\svc\\{_EMAIL} and it aborted",
            expected_output=expected,
        )
    assert outcome.detail["leak_free"] is True


def test_an_unexpected_refusal_says_nothing_about_masking():
    unavailable = ChatError("SSE error 503", status_code=503, reason="DATA_OBFUSCATION_UNAVAILABLE")
    chat = _Chat(fail_with={"recent orders": unavailable})
    db, lf = _masking(chat)
    with _patched(chat, db=db, lf=lf), pytest.raises(ObfuscationAssertionError, match="DATA_OBFUSCATION_UNAVAILABLE"):
        _evaluate()


def test_turns_are_sent_in_order_to_one_conversation():
    chat = _Chat()
    db, lf = _masking(chat)
    turns = [_QUESTION, "Now show the same Total Sales by quarter instead."]
    with _patched(chat, db=db, lf=lf):
        _evaluate(turns=turns)
    item_conversations = [t for c, t in chat.sent.items() if not _is_probe(chat, c)]
    assert item_conversations == [turns]


def test_an_answer_rubric_does_not_decide_the_verdict():
    chat = _Chat()
    db, lf = _masking(chat)
    with _patched(chat, db=db, lf=lf):
        outcome = _evaluate(expected_output={**_EXPECTED, "answer_rubric": "answer the analytics question"})
    assert outcome.runs_passed == 1


def test_a_leak_in_one_run_fails_the_item_whatever_the_gate():
    chat = _Chat()
    db, lf = _masking(chat)
    calls = {"n": 0}

    def one_bad_run(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        if _is_probe(chat, conversation_id):
            return lf(_langfuse, conversation_id, anchors)
        calls["n"] += 1
        return _trace(*chat.sent[conversation_id]) if calls["n"] == 2 else lf(_langfuse, conversation_id, anchors)

    with _patched(chat, db=db, lf=one_bad_run), pytest.raises(ObfuscationAssertionError, match="run 1: LEAK"):
        _evaluate(k=2, gate="any")


def test_a_leak_in_one_run_is_not_scored_as_a_passed_gate():
    chat = _Chat()
    db, lf = _masking(chat)
    calls = {"n": 0}

    def one_bad_run(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        if _is_probe(chat, conversation_id):
            return lf(_langfuse, conversation_id, anchors)
        calls["n"] += 1
        return _trace(*chat.sent[conversation_id]) if calls["n"] == 2 else lf(_langfuse, conversation_id, anchors)

    with (
        _patched(chat, db=db, lf=one_bad_run),
        patch("gooddata_eval.core.agentic.obfuscation.submit_trace_scoring") as submit,
        pytest.raises(ObfuscationAssertionError),
    ):
        _evaluate(k=2, gate="any", langfuse=MagicMock(), dataset_item_id="i1")
    ctx = MagicMock()
    ctx.observe.return_value.__exit__.return_value = False  # let an error in the block surface
    submit.call_args.kwargs["write_scores"](ctx)
    gate = [c.kwargs["value"] for c in ctx.score.call_args_list if c.kwargs["name"] == "gate_passed"]
    assert gate == [False, False], "reports read gate_passed first; it must agree with the failed item"


def _one_run_without_a_trace(chat, lf):
    calls = {"n": 0}

    def read(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        if _is_probe(chat, conversation_id):
            return lf(_langfuse, conversation_id, anchors)
        calls["n"] += 1
        if calls["n"] == 1:
            raise TraceNotFoundError(f"TRACE_NOT_FOUND: no Langfuse trace for session {conversation_id} after 60s")
        return lf(_langfuse, conversation_id, anchors)

    return read


def test_a_run_without_a_trace_is_a_failed_run_the_any_gate_can_carry():
    chat = _Chat()
    db, lf = _masking(chat)
    with _patched(chat, db=db, lf=_one_run_without_a_trace(chat, lf)):
        outcome = _evaluate(k=2, gate="any")
    assert outcome.runs_passed == 1
    assert outcome.detail["trace_found"] is False, "the run that saw no trace is still reported"


def test_a_run_without_a_trace_fails_the_power_gate():
    chat = _Chat()
    db, lf = _masking(chat)
    with (
        _patched(chat, db=db, lf=_one_run_without_a_trace(chat, lf)),
        pytest.raises(ObfuscationAssertionError, match="run 0: TRACE_NOT_FOUND"),
    ):
        _evaluate(k=2, gate="power")


def test_a_turn_that_failed_reads_no_sink_so_it_claims_no_clean_result():
    unavailable = ChatError("SSE error 503", status_code=503, reason="DATA_OBFUSCATION_UNAVAILABLE")
    chat = _Chat(fail_with={"recent orders": unavailable})
    db, lf = _masking(chat)
    with _patched(chat, db=db, lf=lf), pytest.raises(ObfuscationAssertionError) as raised:
        _evaluate()
    assert raised.value.detail["leak_free"] is False
    assert raised.value.detail["trace_found"] is False


def test_each_run_is_scored_with_its_own_failures():
    chat = _Chat()
    db, lf = _masking(chat)
    calls = {"n": 0}

    def second_run_leaks(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        if _is_probe(chat, conversation_id):
            return lf(_langfuse, conversation_id, anchors)
        calls["n"] += 1
        return _trace(*chat.sent[conversation_id]) if calls["n"] == 2 else lf(_langfuse, conversation_id, anchors)

    with (
        _patched(chat, db=db, lf=second_run_leaks),
        patch("gooddata_eval.core.agentic.obfuscation.submit_trace_scoring") as submit,
        pytest.raises(ObfuscationAssertionError),
    ):
        _evaluate(k=2, gate="any", langfuse=MagicMock(), dataset_item_id="i1")
    ctx = MagicMock()
    ctx.observe.return_value.__exit__.return_value = False
    submit.call_args.kwargs["write_scores"](ctx)
    comments = [c.kwargs.get("comment") for c in ctx.score.call_args_list if c.kwargs["name"] == "obfuscation_pass"]
    assert comments[0] == "no failure"
    assert "LEAK EMAIL" in comments[1] and "canary7f3a" not in comments[1]


def test_expected_output_without_canaries_is_rejected():
    with pytest.raises(ValueError, match="canaries"):
        evaluate_agentic_obfuscation(
            host="https://h", token="tok", workspace_id="ws1", question="q", expected_output={"status": "enforced"}
        )


# --- sinks --------------------------------------------------------------------------


def _gd_http(handler) -> httpx.Client:
    return httpx.Client(transport=httpx.MockTransport(handler))


def test_db_read_back_waits_for_the_anchor_and_returns_record_and_items():
    reads = {"n": 0}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/items"):
            reads["n"] += 1
            items = [] if reads["n"] == 1 else [{"role": "user", "content": {"text": _MASKED}}]
            return httpx.Response(200, json={"items": items})
        return httpx.Response(200, json={"title": "t"})

    with _gd_http(handler) as http:
        doc = read_conversation_db(http, "https://h/api/v1/ai/workspaces/ws/chat/conversations", "c1", ["check the"])
    assert doc["conversation"] == {"title": "t"}
    assert doc["items"][0]["content"]["text"] == _MASKED


def test_db_read_back_error_is_a_sink_error_not_an_empty_sink():
    with (
        _gd_http(lambda request: httpx.Response(403, text="forbidden")) as http,
        pytest.raises(SinkUnavailableError, match="403"),
    ):
        read_conversation_db(http, "https://h/api/v1/ai/workspaces/ws/chat/conversations", "c1", ["x"])


def test_langfuse_read_back_needs_a_client():
    with pytest.raises(SinkUnavailableError, match="no Langfuse client"):
        read_langfuse_session(None, "c1", ["x"])


def test_langfuse_read_back_returns_every_trace_of_the_session():
    langfuse = MagicMock()
    langfuse.session_trace_ids.return_value = ["t1"]
    langfuse.get_trace.return_value = {"id": "t1", "input": _MASKED, "observations": [{"id": "o1"}]}
    traces = read_langfuse_session(langfuse, "c1", ["check the"])
    assert traces == [langfuse.get_trace.return_value]
    langfuse.session_trace_ids.assert_called_with("c1")


def test_langfuse_read_back_of_a_rejected_turn_may_be_empty(monkeypatch):
    monkeypatch.setattr(_obfuscation_sinks, "_DEFAULT_LANGFUSE_TIMEOUT_SEC", 0)
    langfuse = MagicMock()
    langfuse.session_trace_ids.return_value = []
    assert read_langfuse_session(langfuse, "c1", [], allow_empty=True) is None
    with pytest.raises(TraceNotFoundError, match="^TRACE_NOT_FOUND: no Langfuse trace for session c1 after 0s$"):
        read_langfuse_session(langfuse, "c1", ["x"])


def test_a_langfuse_read_error_is_never_taken_for_a_turn_that_exported_nothing(monkeypatch):
    monkeypatch.setattr(_obfuscation_sinks, "_DEFAULT_LANGFUSE_TIMEOUT_SEC", 0)
    langfuse = MagicMock()
    denied = httpx.Response(401, request=httpx.Request("GET", "https://lf/api/public/sessions/c1"))
    langfuse.session_trace_ids.side_effect = httpx.HTTPStatusError("401", request=denied.request, response=denied)
    with pytest.raises(SinkUnavailableError, match="Langfuse session c1") as raised:
        read_langfuse_session(langfuse, "c1", [], allow_empty=True)
    assert not isinstance(raised.value, TraceNotFoundError)
    with pytest.raises(SinkUnavailableError) as raised:
        read_langfuse_session(langfuse, "c1", ["x"])
    assert not isinstance(raised.value, TraceNotFoundError), "a failed read is not a missing trace"


def test_a_db_transport_or_body_error_is_a_sink_error(monkeypatch):
    monkeypatch.setattr(_obfuscation_sinks, "_DB_TIMEOUT_SEC", 0)
    url = "https://h/api/v1/ai/workspaces/ws/chat/conversations"

    def refused(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("refused", request=request)

    with _gd_http(refused) as http, pytest.raises(SinkUnavailableError, match="refused"):
        read_conversation_db(http, url, "c1", ["x"])
    with (
        _gd_http(lambda request: httpx.Response(200, text="<html>")) as http,
        pytest.raises(SinkUnavailableError, match="not JSON"),
    ):
        read_conversation_db(http, url, "c1", ["x"])


def test_a_slow_db_read_is_polled_again():
    reads = {"n": 0}
    item = {"role": "user", "content": {"type": "text", "text": "Can you check the recent orders"}}

    def handler(request: httpx.Request) -> httpx.Response:
        reads["n"] += 1
        if reads["n"] == 1:
            raise httpx.ReadTimeout("slow", request=request)
        return httpx.Response(200, json={"items": [item]} if request.url.path.endswith("/items") else {"id": "c1"})

    with _gd_http(handler) as http:
        doc = read_conversation_db(http, "https://h/api/v1/ai/workspaces/ws/chat/conversations", "c1", ["check the"])
    assert doc["items"] == [item]


def test_an_item_needs_at_least_one_run():
    with pytest.raises(ValueError, match="at least one run"):
        _evaluate(k=0)


@pytest.mark.parametrize("error", [ValueError("not JSON"), KeyError("id")])
def test_an_unreadable_langfuse_response_is_a_sink_error(error):
    langfuse = MagicMock()
    langfuse.session_trace_ids.side_effect = error
    with pytest.raises(SinkUnavailableError, match="unreadable response") as raised:
        read_langfuse_session(langfuse, "c1", ["x"])
    assert not isinstance(raised.value, TraceNotFoundError)


def test_trace_not_found_says_how_many_reads_timed_out(monkeypatch):
    monkeypatch.setattr(_obfuscation_sinks, "_DEFAULT_LANGFUSE_TIMEOUT_SEC", 0)
    langfuse = MagicMock()
    langfuse.session_trace_ids.side_effect = httpx.ReadTimeout("slow")
    with pytest.raises(TraceNotFoundError, match=r"\(1 read\(s\) timed out\)$"):
        read_langfuse_session(langfuse, "c1", ["x"])


def test_the_default_wait_for_a_trace_is_sixty_seconds():
    assert _obfuscation_sinks._DEFAULT_LANGFUSE_TIMEOUT_SEC == 60.0


def test_an_item_whose_trace_never_arrives_fails_marked_as_trace_not_found():
    chat = _Chat()
    db, lf = _masking(chat)

    def no_item_trace(_langfuse, conversation_id, anchors, allow_empty=False, **_kw):
        if _is_probe(chat, conversation_id):
            return lf(_langfuse, conversation_id, anchors)
        raise TraceNotFoundError(f"TRACE_NOT_FOUND: no Langfuse trace for session {conversation_id} after 60s")

    with _patched(chat, db=db, lf=no_item_trace), pytest.raises(ObfuscationAssertionError) as raised:
        _evaluate()
    assert "run 0: TRACE_NOT_FOUND" in str(raised.value)
    assert raised.value.detail["trace_found"] is False
    assert raised.value.detail["leak_free"] is True, "a missing trace is not a leak"


# --- observe ------------------------------------------------------------------------


def test_observe_reports_and_deletes_only_the_automation_the_item_made():
    listed = {"n": 0}
    deleted: list[str] = []
    pre = {"id": "old", "attributes": {"metadata": "total_sales"}}
    made = {
        "id": "new",
        "attributes": {"metadata": "total_sales", "externalRecipients": [{"email": "[EMAIL]"}]},
        "relationships": {"recipients": {"data": [{"id": "u1"}]}},
    }
    other = {"id": "someone-else", "attributes": {"metadata": "net_sales"}}

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "DELETE":
            deleted.append(request.url.path.rsplit("/", 1)[1])
            return httpx.Response(204)
        listed["n"] += 1
        return httpx.Response(200, json={"data": [pre] if listed["n"] == 1 else [pre, made, other]})

    with _gd_http(handler) as http:
        entities = WorkspaceEntities(http, "https://h", "ws")
        spec = {"automation_match": "total_sales", "stream_markers": ["[EMAIL]"]}
        before = snapshot(entities, spec)
        notes = observe_and_clean(entities, spec, before, last_stream='{"text": "sent to [EMAIL]"}')
    assert deleted == ["new"]
    assert "OBSERVED automation new created with external=['[EMAIL]'] internal=['u1']" in notes
    assert "OBSERVED last turn stream contains '[EMAIL]'" in notes


def test_observe_says_so_when_the_chat_created_nothing():
    with _gd_http(lambda request: httpx.Response(200, json={"data": []})) as http:
        entities = WorkspaceEntities(http, "https://h", "ws")
        spec = {"metric_title": "Average Order Value QA"}
        notes = observe_and_clean(entities, spec, snapshot(entities, spec), last_stream="")
    assert notes == ["OBSERVED no metric titled 'Average Order Value QA' was created"]


def test_observe_cleanup_errors_become_notes_and_do_not_stop_the_rest():
    made = [
        {"id": "a1", "attributes": {"metadata": "total_sales"}},
        {"id": "a2", "attributes": {"metadata": "total_sales"}},
    ]
    listed = {"n": 0}
    deleted: list[str] = []

    def handler(request: httpx.Request) -> httpx.Response:
        if request.method == "DELETE":
            entity_id = request.url.path.rsplit("/", 1)[1]
            deleted.append(entity_id)
            return httpx.Response(404 if entity_id == "a1" else 500)
        if "/metrics" in request.url.path:
            return httpx.Response(503)
        listed["n"] += 1
        return httpx.Response(200, json={"data": [] if listed["n"] == 1 else made})

    with _gd_http(handler) as http:
        entities = WorkspaceEntities(http, "https://h", "ws")
        spec = {"automation_match": "total_sales"}
        before = snapshot(entities, spec)
        notes = observe_and_clean(entities, {**spec, "metric_title": "M"}, {**before, "metrics": set()}, "")
    assert deleted == ["a1", "a2"], "a 404 is already gone and a 500 does not stop the next delete"
    assert any(n.startswith("OBSERVED could not delete automations a2") for n in notes)
    assert any(n.startswith("OBSERVED cleanup failed (metrics)") for n in notes)


def test_observe_lists_every_page_of_a_busy_workspace(monkeypatch):
    monkeypatch.setattr("gooddata_eval.core.agentic._obfuscation_observe._PAGE_SIZE", 2)
    pages = [[{"id": "a"}, {"id": "b"}], [{"id": "c"}, {"id": "d"}], [{"id": "e"}]]

    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(200, json={"data": pages[int(request.url.params["page"])]})

    with _gd_http(handler) as http:
        listed = WorkspaceEntities(http, "https://h", "ws").list("automations")
    assert sorted(listed) == ["a", "b", "c", "d", "e"]


def test_a_slow_langfuse_read_is_polled_again_not_reported_as_missing():
    langfuse = MagicMock()
    langfuse.session_trace_ids.return_value = ["t1"]
    trace = {"id": "t1", "input": _MASKED, "observations": [{"id": "o1"}]}
    langfuse.get_trace.side_effect = [httpx.ReadTimeout("slow"), trace, trace]
    assert read_langfuse_session(langfuse, "c1", ["check the"]) == [trace]
