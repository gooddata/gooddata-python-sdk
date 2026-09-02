# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import sys
import types
from contextlib import ExitStack, contextmanager
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.metric_skill import (
    AgenticMetricSummary,
    MetricRunResult,
    MetricSkillAssertionError,
    SimulatedResponseError,
    _delete_metric,
    _extract_metric_result,
    _no_where_clause_hint,
    _normalize_maql,
    evaluate_agentic_metric_skill,
    generate_simulated_response,
    run_agentic_metric_skill,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent
from gooddata_eval.core.timing import TIMERS_ENV_VAR

# --- time.monotonic() side effects ---------------------------------------------------
#
# metric_skill reads the clock twice per agent turn (start, stop) and twice more per
# simulated-user reply, so a two-turn conversation needs six values. Named rather than
# inlined because a single new clock read on the production path breaks every one of these
# at once with StopIteration -- and repairing a bare literal means hand-counting clock
# reads at each call site.

# one turn, metric created straight away: agent 3.0s, no simulated user
_CLOCK_ONE_TURN = [5.0, 8.0]
# two turns: agent 1.0s then 0.5s, with a 2.5s simulated-user reply between them
_CLOCK_TWO_TURNS = [20.0, 21.0, 21.0, 23.5, 23.5, 24.0]


def _client() -> MagicMock:
    """A chat client whose conversations are all ``conv-1``.

    Callers override only what they vary -- ``send_message`` and the rest are ordinary
    mock attributes.
    """
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    return client


@contextmanager
def _patched(client, *, simulated_reply=None, simulated_error=None, sdk=False, monotonic=None):
    """Patch metric_skill's ChatClient plus whichever collaborators a test needs.

    ``simulated_reply``/``simulated_error`` patch the simulated user (reply, or raise);
    ``sdk`` patches GoodDataSdk (the created metric's cleanup path); ``monotonic`` feeds
    the clock one of the ``_CLOCK_*`` constants above. Yields
    ``(mock_generate_simulated_response, mock_GoodDataSdk)`` -- None for whatever was not
    patched.
    """
    with ExitStack() as stack:
        stack.enter_context(patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=client))
        mock_sim = mock_sdk_cls = None
        if simulated_reply is not None or simulated_error is not None:
            mock_sim = stack.enter_context(
                patch(
                    "gooddata_eval.core.agentic.metric_skill.generate_simulated_response",
                    return_value=simulated_reply,
                    side_effect=simulated_error,
                )
            )
        if sdk:
            mock_sdk_cls = stack.enter_context(patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk"))
        if monotonic is not None:
            stack.enter_context(patch("time.monotonic", side_effect=monotonic))
        yield mock_sim, mock_sdk_cls


def _create_metric_call(result: str) -> ToolCallEvent:
    return ToolCallEvent(function_name="create_metric", function_arguments="{}", result=result)


_FAILED_RESULT = '{"data": {"isError": true, "error": {"text": "invalid MAQL"}}}'


def test_extract_metric_result_skips_a_failed_retry_and_returns_the_successful_one():
    """QA-29053 regression: agent self-corrects an invalid MAQL by retrying create_metric
    within the same turn; the successful retry must be captured, not the failed first call."""
    calls = [
        _create_metric_call(_FAILED_RESULT),
        _create_metric_call('{"data": {"metric_id": "m1", "maql": "SELECT {metric/foo}"}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m1", "maql": "SELECT {metric/foo}"}


def test_extract_metric_result_returns_none_when_every_attempt_failed():
    calls = [_create_metric_call(_FAILED_RESULT), _create_metric_call(_FAILED_RESULT)]
    assert _extract_metric_result(calls) is None


def test_extract_metric_result_skips_a_failed_call_after_an_earlier_success():
    # The failed call is last, so reversed() reaches it first and must skip past it.
    calls = [_create_metric_call('{"data": {"metric_id": "m1"}}'), _create_metric_call(_FAILED_RESULT)]
    assert _extract_metric_result(calls) == {"metric_id": "m1"}


def test_extract_metric_result_prefers_the_most_recent_successful_call():
    """Two distinct successful create_metric calls in one turn (not a retry after a
    failure) -- the later one wins."""
    calls = [
        _create_metric_call('{"data": {"metric_id": "m1"}}'),
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_a_non_dict_payload():
    # The non-dict payload is last, so reversed() reaches it first and must skip past it.
    calls = [
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
        _create_metric_call('{"data": [{"metric_id": "m1"}]}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_a_non_dict_decoded_result():
    # The whole decoded result (not just its "data" field) is a non-dict here.
    calls = [_create_metric_call('{"metric_id": "m2"}'), _create_metric_call("[]")]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_extract_metric_result_skips_an_empty_payload():
    # The empty payload is last, so reversed() reaches it first and must skip past it.
    calls = [
        _create_metric_call('{"data": {"metric_id": "m2"}}'),
        _create_metric_call('{"data": {}}'),
    ]
    assert _extract_metric_result(calls) == {"metric_id": "m2"}


def test_normalize_maql_strips_whitespace():
    assert _normalize_maql("  SELECT  { metric/foo }  ") == "select {metric/foo}"


def test_normalize_maql_removes_select_wrapper():
    assert _normalize_maql("(SELECT {metric/abc})") == "{metric/abc}"


def test_no_where_clause_hint_is_empty_when_a_candidate_has_a_where_clause():
    assert _no_where_clause_hint(['SELECT {metric/foo} WHERE {label/status} = "active"']) == ""


def test_no_where_clause_hint_is_present_when_no_candidate_has_a_where_clause():
    """QA-29094 follow-up: whether to add a filter must not be left to the simulating LLM's
    judgment of what the original request "implies" -- that fuzzy reasoning is exactly what
    caused it to inject an unrequested filter in the first place."""
    hint = _no_where_clause_hint(["SELECT SUM({fact/order_unit_quantity})"])
    assert hint != ""
    assert "no filter is needed" in hint


def test_no_where_clause_hint_stays_silent_if_any_candidate_has_a_where_clause():
    """PR #1760 review (Henry): _no_where_clause_hint used to see only expected_outputs[0].
    A fixture like agent_metric_skill_4.json lists an unfiltered candidate first and a
    filtered one second -- both accepted by _best_maql_match. Hinting "no filter needed"
    off candidate 0 alone would steer the agent away from the filtered candidate even
    though the scorer would still take it -- the mirror image of the original QA-29094 bug.
    """
    candidates = [
        "SELECT SUM({fact/order_unit_quantity})",
        'SELECT SUM({fact/order_unit_quantity}) WHERE {label/order_status} = "Processed"',
    ]
    assert _no_where_clause_hint(candidates) == ""


def test_no_where_clause_hint_ignores_where_inside_an_identifier():
    """CodeRabbit finding on PR #1760: a naive substring check treats the "where" inside
    an identifier like {metric/somewhere_sales} as a real WHERE clause and wrongly stays
    silent -- it must be stripped as a protected span before matching."""
    assert _no_where_clause_hint(["SELECT {metric/somewhere_sales}"]) != ""


def test_no_where_clause_hint_ignores_where_inside_a_quoted_literal():
    assert _no_where_clause_hint(['SELECT {metric/x} = "somewhere nearby"']) != ""


def test_no_where_clause_hint_ignores_where_inside_a_literal_with_an_escaped_quote():
    """CodeRabbit finding on PR #1760: an escaped quote inside a quoted literal ended the
    protected-span match early, leaking the rest of the literal's text -- including a
    standalone WHERE -- as unprotected. Uses _HINT_PROTECTED_RE (escape-aware), kept
    separate from the shared _PROTECTED_RE that feeds the maql_correct comparator (PR
    #1760 review, Henry) -- see test_normalize_maql_does_not_consume_escape_sequences."""
    maql = 'SELECT {metric/x} = "Jane\\"s store WHERE something"'
    assert _no_where_clause_hint([maql]) != ""


def test_generate_simulated_response_prompt_preserves_maql_fidelity(monkeypatch):
    """Regression test for a live-reproduced bug: the old prompt ("reply briefly",
    no instruction to cover clauses the assistant didn't ask about) let the
    simulating LLM silently drop a MAQL's WHERE clause or paraphrase a label id --
    confirmed via a 5x-repeated A/B test (1/5 vs 5/5 fidelity) that this was the
    prompt, not the model (gpt-4o did not fix it under the old prompt either).
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="ok"))]
    mock_client.chat.completions.create.return_value = mock_response

    # `openai` is an optional [llm-judge] extra, not installed in this test env --
    # inject a fake module rather than patching a real one (mirrors how the source
    # itself does `from openai import OpenAI` as a local, guarded import).
    fake_openai_module = types.SimpleNamespace(OpenAI=MagicMock(return_value=mock_client), OpenAIError=Exception)
    monkeypatch.setitem(sys.modules, "openai", fake_openai_module)

    expected_output = {"maql": 'SELECT {metric/spend_amount_-_cutcgco} WHERE {label/ecommerce_indicator_code} = "1"'}
    generate_simulated_response(
        "Which base metric should I use?", [expected_output], "I need a metric for spend amount"
    )

    call_kwargs = mock_client.chat.completions.create.call_args.kwargs
    sent_prompt = call_kwargs["messages"][0]["content"]

    assert expected_output["maql"] in sent_prompt
    assert "verbatim" in sent_prompt
    assert "filter" in sent_prompt.lower()
    # Guards against a truncated reply mid-MAQL -- the LLM was cutting fidelity short under
    # the old, lower budget before this was raised (see the docstring above).
    assert call_kwargs["max_tokens"] >= 300


def test_generate_simulated_response_prompt_agrees_when_the_original_request_is_already_satisfied(monkeypatch):
    """Regression test for QA-29094: the old prompt told the simulated user to force every
    clause of the ground-truth MAQL regardless of what the original request actually asked
    for, so it would inject filters/constraints the user never mentioned even when the
    assistant's proposal already matched the request. The prompt must now carry the
    original request and instruct the simulated user to agree when it's already satisfied.
    """
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="ok"))]
    mock_client.chat.completions.create.return_value = mock_response
    fake_openai_module = types.SimpleNamespace(OpenAI=MagicMock(return_value=mock_client), OpenAIError=Exception)
    monkeypatch.setitem(sys.modules, "openai", fake_openai_module)

    original_question = "I need a metric for total ordered units called Total Order Quantity"
    expected_output = {"maql": "SELECT SUM({fact/order_unit_quantity}) WHERE {fact/order_status} != 'cancelled'"}
    generate_simulated_response("Should I create this metric?", [expected_output], original_question)

    sent_prompt = mock_client.chat.completions.create.call_args.kwargs["messages"][0]["content"]

    # Structural checks on the interpolated data -- robust to prompt-wording edits.
    assert original_question in sent_prompt
    assert expected_output["maql"] in sent_prompt
    assert "reply briefly" not in sent_prompt.lower()
    # A ground-truth MAQL with a WHERE clause must not trigger the no-filter-needed hint.
    assert "no filter is needed" not in sent_prompt


def test_generate_simulated_response_prompt_handles_a_clarifying_question(monkeypatch):
    """QA-29094 follow-up: the two-branch prompt ("already satisfies" / "missing something")
    both assume the assistant made a proposal -- but the dominant real case is the assistant
    asking a clarifying question first (no proposal exists yet to judge as satisfying or not).
    Without an explicit instruction, the simulating LLM could classify "nothing proposed yet"
    as trivially "satisfied" and reply "yes, that works", leaving the agent no closer to a
    usable metric and burning iterations."""
    monkeypatch.setenv("OPENAI_API_KEY", "test-key")
    mock_client = MagicMock()
    mock_response = MagicMock()
    mock_response.choices = [MagicMock(message=MagicMock(content="ok"))]
    mock_client.chat.completions.create.return_value = mock_response
    fake_openai_module = types.SimpleNamespace(OpenAI=MagicMock(return_value=mock_client), OpenAIError=Exception)
    monkeypatch.setitem(sys.modules, "openai", fake_openai_module)

    expected_output = {"maql": "SELECT SUM({fact/order_unit_quantity})"}
    generate_simulated_response("Which base metric should I use?", [expected_output], "I need total ordered units")

    sent_prompt = mock_client.chat.completions.create.call_args.kwargs["messages"][0]["content"]

    assert "clarifying question" in sent_prompt
    # No WHERE clause in the ground truth -- the no-filter hint must fire here too.
    assert "no filter is needed" in sent_prompt


def test_normalize_maql_is_case_insensitive_for_keywords():
    """Regression test for a live-reproduced bug: 'FOR PREVIOUS(...)' vs
    'FOR Previous(...)' scored as a mismatch even though MAQL keywords are
    case-insensitive -- a semantically identical agent answer failed the eval
    purely on keyword casing."""
    actual = "SELECT {metric/active_card_count_-_txn_-_cutcgco} FOR PREVIOUS({label/process_date.year})"
    expected = "SELECT {metric/active_card_count_-_txn_-_cutcgco}\n  FOR Previous({label/process_date.year})"
    assert _normalize_maql(actual) == _normalize_maql(expected)


def test_normalize_maql_preserves_identifier_case():
    # {type/id} references are real, case-sensitive ids -- must never be casefolded.
    assert "Mixed_Case_Id" in _normalize_maql("SELECT {metric/Mixed_Case_Id}")


def test_normalize_maql_preserves_quoted_literal_case():
    """The bug this guards against: naively lowercasing everything outside {..}
    would also lowercase quoted WHERE-clause literal values, which are real,
    case-sensitive data -- not keywords. Two literals differing only in case
    must NOT be treated as equal; that would be a false positive."""
    assert _normalize_maql('WHERE {label/status} = "Active"') != _normalize_maql('WHERE {label/status} = "active"')


def test_normalize_maql_does_not_consume_escape_sequences():
    """PR #1760 review (Henry): _PROTECTED_RE feeds this comparator (via
    _casefold_outside_protected), so it must NOT treat \\X as an escape sequence unless
    MAQL literals are confirmed to support backslash escaping (unconfirmed). A `\\"`
    inside a literal must still end that literal at the next real quote -- not swallow
    everything up to the following quoted value, which would leave a real keyword like
    AND uncasefolded and a later literal's case wrongly casefolded."""
    maql = 'SELECT {metric/x} WHERE {label/path} = "C:\\" AND {label/y} = "Active"'
    normalized = _normalize_maql(maql)
    assert "and {label/y}" in normalized  # AND is a keyword outside the literal -- casefolded
    assert '"Active"' in normalized  # the second literal's case is untouched -- not "active"


def test_metric_run_result_fields():
    r = MetricRunResult(
        conversation_id="c1",
        metric_result={"maql": "SELECT {metric/x}"},
        metric_created=True,
        actual_maql="SELECT {metric/x}",
        maql_correct=True,
        total_turns=1.0,
    )
    assert r.metric_created is True
    assert r.maql_correct is True


def test_agentic_metric_summary_pass_at_k():
    r = MetricRunResult("c1", {"maql": "x"}, True, "x", True, 1.0)
    s = AgenticMetricSummary(run_results=[r], pass_at_k=True, pass_power_k=True, best=r)
    assert s.pass_at_k is True


def test_run_agentic_metric_skill_creates_conversation(monkeypatch):
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )

    with _patched(mock_client):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is True
    assert summary.best.metric_created is True
    mock_client.close.assert_called_once()


def test_run_agentic_metric_skill_closes_client_on_no_result():
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I will work on that.",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with _patched(mock_client, simulated_reply="Go ahead and create it.") as (mock_sim, _):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=2,
        )
    mock_client.close.assert_called_once()
    assert summary.pass_at_k is False
    assert summary.best.metric_created is False
    mock_sim.assert_called_once_with("I will work on that.", [{"maql": "SELECT {metric/foo}"}], "Create metric foo")


def test_run_agentic_metric_skill_logs_simulated_user_timing(monkeypatch, capsys):
    monkeypatch.setenv(TIMERS_ENV_VAR, "1")
    mock_client = _client()
    mock_client.send_message.side_effect = [
        ChatResult.model_validate(
            {
                "textResponse": "Which field should I use?",
                "toolCallEvents": [],
                "reasoningStepCount": 1,
            }
        ),
        _create_metric_chat_result(),
    ]

    with _patched(mock_client, simulated_reply="Use the foo field.", sdk=True, monotonic=_CLOCK_TWO_TURNS):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
        )

    output = capsys.readouterr().out
    assert (
        "[timer] metric_skill conv-1 GoodData turn 1 complete after 1.00s; waiting for gpt-4o-mini simulated user"
        in output
    )
    assert "[timer] metric_skill conv-1 gpt-4o-mini simulated user complete after 2.50s" in output


def test_run_agentic_metric_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with _patched(mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_metric_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with _patched(mock_client):
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "x"},
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    # Runs 1 and 2 always create fresh; run 0 uses existing-conv
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


def test_delete_metric_uses_sdk_entities_api():
    sdk = MagicMock()
    _delete_metric(sdk, "ws1", "foo_metric")
    sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_delete_metric_swallows_failures():
    sdk = MagicMock()
    sdk._client.entities_api.delete_entity_metrics.side_effect = RuntimeError("500")
    # Cleanup is best-effort — a failed delete is logged, never propagated.
    _delete_metric(sdk, "ws1", "foo_metric")


def _create_metric_chat_result(metric_id: str = "foo_metric"):
    return ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": f'{{"data": {{"maql": "SELECT {{metric/foo}}", "metric_id": "{metric_id}"}}}}',
                }
            ],
            "reasoningStepCount": 1,
        }
    )


