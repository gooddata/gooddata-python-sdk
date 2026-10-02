# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
import json as _json
import sys
import types
from datetime import date
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic import _conversation_context as ctx_mod
from gooddata_eval.core.agentic._conversation_context import (
    CONFIRMATION_REPLY,
    NO_ANSWER_REPLY,
    NUDGE_MESSAGE,
    ClarificationJudge,
    ClarificationVerdict,
    _ClarificationLLM,
    classify_reply,
    judge_prompt,
    reply_from_facts,
    reply_restating,
)
from gooddata_eval.core.agentic.conversation import (
    ConversationAssertionError,
    ConversationFixture,
    ConversationResult,
    TurnDefinition,
    TurnResult,
    _canonical_maql,
    _check_output_correct,
    _created_alert_ids,
    _expected_viz,
    _get_sim_user_response,
    _metric_creations,
    _resolve_refs,
    evaluate_agentic_conversation,
    resolve_conversation_mode,
    run_agentic_conversation,
)
from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ChatError, TurnIncompleteError
from gooddata_eval.core.chat.sse_client import ChatError as ChatError_
from gooddata_eval.core.evaluators._llm_judge import JudgeResponseError
from gooddata_eval.core.models import ChatResult, LoopExit, ToolCallEvent


def _skills_tc(*skills):
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    # `skill_names` is the key the real set_skills tool declares and reads. These tests
    # previously used a bare `skills`, which only passed via _activated_skills' fallback
    # spelling -- so they exercised a payload shape the platform never actually sends.
    tc.parsed_arguments = lambda: {"skill_names": list(skills)}
    return tc


def _create_metric_tc(metric_id):
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "create_metric"
    tc.result = "{}"  # truthy so cleanup collection processes it; content comes from parsed_result
    tc.parsed_result = lambda mid=metric_id: {"data": {"metric_id": mid, "maql": "SELECT 1"}}
    return tc


def _create_metric_tc_error(message):
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "create_metric"
    tc.result = "{}"  # truthy; content comes from parsed_result
    tc.parsed_result = lambda msg=message: {"data": {"isError": True, "error": {"text": msg}}}
    return tc


def _metric_turn_result(tool_calls):
    r = MagicMock()
    r.text_response = "done"
    r.created_visualizations = None
    r.tool_call_events = tool_calls
    r.reasoning_step_events = []
    r.turn_wall_clock_sec = None
    return r


def test_turn_definition_model():
    t = TurnDefinition(
        turn_id="t1",
        message="Make a chart",
        expected_skill="visualization",
        expected_output_type="visualization",
    )
    assert t.turn_id == "t1"


def test_conversation_fixture_model():
    f = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    assert len(f.turns) == 1


def test_turn_result_skill_success():
    r = TurnResult(
        turn_id="t1",
        expected_skill="visualization",
        skill_routing=True,
        output_present=True,
        no_error=True,
        activated_skills=["visualization"],
        clarification_turns_used=0,
        output_correct=None,
    )
    assert r.skill_success is True


def _turn_result() -> TurnResult:
    return TurnResult(
        turn_id="t1",
        expected_skill="visualization",
        skill_routing=True,
        output_present=True,
        no_error=True,
        activated_skills=["visualization"],
        clarification_turns_used=0,
        output_correct=None,
    )


def test_turn_result_detail_copies_activated_skills():
    """A caller mutating the returned dict must not reach back into the TurnResult."""
    r = _turn_result()
    d = r.detail()
    d["activated_skills"].append("mutated")
    assert r.activated_skills == ["visualization"]


def test_turn_result_detail_fields_all_exist_on_the_model():
    """_DETAIL_FIELDS is a hand-listed subset, so a renamed field must fail here rather
    than silently drop a key from every report."""
    assert set(TurnResult.model_fields) >= TurnResult._DETAIL_FIELDS
    assert set(_turn_result().detail()) == TurnResult._DETAIL_FIELDS | {"context_success", "failure_reasons"}


def test_resolve_refs_no_refs():
    assert _resolve_refs({"key": "value"}, {}) == {"key": "value"}


def test_resolve_refs_substitutes():
    turn_outputs = {"t1": {"maql": "SELECT {metric/foo}"}}
    result = _resolve_refs({"maql": "$ref:t1.maql"}, turn_outputs)
    assert result == {"maql": "SELECT {metric/foo}"}


def test_get_sim_user_response_metric_branch_forwards_the_turn_message():
    """QA-29094 follow-up: every test in this file patches out `_get_sim_user_response`
    itself, so its metric branch (which forwards to
    ``metric_skill.generate_simulated_response``) had 0% coverage -- a future signature
    change there would raise inside the bare ``except Exception`` and silently fall through
    to the generic fallback prompt instead of failing loudly."""
    turn = TurnDefinition(
        turn_id="t1",
        message="I need a metric for total ordered units",
        expected_skill="metric",
        expected_output_type="metric",
    )
    expected_output = {"maql": "SELECT SUM({fact/order_unit_quantity})"}

    with patch(
        "gooddata_eval.core.agentic.metric_skill.generate_simulated_response",
        return_value="Yes, that works.",
    ) as mock_sim:
        reply = _get_sim_user_response("Should I create this metric?", turn, expected_output)

    assert reply == "Yes, that works."
    mock_sim.assert_called_once_with("Should I create this metric?", [expected_output], turn.message)


def test_run_agentic_conversation_single_turn():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    mock_chat_result.tool_call_events = [tc]
    mock_chat_result.reasoning_step_events = []
    mock_chat_result.turn_wall_clock_sec = None
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.conversation_id == "conv-1"
    assert len(result.turn_results) == 1
    mock_client.close.assert_called_once()


def test_run_agentic_conversation_uses_initial_conversation_id():
    mock_client = MagicMock()
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result.tool_call_events = [tc]
    mock_chat_result.reasoning_step_events = []
    mock_chat_result.turn_wall_clock_sec = None
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
            initial_conversation_id="existing-conv",
        )
    assert result.conversation_id == "existing-conv"
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_conversation_creates_and_deletes_conversation():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "new-conv"
    mock_chat_result = MagicMock()
    mock_chat_result.text_response = "Here is your visualization"
    mock_chat_result.created_visualizations = [MagicMock()]
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    mock_chat_result.tool_call_events = [tc]
    mock_chat_result.reasoning_step_events = []
    mock_chat_result.turn_wall_clock_sec = None
    mock_client.send_message.return_value = mock_chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )
    assert result.conversation_id == "new-conv"
    mock_client.create_conversation.assert_called_once()
    mock_client.delete_conversation.assert_called_once_with("new-conv")


def test_run_agentic_conversation_deletes_created_metrics():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _metric_turn_result([_skills_tc("metric"), _create_metric_tc("foo_metric")])

    fixture = ConversationFixture(
        id="test-metric",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Create a metric counting x",
                expected_skill="metric",
                expected_output_type="metric",
            )
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )
    # The metric created during the conversation is deleted after it completes, via the SDK.
    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "foo_metric")


def _two_metric_turn_fixture():
    return ConversationFixture(
        id="test-multi",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(
                turn_id="t1", message="Create shared", expected_skill="metric", expected_output_type="metric"
            ),
            TurnDefinition(
                turn_id="t2", message="Create extra", expected_skill="metric", expected_output_type="metric"
            ),
        ],
    )


def test_run_agentic_conversation_deletes_every_unique_metric_across_turns():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    # Turn 1 creates "shared"; turn 2 re-creates "shared" (duplicate) and adds "extra".
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("shared")]),
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("shared"), _create_metric_tc("extra")]),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    # Metrics from all turns are cleaned up, and each unique id is deleted exactly once.
    deleted = sorted(c.args for c in mock_sdk._client.entities_api.delete_entity_metrics.call_args_list)
    assert deleted == [("ws1", "extra"), ("ws1", "shared")]