def test_run_agentic_metric_skill_deletes_created_metric():
    mock_client = _client()
    mock_client.send_message.return_value = _create_metric_chat_result()
    with _patched(mock_client, sdk=True) as (_, mock_sdk_cls):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    # The metric the run created is deleted on the way out, by its exact id, via the SDK.
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_deletes_the_metric_created_by_a_self_corrected_retry():
    """QA-29053 regression: a failed create_metric call followed by a successful retry, in the
    same turn, used to leave metric_id_to_delete unset -- the metric the retry created leaked
    into the shared workspace."""
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"isError": true, "error": {"text": "invalid MAQL"}}}',
                },
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}", "metric_id": "foo_metric"}}',
                },
            ],
            "reasoningStepCount": 1,
        }
    )
    with _patched(mock_client, sdk=True) as (_, mock_sdk_cls):
        mock_sdk = mock_sdk_cls.create.return_value
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert summary.best.metric_created is True
    assert summary.best.maql_correct is True
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_run_agentic_metric_skill_deletes_metric_even_when_teardown_fails():
    # A metric is created, then conversation teardown raises; the created metric must still
    # have been cleaned up (its deletion happens inside the per-run finally, before teardown).
    mock_client = _client()
    mock_client.send_message.return_value = _create_metric_chat_result()
    mock_client.delete_conversation.side_effect = RuntimeError("teardown boom")

    with (
        _patched(mock_client, sdk=True) as (_, mock_sdk_cls),
        pytest.raises(RuntimeError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def test_generate_simulated_response_without_an_api_key(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    with (
        patch.dict(sys.modules, {"openai": MagicMock()}),
        pytest.raises(SimulatedResponseError, match="OPENAI_API_KEY"),
    ):
        generate_simulated_response("Which brand field?", [{"maql": "SELECT {metric/foo}"}], "I need a metric for foo")


def test_generate_simulated_response_without_the_openai_package():
    with (
        patch.dict(sys.modules, {"openai": None}),
        pytest.raises(SimulatedResponseError, match="openai package is required"),
    ):
        generate_simulated_response("Which brand field?", [{"maql": "SELECT {metric/foo}"}], "I need a metric for foo")


def test_run_agentic_metric_skill_fails_the_run_when_the_simulated_reply_cannot_be_generated():
    exc = SimulatedResponseError("OPENAI_API_KEY environment variable is not set")
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "Which brand field should I count?",
            "toolCallEvents": [],
            "reasoningStepCount": 1,
        }
    )
    with _patched(mock_client, simulated_error=exc) as (mock_sim, _):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=3,
        )

    assert summary.pass_at_k is False
    assert summary.best.metric_created is False
    assert summary.best.total_turns == 1.0
    mock_client.close.assert_called_once()
    mock_sim.assert_called_once_with(
        "Which brand field should I count?", [{"maql": "SELECT {metric/foo}"}], "Create metric foo"
    )


def test_run_agentic_metric_skill_accumulates_reasoning_steps_across_iterations():
    clarify_turn = ChatResult.model_validate(
        {
            "textResponse": "Could you clarify which foo you mean?",
            "toolCallEvents": [],
            "reasoningSteps": ["step one"],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningSteps": ["step two"],
        }
    )
    mock_client = _client()
    mock_client.send_message.side_effect = [clarify_turn, created_turn]

    with _patched(mock_client, simulated_reply="It's foo"):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=2,
        )

    assert summary.best.reasoning_steps == ["step one", "step two"]


def test_evaluate_agentic_metric_skill_returns_reasoning_steps_on_pass():
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "done",
            "toolCallEvents": [
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": '{"data": {"maql": "SELECT {metric/foo}"}}',
                }
            ],
            "reasoningSteps": ["thinking about it"],
        }
    )
    with _patched(mock_client):
        outcome = evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert outcome.reasoning_steps == ["thinking about it"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id is None
    assert outcome.detail == {
        "metric_created": True,
        "maql_correct": True,
        "expected_maql_candidates": ["SELECT {metric/foo}"],
        "actual_maql": "SELECT {metric/foo}",
        "latency_breakdown": [],
    }


def test_evaluate_agentic_metric_skill_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = _client()
    mock_client.send_message.return_value = ChatResult.model_validate(
        {
            "textResponse": "I will work on that.",
            "toolCallEvents": [],
            "reasoningSteps": ["confused thinking"],
        }
    )
    with _patched(mock_client), pytest.raises(MetricSkillAssertionError) as exc_info:
        evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
            max_iterations=1,
        )
    assert exc_info.value.reasoning_steps == ["confused thinking"]
    assert exc_info.value.detail == {
        "metric_created": False,
        "maql_correct": False,
        "expected_maql_candidates": ["SELECT {metric/foo}"],
        "actual_maql": "",
        "latency_breakdown": [],
    }
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id is None