def test_run_agentic_conversation_skill_routing_persists_across_turns():
    """A skill activated in an earlier turn stays credited when a later turn reuses it
    without re-issuing set_skills -- the platform keeps a skill active once set, so an
    agent correctly omits a redundant set_skills call. Requiring a fresh call every turn
    produced false FAILs on turns that did the right thing (found via
    debug_conversation.py replaying analyst-explores-dynamic-currency-conversion,
    turns t4/t5: create_adhoc_visualization/create_metric both ran and succeeded, but
    skill_routing was False solely because set_skills wasn't repeated)."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        _metric_turn_result([_create_metric_tc("m2")]),  # no set_skills -- skill already active
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    assert result.turn_results[0].skill_routing is True
    assert result.turn_results[1].skill_routing is True

    # The two fields measure different scopes (see TurnResult's docstring), so the reused
    # turn reports routing credit alongside an empty own-declarations list. Asserted so the
    # combination is pinned as intended output rather than read as a scoring bug by whoever
    # triages the report next.
    assert result.turn_results[0].activated_skills == ["metric"]
    assert result.turn_results[1].activated_skills == []
    # active_skills shows where t2's credit came from -- without it, skill_routing=True
    # next to an empty activated_skills reads as a scoring bug.
    assert result.turn_results[0].active_skills == ["metric"]
    assert result.turn_results[1].active_skills == ["metric"]


def test_run_agentic_conversation_skill_routing_false_after_a_later_call_deactivates_it():
    """set_skills REPLACES the active set, so a skill dropped by a later call is no longer
    active and must lose routing credit.

    Replace-not-append was verified against the gen-ai service's skill registry, and is
    stated in the set_skills tool's own description. Tracking activations as a running
    union instead would credit `metric` on t3 here even though t2 switched it off --
    turning the false FAIL this PR fixes into a false PASS, which is worse: it reports a
    broken conversation as working.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        # t1 activates metric and uses it.
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        # t2 replaces the active set with visualization -- metric is now OFF.
        _metric_turn_result([_skills_tc("visualization"), _create_metric_tc("m2")]),
        # t3 expects metric and declares nothing, so it inherits t2's set: no metric.
        _metric_turn_result([_create_metric_tc("m3")]),
    ]

    fixture = ConversationFixture(
        id="test-deactivated",
        expected_skills=["metric", "visualization"],
        turns=[
            TurnDefinition(turn_id="t1", message="Create a", expected_skill="metric", expected_output_type="metric"),
            TurnDefinition(
                turn_id="t2", message="Chart it", expected_skill="visualization", expected_output_type="metric"
            ),
            TurnDefinition(turn_id="t3", message="Create b", expected_skill="metric", expected_output_type="metric"),
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.turn_results[0].skill_routing is True  # metric active
    assert result.turn_results[1].skill_routing is True  # visualization active, replaced metric
    assert result.turn_results[2].skill_routing is False  # metric was deactivated by t2
    assert result.turn_results[2].active_skills == ["visualization"]


def test_run_agentic_conversation_only_the_last_set_skills_call_in_a_turn_counts():
    """Several set_skills calls can land within one logical turn (its clarification
    sub-turns share one tool-call list). Since each call replaces the active set, only the
    final one describes the result -- merging them would credit `metric` here even though
    the same turn went on to replace it with `visualization`.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _metric_turn_result(
        [_skills_tc("metric"), _skills_tc("visualization"), _create_metric_tc("m1")]
    )

    fixture = ConversationFixture(
        id="test-last-call-wins",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(turn_id="t1", message="Create a", expected_skill="metric", expected_output_type="metric"),
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.turn_results[0].active_skills == ["visualization"]
    assert result.turn_results[0].activated_skills == ["visualization"]
    assert result.turn_results[0].skill_routing is False  # metric was replaced within the turn
    # ...but `metric` WAS exercised, so coverage still holds. The two metrics ask different
    # questions and must not be derived from the same field.
    assert result.full_skill_coverage is True


def test_run_agentic_conversation_coverage_counts_a_skill_replaced_within_its_own_turn():
    """full_skill_coverage asks "was every expected skill ever exercised", which is
    cumulative over ALL declarations -- unlike skill_routing, which asks what is active now.

    Deriving it from TurnResult.activated_skills (each turn's FINAL declaration) drops any
    skill a turn declared and then replaced across its own clarification sub-turns: a false
    FAIL on a skill that genuinely ran. Only bites within a turn, which is why every other
    coverage test -- one declaration per turn -- stays green either way.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    # Sub-turn 1 routes to `metric` but produces no output, triggering a clarification
    # round; sub-turn 2 replaces the active set with `visualization` and completes.
    clarification = MagicMock()
    clarification.text_response = "which measure did you mean?"
    clarification.created_visualizations = None
    clarification.tool_call_events = [_skills_tc("metric")]
    clarification.reasoning_step_events = []
    clarification.turn_wall_clock_sec = None
    clarification.alert_proposals = None
    mock_client.send_message.side_effect = [
        clarification,
        _metric_turn_result([_skills_tc("visualization"), _create_metric_tc("m1")]),
    ]

    fixture = ConversationFixture(
        id="test-coverage-within-turn",
        expected_skills=["metric", "visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1", message="Chart revenue", expected_skill="visualization", expected_output_type="metric"
            ),
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.conversation._get_sim_user_response", return_value="revenue"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.turn_results[0].activated_skills == ["visualization"]
    assert result.turn_results[0].active_skills == ["visualization"]
    assert result.full_skill_coverage is True


def test_run_agentic_conversation_an_empty_set_skills_call_clears_active_skills():
    """`set_skills([])` is a real declaration -- it deactivates everything -- so it must be
    distinguishable from making no call at all, which carries the previous set over.
    Treating both as "nothing declared" would leave t2 credited for t1's skill.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        _metric_turn_result([_skills_tc(), _create_metric_tc("m2")]),  # set_skills([]) -- clears
    ]

    fixture = ConversationFixture(
        id="test-explicit-clear",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(turn_id="t1", message="Create a", expected_skill="metric", expected_output_type="metric"),
            TurnDefinition(turn_id="t2", message="Create b", expected_skill="metric", expected_output_type="metric"),
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.turn_results[0].skill_routing is True
    assert result.turn_results[1].skill_routing is False  # cleared, not carried over
    assert result.turn_results[1].active_skills == []


def test_run_agentic_conversation_skill_routing_false_when_skill_never_activated():
    """Guard against the fix being too lenient: a skill that no turn ever activated
    must still fail routing, not be credited by the cumulative-set change."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _metric_turn_result([_create_metric_tc("m1")])

    fixture = ConversationFixture(
        id="test-never-activated",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(turn_id="t1", message="Create x", expected_skill="metric", expected_output_type="metric"),
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.turn_results[0].skill_routing is False


def test_run_agentic_conversation_deletes_metrics_even_when_a_later_turn_raises():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    # Turn 1 creates "m1"; turn 2 blows up mid-run — the finally must still clean up "m1".
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        RuntimeError("boom"),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk") as mock_sdk_cls,
        pytest.raises(RuntimeError),
    ):
        mock_sdk = mock_sdk_cls.create.return_value
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    mock_sdk._client.entities_api.delete_entity_metrics.assert_called_once_with("ws1", "m1")


def _alert_turn_fixture():
    return ConversationFixture(
        id="conv-alert",
        expected_skills=["alert"],
        turns=[
            TurnDefinition(
                turn_id="create_alert",
                message="Now alert me when the metric drops below 100.",
                expected_skill="alert",
                expected_output_type="tool_call",
                expected_tool_name="create_metric_alert",
            )
        ],
    )


def test_run_agentic_conversation_treats_alert_proposal_as_a_clarification():
    """GDAI-2032 regression: a proposal-only turn has no text, so the old text-only check
    stopped the turn instead of replying, and create_metric_alert never happened."""
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [{"cta": "Should I create this alert?", "recipients": [{"email": "a@b.com"}]}],
            "toolCallEvents": [
                {"functionName": "set_skills", "functionArguments": '{"skills": ["alert"]}', "result": None},
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None},
            ],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "toolCallEvents": [
                {"functionName": "create_metric_alert", "functionArguments": "{}", "result": '{"id": "alert-1"}'}
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch(
            "gooddata_eval.core.agentic.conversation._get_sim_user_response",
            return_value="Yes, please create it.",
        ) as mock_sim,
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_alert_turn_fixture(),
        )

    assert "Should I create this alert?" in mock_sim.call_args.args[0]
    assert result.turn_results[0].clarification_turns_used == 1
    assert result.turn_results[0].skill_success is True


def _viz_turn_result(text=None, viz=None, tool_calls=()):
    r = MagicMock()
    r.text_response = text
    r.created_visualizations = viz
    r.tool_call_events = list(tool_calls)
    r.reasoning_step_events = []
    r.turn_wall_clock_sec = None
    r.alert_proposals = []
    return r


def test_run_agentic_conversation_replies_to_a_statement_without_a_question_mark():
    """QA-28982 regression: gpt-5.2 answered "I need to confirm ... Next I'll:" -- no question
    mark, so the old substring heuristic ended the turn and no metric was ever created."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    stalling_turn = _viz_turn_result(
        text="I can create that, but first I need to confirm which Net Sales calculation to use. Next I'll: ...",
        tool_calls=[_skills_tc("metric")],
    )
    mock_client.send_message.side_effect = [
        stalling_turn,
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch(
            "gooddata_eval.core.agentic.conversation._get_sim_user_response",
            return_value="Go ahead with Net Sales.",
        ) as mock_sim,
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture().model_copy(update={"turns": _two_metric_turn_fixture().turns[:1]}),
        )

    mock_sim.assert_called_once()
    assert result.turn_results[0].clarification_turns_used == 1
    assert result.turn_results[0].skill_success is True


def test_run_agentic_conversation_stops_when_the_agent_says_nothing():
    """An agent that returns neither text nor tool calls is stuck -- no point replying to it."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _viz_turn_result(text=None)

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.conversation._get_sim_user_response") as mock_sim,
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture().model_copy(update={"turns": _two_metric_turn_fixture().turns[:1]}),
        )

    mock_sim.assert_not_called()
    assert mock_client.send_message.call_count == 1
    assert result.turn_results[0].skill_success is False


def test_run_agentic_conversation_records_a_failed_turn_when_a_ref_cannot_be_resolved():
    """QA-28982 regression: turn 1 producing no metric used to raise ValueError out of the whole
    run, hiding which turn broke and skipping every later turn."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _viz_turn_result(text="Which Net Sales metric?", tool_calls=[_skills_tc("metric")]),
        _viz_turn_result(text="Working on it.", tool_calls=[_skills_tc("metric")]),
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m2")]),
    ]
    fixture = ConversationFixture(
        id="test-ref",
        expected_skills=["metric"],
        turns=[
            TurnDefinition(
                turn_id="t1", message="Create shared", expected_skill="metric", expected_output_type="metric"
            ),
            TurnDefinition(
                turn_id="t2",
                message="Chart it",
                expected_skill="visualization",
                expected_output={"metrics": ["metric/$ref:t1.metric_id"]},
            ),
            TurnDefinition(
                turn_id="t3", message="Create another", expected_skill="metric", expected_output_type="metric"
            ),
        ],
    )

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.conversation._get_sim_user_response", return_value="Go ahead."),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
            max_clarification_turns=1,
        )

    assert [t.turn_id for t in result.turn_results] == ["t1", "t2", "t3"]
    assert result.turn_results[0].skill_success is False
    assert result.turn_results[1].no_error is False
    assert result.turn_results[2].skill_success is True
    assert result.conversation_success is False


def test_run_agentic_conversation_sends_the_next_turn_after_a_self_corrected_retry():
    """QA-29053 regression: turn 1 self-corrects create_metric after a failed first attempt;
    turn 2's message must still be sent, resolving its $ref against the successful retry."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc_error("invalid MAQL"), _create_metric_tc("m1")]),
        _viz_turn_result(text="Here is your chart", viz=[MagicMock()], tool_calls=[_skills_tc("visualization")]),
    ]
    fixture = ConversationFixture(
        id="test-retry",
        expected_skills=["metric", "visualization"],
        turns=[
            TurnDefinition(turn_id="t1", message="Create it", expected_skill="metric", expected_output_type="metric"),
            TurnDefinition(
                turn_id="t2",
                message="Chart it",
                expected_skill="visualization",
                expected_output={"metrics": ["metric/$ref:t1.metric_id"]},
            ),
        ],
    )

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert mock_client.send_message.call_count == 2
    mock_client.send_message.assert_any_call("conv-1", "Chart it")
    assert result.turn_results[0].skill_success is True
    assert result.turn_results[1].no_error is True
    assert result.conversation_success is True


def test_run_agentic_conversation_accumulates_reasoning_steps_across_turns():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}

    turn1_result = MagicMock()
    turn1_result.text_response = "Here is your visualization"
    turn1_result.created_visualizations = [MagicMock()]
    turn1_result.tool_call_events = [tc]
    turn1_result.reasoning_step_events = []
    turn1_result.turn_wall_clock_sec = None
    turn1_result.reasoning_steps = ["turn one reasoning"]

    turn2_result = MagicMock()
    turn2_result.text_response = "Here is another visualization"
    turn2_result.created_visualizations = [MagicMock()]
    turn2_result.tool_call_events = [tc]
    turn2_result.reasoning_step_events = []
    turn2_result.turn_wall_clock_sec = None
    turn2_result.reasoning_steps = ["turn two reasoning"]

    mock_client.send_message.side_effect = [turn1_result, turn2_result]

    fixture = ConversationFixture(
        id="test-reasoning",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            ),
            TurnDefinition(
                turn_id="t2",
                message="Make another chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            ),
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )

    assert result.reasoning_steps == ["turn one reasoning", "turn two reasoning"]