def test_records_agent_and_simulated_user_latency_separately():
    # metric_skill's OpenAI call is the simulated user, not a judge, and it sits ON the
    # critical path -- the next agent turn cannot be sent until the reply exists. Keeping
    # it in its own bucket is what makes that visible: agent_s is GoodData's cost across
    # both turns, simulated_user_s is ours.
    mock_client = _client()
    mock_client.send_message.side_effect = [
        ChatResult.model_validate(
            {"textResponse": "Which field should I use?", "toolCallEvents": [], "reasoningStepCount": 1}
        ),
        _create_metric_chat_result(),
    ]

    with _patched(mock_client, simulated_reply="Use the foo field.", sdk=True, monotonic=_CLOCK_TWO_TURNS):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
        )

    timings = summary.run_results[0].timings
    assert timings.agent_s == 1.5  # 1.0s turn 1 + 0.5s turn 2
    assert timings.simulated_user_s == 2.5
    # metric_skill has no judge; conflating its simulated user with one would misreport
    # a blocking call as a deferrable one.
    assert timings.judge_s == 0.0


def test_evaluate_metric_skill_surfaces_timings_on_the_outcome():
    # The item report reads timings off the outcome, so a kind that measures phases but
    # does not propagate them reports zeroes and looks instantaneous.
    mock_client = _client()
    mock_client.send_message.return_value = _create_metric_chat_result()

    with _patched(mock_client, sdk=True, monotonic=_CLOCK_ONE_TURN):
        outcome = evaluate_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
            k=1,
        )

    assert outcome.timings.agent_s == 3.0
    assert outcome.timings.simulated_user_s == 0.0


def test_no_timer_output_by_default(monkeypatch, capsys):
    # metric_skill emits four [timer] lines per turn-pair; on a multi-turn conversation
    # that is the bulk of the run's output. Off unless asked for.
    monkeypatch.delenv(TIMERS_ENV_VAR, raising=False)
    mock_client = _client()
    mock_client.send_message.return_value = _create_metric_chat_result()

    with _patched(mock_client, sdk=True, monotonic=_CLOCK_ONE_TURN):
        summary = run_agentic_metric_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create metric foo",
            expected_output={"maql": "SELECT {metric/foo}"},
        )

    assert "[timer]" not in capsys.readouterr().out
    # Silenced, not un-measured.
    assert summary.run_results[0].timings.agent_s == 3.0