def test_evaluate_agentic_conversation_returns_reasoning_steps_on_pass():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["visualization"]}
    chat_result = MagicMock()
    chat_result.text_response = "Here is your visualization"
    chat_result.created_visualizations = [MagicMock()]
    chat_result.tool_call_events = [tc]
    chat_result.reasoning_step_events = []
    chat_result.turn_wall_clock_sec = None
    chat_result.reasoning_steps = ["thinking about it"]
    chat_result.response_id = "resp-1"
    mock_client.send_message.return_value = chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client):
        outcome = evaluate_agentic_conversation(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
        )
    assert outcome.reasoning_steps == ["thinking about it"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id == "resp-1"
    assert outcome.detail == {
        "mode": "legacy",
        "full_skill_coverage": True,
        "conversation_success": True,
        "context_success": True,
        "context_kept_rate": None,
        "turns_before_first_break": 1,
        "lost_context_clarifications": 0,
        "stalled_turns": 0,
        "total_clarification_turns": 0,
        "max_clarification_turns": 7,
        "judge_model": None,
        "turns": [
            {
                "turn_id": "t1",
                "expected_skill": "visualization",
                "skill_routing": True,
                "output_present": True,
                "output_correct": None,
                "activated_skills": ["visualization"],
                "active_skills": ["visualization"],
                "exit_reason": "success",
                "clarification_turns_used": 0,
                "mismatches": [],
                "clarifications": [],
                "depends_on": [],
                "context_success": True,
                "failure_reasons": [],
            }
        ],
        "latency_breakdown": [],
        "tool_calls": [],
    }


def test_evaluate_agentic_conversation_attaches_reasoning_steps_to_exception_on_fail():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    tc = MagicMock(spec=ToolCallEvent)
    tc.call_ts = None
    tc.result_ts = None
    tc.index = None
    tc.function_name = "set_skills"
    tc.parsed_arguments = lambda: {"skills": ["other_skill"]}
    chat_result = MagicMock()
    chat_result.text_response = "Here is something else"
    chat_result.created_visualizations = None
    chat_result.tool_call_events = [tc]
    chat_result.reasoning_step_events = []
    chat_result.turn_wall_clock_sec = None
    chat_result.alert_proposals = []
    chat_result.reasoning_steps = ["confused thinking"]
    chat_result.response_id = "resp-2"
    mock_client.send_message.return_value = chat_result

    fixture = ConversationFixture(
        id="test-1",
        expected_skills=["visualization"],
        turns=[
            TurnDefinition(
                turn_id="t1",
                message="Make a chart",
                expected_skill="visualization",
                expected_output_type="visualization",
            )
        ],
    )
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        pytest.raises(ConversationAssertionError) as exc_info,
    ):
        evaluate_agentic_conversation(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            fixture=fixture,
            max_clarification_turns=0,
        )
    assert exc_info.value.reasoning_steps == ["confused thinking"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id == "resp-2"
    assert exc_info.value.detail == {
        "mode": "legacy",
        "full_skill_coverage": False,
        "conversation_success": False,
        "context_success": False,
        "context_kept_rate": None,
        "turns_before_first_break": 0,
        "lost_context_clarifications": 0,
        "stalled_turns": 1,
        "total_clarification_turns": 0,
        "max_clarification_turns": 0,
        "judge_model": None,
        "turns": [
            {
                "turn_id": "t1",
                "expected_skill": "visualization",
                "skill_routing": False,
                "output_present": False,
                "output_correct": None,
                "activated_skills": ["other_skill"],
                "active_skills": ["other_skill"],
                # Output never appeared and the clarification budget ran out -- the turn is
                # not a refusal, which skill_routing/output_present alone cannot show.
                "exit_reason": "budget_exhausted",
                "clarification_turns_used": 0,
                "mismatches": [],
                "clarifications": [
                    {
                        "kind": "no_action",
                        "agent_message": "Here is something else",
                        "lost_context": None,
                        "reasoning": "",
                        "judge_error": None,
                        "judge_input": "",
                        "reply": "",
                    }
                ],
                "depends_on": [],
                "context_success": False,
                "failure_reasons": [
                    "no output of the expected type",
                    "ended a reply without the expected output and without asking anything",
                ],
            }
        ],
        "latency_breakdown": [],
        "tool_calls": [],
    }


def test_a_chat_error_ends_only_its_own_turn_and_is_recorded():
    """A chat fault used to escape the whole conversation, discarding the turns already done.

    t1 completes; t2's chat call fails. t1's result must survive, and t2 must be reported as
    an infrastructure fault -- both exit_reason and no_error say so, so it is not counted as
    the agent failing to produce output.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        ChatError("stream died"),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    assert len(result.turn_results) == 2
    assert result.turn_results[0].exit_reason is LoopExit.SUCCESS
    assert result.turn_results[0].output_present is True

    assert result.turn_results[1].exit_reason is LoopExit.CHAT_ERROR
    assert result.turn_results[1].output_present is False
    # no_error used to be hardcoded True on the reasoning that a chat fault would have
    # escaped before reaching here. Now that it is caught, it has to read the exit back.
    assert result.turn_results[1].no_error is False
    assert result.turn_results[1].skill_success is False


def test_a_partial_result_joins_the_shared_timeline_like_any_other_turn():
    """What the stream delivered before it died is still the turn's work.

    Each turn's SSE stream times from ~0 and indexes from 0, so a late turn's events have to
    be rebased before they can be merged. The success path does that; the ChatError branch
    used to extend the conversation lists with the raw partial, which put a second-turn tool
    call at call_ts 0.5 alongside the first turn's -- `timeline_detail` then reported two
    turns overlapping, with duplicate indexes. Its reasoning steps were dropped from
    total_steps for the same reason.
    """
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"

    first = _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")])
    first.turn_wall_clock_sec = 12.0
    first.reasoning_step_count = 2

    partial = ChatResult.model_validate(
        {
            "textResponse": "",
            "toolCallEvents": [
                {"functionName": "create_metric", "functionArguments": "{}", "call_ts": 0.5, "index": 0}
            ],
            "reasoningStepCount": 3,
            "streamEnded": False,
        }
    )
    mock_client.send_message.side_effect = [first, ChatError("stream died", partial_result=partial)]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )

    assert result.turn_results[1].exit_reason is LoopExit.CHAT_ERROR
    # Shifted by the first turn's wall clock, and indexed past the first turn's two calls.
    shifted = [tc for tc in result.tool_call_events if tc.call_ts is not None]
    assert [tc.call_ts for tc in shifted] == [12.5]
    assert [tc.index for tc in shifted] == [2]
    # The steps were taken, so they count.
    assert result.total_steps == 5


def test_a_non_chat_exception_still_propagates():
    """Only chat faults are absorbed. A programming error must not be relabelled CHAT_ERROR."""
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [
        _metric_turn_result([_skills_tc("metric"), _create_metric_tc("m1")]),
        TypeError("a real bug"),
    ]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        pytest.raises(TypeError),
    ):
        run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_two_metric_turn_fixture(),
        )


def test_run_agentic_conversation_sums_the_reasoning_steps_of_every_turn():
    """QA-29110: the effort comparison reads `steps`. A clarification round is part of the
    work the effort setting changes, so its steps count with the rest."""
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [{"cta": "Should I create this alert?", "recipients": [{"email": "a@b.com"}]}],
            "reasoningStepCount": 2,
            "toolCallEvents": [
                {"functionName": "set_skills", "functionArguments": '{"skills": ["alert"]}', "result": None},
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None},
            ],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "reasoningStepCount": 3,
            "toolCallEvents": [
                {"functionName": "create_metric_alert", "functionArguments": "{}", "result": '{"id": "alert-1"}'}
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch(
            "gooddata_eval.core.agentic.conversation._get_sim_user_response",
            return_value="Yes, please create it.",
        ),
    ):
        result = run_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_alert_turn_fixture(),
        )

    assert result.total_steps == 5
    assert result.total_clarification_turns == 1


def test_conversation_writes_the_turn_step_and_clarification_counts_to_langfuse():
    """`turns` is not the clarification count: it is one per fixture turn plus every
    simulated-user round, so a test has to pin the sum rather than either half."""
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [{"cta": "Should I create this alert?", "recipients": [{"email": "a@b.com"}]}],
            "reasoningStepCount": 2,
            "toolCallEvents": [
                {"functionName": "set_skills", "functionArguments": '{"skills": ["alert"]}', "result": None},
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None},
            ],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "reasoningStepCount": 3,
            "toolCallEvents": [
                {"functionName": "create_metric_alert", "functionArguments": "{}", "result": '{"id": "alert-1"}'}
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.side_effect = [proposal_turn, created_turn]
    captured = {}

    def _capture(_submit, _identity, **kwargs):
        captured["write_scores"] = kwargs["write_scores"]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=mock_client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.conversation.submit_trace_scoring", _capture),
        patch(
            "gooddata_eval.core.agentic.conversation._get_sim_user_response",
            return_value="Yes, please create it.",
        ),
    ):
        evaluate_agentic_conversation(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            fixture=_alert_turn_fixture(),
            langfuse=MagicMock(),
            dataset_item_id="item-1",
        )

    ctx = MagicMock()
    captured["write_scores"](ctx)
    scores = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}

    assert scores["clarification_turns"] == 1
    assert scores["turns"] == 2  # 1 fixture turn + 1 clarification round
    assert scores["steps"] == 5


def _viz(
    metric: str = "metric/gross_margin_percent",
    dim: str = "label/dim_store.store_format",
    filters: dict | None = None,
    sort: list[dict] | None = None,
) -> dict:
    query: dict = {"fields": {"m": {"using": metric}, "d": {"using": dim}}, "filter_by": filters or {}}
    if sort:
        query["sort_by"] = sort
    return {"type": "bar_chart", "query": query, "metrics": ["m"], "view_by": ["d"]}


_EXPRESS = {
    "f": {"type": "attribute_filter", "using": "label/dim_store.store_format", "state": {"include": ["Express"]}}
}


def _tool(name: str, args: dict | None = None, result: object = None) -> dict:
    return {
        "functionName": name,
        "functionArguments": _json.dumps(args or {}),
        "result": _json.dumps(result) if result is not None else None,
    }


def _result(
    text: str | None = "Done", viz: dict | None = None, tools: list[dict] | None = None, **extra: object
) -> ChatResult:
    payload: dict = {"textResponse": text, "toolCallEvents": tools or []}
    if viz is not None:
        payload["createdVisualizations"] = {"objects": [viz]}
    payload.update(extra)
    return ChatResult.model_validate(payload)


def _viz_turn(turn_id: str = "t1", expected: dict | None = None, **kw: object) -> TurnDefinition:
    return TurnDefinition(
        turn_id=turn_id,
        message=kw.pop("message", "chart it"),
        expected_skill="visualization",
        expected_output={"visualization": expected} if expected is not None else None,
        **kw,
    )


def test_output_correct_reads_the_wrapped_visualization_and_passes_an_identical_chart() -> None:
    ok, diff = _check_output_correct(_viz_turn(expected=_viz(filters=_EXPRESS)), _result(viz=_viz(filters=_EXPRESS)))
    assert (ok, diff) == (True, [])


def test_output_correct_fails_a_chart_that_dropped_an_established_filter() -> None:
    ok, diff = _check_output_correct(_viz_turn(expected=_viz(filters=_EXPRESS)), _result(viz=_viz()))
    assert ok is False
    assert any(d.startswith("attribute filters") for d in diff)


def test_output_correct_fails_a_filter_nobody_asked_for() -> None:
    ok, diff = _check_output_correct(_viz_turn(expected=_viz()), _result(viz=_viz(filters=_EXPRESS)))
    assert ok is False
    assert any(d.startswith("attribute filters") for d in diff)


def test_output_correct_fails_a_different_metric() -> None:
    ok, diff = _check_output_correct(_viz_turn(expected=_viz()), _result(viz=_viz(metric="metric/units_sold")))
    assert ok is False
    assert diff[0].startswith("metrics")


def test_output_correct_accepts_any_listed_alternative() -> None:
    turn = _viz_turn(expected=_viz(filters=_EXPRESS), expected_output_alternatives=[{"visualization": _viz()}])
    assert _check_output_correct(turn, _result(viz=_viz()))[0] is True


def test_output_correct_checks_sort_only_when_expected_states_it() -> None:
    sort = [{"type": "metric_sort", "direction": "DESC", "metrics": ["m"]}]
    assert _check_output_correct(_viz_turn(expected=_viz()), _result(viz=_viz(sort=sort)))[0] is True
    ok, diff = _check_output_correct(_viz_turn(expected=_viz(sort=sort)), _result(viz=_viz()))
    assert ok is False
    assert diff[0].startswith("sort")


def test_output_correct_sort_without_a_direction_matches_either_direction() -> None:
    by_units = [{"type": "metric_sort", "metrics": ["m"]}]
    asc = [{"type": "metric_sort", "direction": "ASC", "metrics": ["m"]}]
    assert _check_output_correct(_viz_turn(expected=_viz(sort=by_units)), _result(viz=_viz(sort=asc)))[0] is True
    desc = [{"type": "metric_sort", "direction": "DESC", "metrics": ["m"]}]
    assert _check_output_correct(_viz_turn(expected=_viz(sort=desc)), _result(viz=_viz(sort=asc)))[0] is False


def test_output_correct_is_unknown_when_nothing_is_expected() -> None:
    assert _check_output_correct(_viz_turn(), _result(viz=_viz())) == (None, [])


def test_output_correct_compares_tool_arguments_across_the_turn() -> None:
    turn = TurnDefinition(
        turn_id="a",
        message="alert me",
        expected_skill="alert",
        expected_output_type="tool_call",
        expected_tool_name="create_metric_alert",
        expected_tool_args={"metric_id": "units_sold", "threshold": 25},
    )
    call = ToolCallEvent.model_validate(_tool("create_metric_alert", {"metric_id": "units_sold", "threshold": 25}))
    wrong = ToolCallEvent.model_validate(_tool("create_metric_alert", {"metric_id": "units_sold", "threshold": 250}))
    assert _check_output_correct(turn, _result(), [call])[0] is True
    assert _check_output_correct(turn, _result(), [wrong])[0] is False


def test_output_correct_compares_maql_for_a_metric_turn() -> None:
    turn = TurnDefinition(
        turn_id="m",
        message="make it",
        expected_skill="metric",
        expected_output_type="metric",
        expected_output={"maql": "SELECT {metric/a} / {metric/b}"},
    )
    good = ToolCallEvent.model_validate(
        _tool("create_metric", result={"data": {"metric_id": "x", "maql": "SELECT {metric/a}/{metric/b}"}})
    )
    bad = ToolCallEvent.model_validate(
        _tool("create_metric", result={"data": {"metric_id": "x", "maql": "SELECT {metric/a}"}})
    )
    assert _check_output_correct(turn, _result(), [good])[0] is True
    assert _check_output_correct(turn, _result(), [bad])[0] is False


@pytest.mark.parametrize(
    ("result", "kind"),
    [
        (_result(text="Formula: SELECT 1. Should I create this metric?"), "confirmation"),
        (_result(text=None, alertProposals=[{"cta": "Create?"}]), "confirmation"),
        (_result(text="Which revenue metric do you mean?"), "question"),
        (_result(text="Please select one of the five options by number, name, or ID."), "question"),
        (_result(text="Reply with the number of the dashboard to use."), "question"),
        (_result(text="Let me check what that maps to."), "no_action"),
        (_result(text=None), "no_action"),
        (_result(text="Pick one", unhandledParts=[{"type": "clarifyingQuestions"}]), "question"),
    ],
)
def test_classify_reply(result: ChatResult, kind: str) -> None:
    assert classify_reply(result, result.text_response or render_answer_text(result)) == kind


def test_resolve_conversation_mode(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("GD_EVAL_CONVERSATION_MODE", raising=False)
    assert resolve_conversation_mode() == "legacy"
    monkeypatch.setenv("GD_EVAL_CONVERSATION_MODE", "context")
    assert resolve_conversation_mode() == "context"
    assert resolve_conversation_mode("legacy") == "legacy"
    with pytest.raises(ValueError, match="legacy"):
        resolve_conversation_mode("strict")


class _FakeJudge:
    """Grades every question with a fixed verdict and records what it was shown."""

    model_name = "fake-judge"

    def __init__(self, lost_context: bool | None) -> None:
        self.lost_context = lost_context
        self.calls: list[tuple[str, str, str]] = []

    def judge(self, history: str, latest: str, question: str) -> ClarificationVerdict:
        self.calls.append((history, latest, question))
        return ClarificationVerdict(lost_context=self.lost_context, reasoning="because")


_SKILLS = _tool("set_skills", {"skill_names": ["visualization"]})


def _run(
    replies: list, turns: list[TurnDefinition], mode: str = "context", judge: _FakeJudge | None = None, **kw: object
) -> tuple[ConversationResult, MagicMock]:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = replies
    fixture = ConversationFixture(id="c", expected_skills=["visualization"], turns=turns)
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
    ):
        result = run_agentic_conversation(
            host="h", token="t", workspace_id="ws", fixture=fixture, mode=mode, clarification_judge=judge, **kw
        )
    return result, client


def test_context_mode_fails_a_turn_that_asks_for_what_the_conversation_established() -> None:
    turns = [
        _viz_turn("t1", expected=_viz()),
        _viz_turn("t2", expected=_viz(filters=_EXPRESS), message="its margin?", depends_on=["t1"]),
    ]
    judge = _FakeJudge(lost_context=True)
    with patch(
        "gooddata_eval.core.agentic.conversation.reply_restating", return_value="As I said earlier, Express."
    ) as restate:
        result, client = _run(
            [
                _result(viz=_viz(), tools=[_SKILLS]),
                _result(text="Which store format do you mean?"),
                _result(viz=_viz(filters=_EXPRESS)),
            ],
            turns,
            judge=judge,
        )
    t2 = result.turn_results[1]
    assert t2.skill_success is True  # the legacy verdict still passes it
    assert t2.lost_context is True
    assert t2.context_success is False
    assert "asked for information the conversation already established" in t2.failure_reasons()
    assert result.conversation_success is True
    assert result.context_success is False
    assert result.context_kept_rate == 0.0
    assert result.turns_before_first_break == 1
    assert result.lost_context_clarifications == 1
    restate.assert_called_once()
    assert client.send_message.call_args_list[2].args[1] == "As I said earlier, Express."
    history, latest, question = judge.calls[0]
    assert "chart it" in history
    assert latest == "its margin?"
    assert "its margin?" in t2.clarifications[0].judge_input
    assert question == "Which store format do you mean?"


def test_context_mode_sends_the_set_answer_to_a_legitimate_question() -> None:
    turns = [_viz_turn("t1", expected=_viz(), message="revenue by format", set_answers=["Gross Margin Percent."])]
    result, client = _run(
        [_result(text="Which metric do you mean?"), _result(viz=_viz(), tools=[_SKILLS])],
        turns,
        judge=_FakeJudge(lost_context=False),
    )
    assert client.send_message.call_args_list[1].args[1] == "Gross Margin Percent."
    assert result.turn_results[0].context_success is True
    assert result.turn_results[0].clarifications[0].reply == "Gross Margin Percent."


def test_context_mode_answers_a_confirmation_with_yes_and_does_not_count_it_against_the_turn() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    judge = _FakeJudge(lost_context=True)
    result, client = _run(
        [_result(text="Should I create this chart?"), _result(viz=_viz(), tools=[_SKILLS])], turns, judge=judge
    )
    assert client.send_message.call_args_list[1].args[1] == CONFIRMATION_REPLY
    assert judge.calls == []
    assert result.turn_results[0].context_success is True


def test_context_mode_records_an_iteration_limit_as_a_stall_and_nudges() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    incomplete = TurnIncompleteError("SSE error 502", status_code=502, reason="max_iterations")
    result, client = _run([incomplete, _result(viz=_viz(), tools=[_SKILLS])], turns, judge=_FakeJudge(False))
    turn = result.turn_results[0]
    assert client.send_message.call_args_list[1].args[1] == NUDGE_MESSAGE
    assert turn.output_present is True
    assert turn.stalled is True
    assert turn.context_success is False
    assert result.stalled_turns == 1


def test_context_mode_never_primes_the_simulated_user_with_the_expected_output() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    with patch("gooddata_eval.core.agentic.conversation._get_sim_user_response") as legacy_sim:
        _run([_result(text="Which metric?"), _result(viz=_viz(), tools=[_SKILLS])], turns, judge=_FakeJudge(False))
    legacy_sim.assert_not_called()


def test_legacy_mode_keeps_the_primed_simulated_user_and_the_legacy_verdict() -> None:
    turns = [_viz_turn("t1", expected=_viz(filters=_EXPRESS))]
    with patch("gooddata_eval.core.agentic.conversation._get_sim_user_response", return_value="Express") as sim:
        result, _ = _run(
            [_result(text="Which format?"), _result(viz=_viz(), tools=[_SKILLS])],
            turns,
            mode="legacy",
            judge=_FakeJudge(False),
        )
    sim.assert_called_once()
    assert result.conversation_success is True  # legacy ignores the dropped filter
    assert result.context_success is False  # ...which context mode reports
    assert result.turn_results[0].output_correct is False


def test_context_kept_rate_is_over_labelled_turns_only() -> None:
    turns = [
        _viz_turn("t1", expected=_viz()),
        _viz_turn("t2", expected=_viz(), depends_on=["t1"]),
        _viz_turn("t3", expected=_viz(filters=_EXPRESS)),
    ]
    good = _result(viz=_viz(), tools=[_SKILLS])
    result, _ = _run([good, good, good], turns, judge=_FakeJudge(False))
    # t3 fails but is not labelled context-dependent, so the rate is t2 alone.
    assert result.context_kept_rate == 1.0
    assert result.turns_before_first_break == 2
    assert result.context_success is False


def test_fresh_conversation_per_turn_gives_every_turn_an_empty_history() -> None:
    turns = [_viz_turn("t1", expected=_viz()), _viz_turn("t2", expected=_viz())]
    good = _result(viz=_viz(), tools=[_SKILLS])
    _, client = _run([good, good], turns, judge=_FakeJudge(False), fresh_conversation_per_turn=True)
    assert client.create_conversation.call_count == 2
    assert client.delete_conversation.call_count == 2


def test_cleanup_deletes_created_metrics_and_alerts_but_keeps_a_metric_updated_in_place() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    tools = [
        _SKILLS,
        _tool("create_metric", result={"data": {"metric_id": "new_one", "maql": "SELECT 1", "created_new": True}}),
        _tool("create_metric", result={"data": {"metric_id": "old_one", "maql": "SELECT 2", "created_new": False}}),
        _tool("create_metric_alert", result={"id": "alert-1"}),
    ]
    with (
        patch("gooddata_eval.core.agentic.conversation._delete_metric") as del_metric,
        patch("gooddata_eval.core.agentic.conversation._delete_alert") as del_alert,
    ):
        _run([_result(viz=_viz(), tools=tools)], turns, judge=_FakeJudge(False))
    assert [c.args[2] for c in del_metric.call_args_list] == ["new_one"]
    assert [c.args[2] for c in del_alert.call_args_list] == ["alert-1"]


def test_cleanup_still_runs_for_a_metric_created_before_the_stream_died() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    partial = _result(tools=[_tool("create_metric", result={"data": {"metric_id": "orphan", "maql": "SELECT 1"}})])
    # No pytest.raises: a chat fault now ends its own turn and is recorded as
    # LoopExit.CHAT_ERROR rather than discarding the turns that already completed. What this
    # test is actually about -- the metric created before the stream died still gets deleted
    # -- is unchanged, and is what the assertion below pins.
    with patch("gooddata_eval.core.agentic.conversation._delete_metric") as del_metric:
        _run([ChatError_("stream died", partial_result=partial)], turns, judge=_FakeJudge(False))
    assert [c.args[2] for c in del_metric.call_args_list] == ["orphan"]


def test_context_mode_pushes_a_stalled_turn_once_then_ends_it() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    stall = _result(text="Let me look into that.")
    result, client = _run([stall, stall, stall], turns, judge=_FakeJudge(False))
    assert client.send_message.call_count == 2
    assert [c.kind for c in result.turn_results[0].clarifications] == ["no_action", "no_action"]
    assert result.turn_results[0].context_success is False


@pytest.mark.parametrize(("mode", "gate"), [("legacy", True), ("context", False)])
def test_scores_carry_both_verdicts_and_gate_on_the_mode(mode: str, gate: bool) -> None:
    """A turn that shows the chart but drops an established filter: legacy passes it, context does not."""
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = [_result(viz=_viz(), tools=[_SKILLS])]
    fixture = ConversationFixture(
        id="c", expected_skills=["visualization"], turns=[_viz_turn("t1", expected=_viz(filters=_EXPRESS))]
    )
    captured: dict = {}

    def _capture(_submit: object, _identity: object, **kwargs: object) -> None:
        captured["write_scores"] = kwargs["write_scores"]

    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.conversation.submit_trace_scoring", _capture),
    ):
        try:
            evaluate_agentic_conversation(
                host="h",
                token="t",
                workspace_id="ws",
                fixture=fixture,
                langfuse=MagicMock(),
                dataset_item_id="item-1",
                mode=mode,
                clarification_judge=_FakeJudge(False),
            )
            raised = False
        except ConversationAssertionError:
            raised = True
    assert raised is not gate

    ctx = MagicMock()
    captured["write_scores"](ctx)
    scores = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}
    assert scores["conversation_success"] == 1.0
    assert scores["context_success"] == 0.0
    assert scores["gate_passed"] is gate
    assert scores["turns_before_first_break"] == 0


def test_output_correct_treats_an_end_date_after_today_as_today() -> None:
    """ "2025 and 2026 so far": the year end and today select the same data."""
    so_far = {
        "f": {"type": "date_filter", "using": "dataset/transaction_date", "from": "2025-01-01", "to": "2026-12-31"}
    }
    today = {
        "f": {"type": "date_filter", "using": "dataset/transaction_date", "from": "2025-01-01", "to": "2026-09-30"}
    }
    earlier = {
        "f": {"type": "date_filter", "using": "dataset/transaction_date", "from": "2025-01-01", "to": "2026-06-30"}
    }
    with patch("gooddata_eval.core.agentic.conversation.date") as fake_date:
        fake_date.today.return_value = date(2026, 9, 30)
        assert _check_output_correct(_viz_turn(expected=_viz(filters=so_far)), _result(viz=_viz(filters=today)))[0]
        assert not _check_output_correct(_viz_turn(expected=_viz(filters=so_far)), _result(viz=_viz(filters=earlier)))[
            0
        ]


def _llm_returning(body: str) -> _ClarificationLLM:
    llm = _ClarificationLLM.__new__(_ClarificationLLM)
    llm.model = "fake"
    llm._system_prompt = ""
    choice = MagicMock()
    choice.message.content = body
    llm._create_completion = lambda messages: MagicMock(choices=[choice])
    return llm


def test_clarification_llm_reads_the_named_boolean() -> None:
    assert _llm_returning('{"already_in_conversation": true, "reasoning": "t2 said so"}').already_in_conversation(
        "p"
    ) == (True, "t2 said so")
    assert (
        _llm_returning('{"already_in_conversation": false, "reasoning": "no"}').already_in_conversation("p")[0] is False
    )


@pytest.mark.parametrize("body", ['{"score": 0}', '{"already_in_conversation": "yes"}', "not json", ""])
def test_clarification_llm_refuses_anything_but_a_boolean_verdict(body: str) -> None:
    with pytest.raises(JudgeResponseError):
        _llm_returning(body).already_in_conversation("p")


def test_judge_prompt_marks_an_empty_history() -> None:
    assert "CONVERSATION BEFORE:\n(empty)" in judge_prompt("", "Sort it", "By what?")


def test_context_mode_restates_at_most_once_per_turn() -> None:
    turns = [_viz_turn("t1", expected=_viz(), set_answers=["Gross Margin Percent."])]
    with patch(
        "gooddata_eval.core.agentic.conversation.reply_restating", return_value="As I said earlier, X."
    ) as restate:
        _, client = _run(
            [_result(text="Which one?"), _result(text="Which one, again?"), _result(viz=_viz(), tools=[_SKILLS])],
            turns,
            judge=_FakeJudge(lost_context=True),
        )
    restate.assert_called_once()
    assert client.send_message.call_args_list[2].args[1] == "Gross Margin Percent."


def test_output_correct_treats_a_single_value_in_as_equals() -> None:
    turn = TurnDefinition(
        turn_id="m",
        message="make it",
        expected_skill="metric",
        expected_output_type="metric",
        expected_output={"maql": 'SELECT {metric/a} WHERE {label/b} = "Digital"'},
    )
    same = ToolCallEvent.model_validate(
        _tool(
            "create_metric",
            result={"data": {"metric_id": "x", "maql": 'SELECT {metric/a} WHERE {label/b} IN ("Digital")'}},
        )
    )
    two = ToolCallEvent.model_validate(
        _tool(
            "create_metric",
            result={"data": {"metric_id": "x", "maql": 'SELECT {metric/a} WHERE {label/b} IN ("Digital", "Online")'}},
        )
    )
    assert _check_output_correct(turn, _result(), [same])[0] is True
    assert _check_output_correct(turn, _result(), [two])[0] is False


def test_an_iteration_limit_after_the_chart_was_made_keeps_the_chart() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    partial = _result(viz=_viz(), tools=[_SKILLS])
    incomplete = TurnIncompleteError("SSE error 502", status_code=502, reason="max_iterations", partial_result=partial)
    result, client = _run([incomplete], turns, judge=_FakeJudge(False))
    turn = result.turn_results[0]
    assert client.send_message.call_count == 1
    assert turn.output_present is True and turn.output_correct is True
    assert turn.stalled is True


def test_a_fresh_conversation_starts_with_no_active_skills() -> None:
    turns = [_viz_turn("t1", expected=_viz()), _viz_turn("t2", expected=_viz())]
    result, _ = _run(
        [_result(viz=_viz(), tools=[_SKILLS]), _result(viz=_viz())],
        turns,
        judge=_FakeJudge(False),
        fresh_conversation_per_turn=True,
    )
    assert result.turn_results[1].skill_routing is False


def test_a_question_on_the_last_allowed_round_is_still_judged() -> None:
    turns = [_viz_turn("t1", expected=_viz())]
    judge = _FakeJudge(lost_context=True)
    result, _ = _run([_result(text="Which chart?")], turns, judge=judge, max_clarification_turns=0)
    assert result.turn_results[0].clarifications[0].lost_context is True
    assert result.lost_context_clarifications == 1


def test_not_in_is_not_rewritten_as_equals() -> None:
    assert "not in" in _canonical_maql('SELECT {metric/a} WHERE {label/b} NOT IN ("x")')
    assert _canonical_maql('SELECT {metric/a} WHERE {label/b} IN ("x")') == _canonical_maql(
        'SELECT {metric/a} WHERE {label/b} = "x"'
    )


def test_the_flat_expected_shape_is_still_checked() -> None:
    turn = TurnDefinition(
        turn_id="t",
        message="m",
        expected_skill="visualization",
        expected_output={"metrics": ["metric/gross_margin_percent"], "dimensions": ["label/dim_store.store_format"]},
    )
    assert _check_output_correct(turn, _result(viz=_viz()))[0] is True
    assert _check_output_correct(turn, _result(viz=_viz(metric="metric/units_sold")))[0] is False


# --- clarification judge -------------------------------------------------------------


def _judge_with(llm: MagicMock) -> ClarificationJudge:
    judge = ClarificationJudge(model="fake")
    judge._llm = llm
    return judge


def test_judge_reads_the_verdict_and_caches_it_per_prompt() -> None:
    llm = MagicMock()
    llm.already_in_conversation.return_value = (True, "t1 named it")
    judge = _judge_with(llm)
    first = judge.judge("USER: chart it", "Add Units Sold", "Which chart?")
    second = judge.judge("USER: chart it", "Add Units Sold", "Which chart?")
    assert first == second == ClarificationVerdict(lost_context=True, reasoning="t1 named it")
    llm.already_in_conversation.assert_called_once()
    judge.judge("", "Add Units Sold", "Which chart?")
    assert llm.already_in_conversation.call_count == 2


def test_an_unreadable_verdict_leaves_the_clarification_unjudged() -> None:
    llm = MagicMock()
    llm.already_in_conversation.side_effect = JudgeResponseError("no boolean")
    verdict = _judge_with(llm).judge("", "x", "y")
    assert verdict.lost_context is None
    assert "no boolean" in verdict.error


def test_a_provider_fault_leaves_clarifications_unjudged_and_is_announced_once(
    capsys: pytest.CaptureFixture[str],
) -> None:
    llm = MagicMock()
    llm.already_in_conversation.side_effect = RuntimeError("401 bad key")
    judge = _judge_with(llm)
    assert judge.judge("", "a", "q1").lost_context is None
    assert judge.judge("", "b", "q2").error == "401 bad key"
    assert capsys.readouterr().out.count("left unjudged") == 1


def test_the_judge_needs_no_api_key_until_it_is_asked(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    judge = ClarificationJudge()
    assert judge.model_name
    assert judge.judge("", "a", "q").error is not None


def test_the_clarification_llm_uses_its_own_prompt(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    _fake_openai(monkeypatch, MagicMock())
    llm = _ClarificationLLM(model="gpt-4o")
    assert "already_in_conversation" in llm._system_prompt
    assert llm.model == "gpt-4o"


def test_the_clarification_llm_retries_an_empty_body_once() -> None:
    llm = _llm_returning("")
    calls: list[int] = []
    choice = MagicMock()
    choice.message.content = '{"already_in_conversation": false, "reasoning": "r"}'
    bodies = iter([MagicMock(choices=[]), MagicMock(choices=[choice])])
    llm._create_completion = lambda messages: calls.append(1) or next(bodies)
    assert llm.already_in_conversation("p") == (False, "r")
    assert len(calls) == 2


# --- simulated user (context mode) -------------------------------------------------------


def _fake_openai(monkeypatch: pytest.MonkeyPatch, openai_cls: MagicMock) -> MagicMock:
    """Stand in for the optional openai package, whether or not it is installed."""
    monkeypatch.setitem(sys.modules, "openai", types.SimpleNamespace(OpenAI=openai_cls))
    return openai_cls


def _openai_returning(content: str | None) -> MagicMock:
    response = MagicMock()
    response.choices = [MagicMock()]
    response.choices[0].message.content = content
    client = MagicMock()
    client.chat.completions.create.return_value = response
    return MagicMock(return_value=client)


def test_reply_from_facts_without_facts_needs_no_llm(monkeypatch: pytest.MonkeyPatch) -> None:
    openai_cls = _fake_openai(monkeypatch, MagicMock())
    assert reply_from_facts("USER: x", "Which?", []) == NO_ANSWER_REPLY
    openai_cls.assert_not_called()


def test_reply_from_facts_answers_from_the_facts(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    openai_cls = _fake_openai(monkeypatch, _openai_returning("  Sales Order Revenue.  "))
    assert reply_from_facts("USER: revenue by month", "Which revenue?", ["Sales Order Revenue."]) == (
        "Sales Order Revenue."
    )
    prompt = openai_cls.return_value.chat.completions.create.call_args.kwargs["messages"][1]["content"]
    assert "Sales Order Revenue." in prompt and "Which revenue?" in prompt


@pytest.mark.parametrize("failure", ["no_key", "provider_error", "empty_body"])
def test_simulated_user_falls_back_when_the_llm_gives_nothing(monkeypatch: pytest.MonkeyPatch, failure: str) -> None:
    if failure == "no_key":
        monkeypatch.delenv("OPENAI_API_KEY", raising=False)
        openai_cls = _openai_returning("unused")
    else:
        monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
        openai_cls = _openai_returning(None)
        if failure == "provider_error":
            openai_cls.return_value.chat.completions.create.side_effect = RuntimeError("503")
    _fake_openai(monkeypatch, openai_cls)
    assert reply_from_facts("h", "q", ["fact"]) == NO_ANSWER_REPLY
    assert reply_restating("h", "q").startswith("As I said earlier")


def test_reply_restating_returns_the_llm_restatement(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")
    _fake_openai(monkeypatch, _openai_returning("As I said earlier, Express."))
    assert reply_restating("USER: weakest? ASSISTANT: Express", "Which format?") == "As I said earlier, Express."


def test_simulated_user_reports_a_missing_openai_package(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setitem(sys.modules, "openai", None)
    assert ctx_mod._chat("s", "u") is None


# --- turn verdict and content-check edges -------------------------------------------------


def test_failure_reasons_name_an_unrun_turn_and_an_inactive_skill() -> None:
    unrun = _turn_result().model_copy(update={"no_error": False})
    assert unrun.failure_reasons()[0] == "turn could not run"
    wrong_skill = _turn_result().model_copy(update={"skill_routing": False})
    assert wrong_skill.failure_reasons() == ["skill 'visualization' not active"]


def test_expected_viz_is_none_for_a_shape_it_cannot_read() -> None:
    assert _expected_viz({"visualization": "not a chart"}) is None
    assert _expected_viz({"visualization": {"query": {"fields": {"m": 1}}}}) is None
    assert _expected_viz({"visualization": {"query": {}}}) is None


def test_mismatches_name_the_dimension_and_the_type() -> None:
    expected = {**_viz(), "type": "line_chart"}
    ok, diff = _check_output_correct(_viz_turn(expected=expected), _result(viz=_viz(dim="label/dim_brand.brand_name")))
    assert ok is False
    assert any(d.startswith("dimensions") for d in diff)
    assert any(d.startswith("type") for d in diff)


def test_output_correct_without_anything_to_compare_against() -> None:
    assert _check_output_correct(_viz_turn(expected=_viz()), _result()) == (False, ["no visualization to compare"])
    metric_turn = TurnDefinition(
        turn_id="m",
        message="make it",
        expected_skill="metric",
        expected_output_type="metric",
        expected_output={"maql": "SELECT 1"},
    )
    assert _check_output_correct(metric_turn, _result(), []) == (False, ["no created metric to compare"])
    no_maql = metric_turn.model_copy(update={"expected_output": {"title": "x"}})
    assert _check_output_correct(no_maql, _result(), []) == (None, [])


def test_cleanup_ignores_tool_results_it_cannot_read() -> None:
    unreadable = [
        ToolCallEvent.model_validate(_tool("create_metric", result=["not", "a", "dict"])),
        ToolCallEvent.model_validate(_tool("create_metric", result={"data": {"isError": True}})),
        ToolCallEvent.model_validate(_tool("create_metric_alert", result=["nope"])),
        ToolCallEvent.model_validate(_tool("create_metric_alert", result={"data": {"id": "a-nested"}})),
    ]
    assert _metric_creations(unreadable) == []
    assert _created_alert_ids(unreadable) == ["a-nested"]


def test_fresh_conversation_per_turn_refuses_a_conversation_it_did_not_create() -> None:
    fixture = ConversationFixture(id="c", expected_skills=["visualization"], turns=[_viz_turn("t1")])
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient"),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        pytest.raises(ValueError, match="creates itself"),
    ):
        run_agentic_conversation(
            host="h",
            token="t",
            workspace_id="ws",
            fixture=fixture,
            initial_conversation_id="given",
            fresh_conversation_per_turn=True,
        )


def test_context_kept_rate_is_scored_when_there_are_dependent_turns() -> None:
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = [_result(viz=_viz(), tools=[_SKILLS]), _result(viz=_viz())]
    fixture = ConversationFixture(
        id="c",
        expected_skills=["visualization"],
        turns=[_viz_turn("t1", expected=_viz()), _viz_turn("t2", expected=_viz(), depends_on=["t1"])],
    )
    captured: dict = {}
    with (
        patch("gooddata_eval.core.agentic.conversation.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.conversation.GoodDataSdk"),
        patch(
            "gooddata_eval.core.agentic.conversation.submit_trace_scoring",
            lambda _s, _i, **kw: captured.update(write=kw["write_scores"]),
        ),
    ):
        evaluate_agentic_conversation(
            host="h",
            token="t",
            workspace_id="ws",
            fixture=fixture,
            langfuse=MagicMock(),
            dataset_item_id="i",
            mode="context",
            clarification_judge=_FakeJudge(False),
        )
    ctx = MagicMock()
    captured["write"](ctx)
    scores = {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}
    assert scores["context_kept_rate"] == 1.0
    assert scores["turns_before_first_break"] == 2
