# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic.conversation import (
    ConversationAssertionError,
    ConversationFixture,
    TurnDefinition,
    TurnResult,
    _get_sim_user_response,
    _resolve_refs,
    evaluate_agentic_conversation,
    run_agentic_conversation,
)
from gooddata_eval.core.models import ChatResult, ToolCallEvent


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
    assert set(_turn_result().detail()) == TurnResult._DETAIL_FIELDS


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
        "full_skill_coverage": True,
        "total_clarification_turns": 0,
        "turns": [
            {
                "turn_id": "t1",
                "expected_skill": "visualization",
                "skill_routing": True,
                "output_present": True,
                "output_correct": None,
                "activated_skills": ["visualization"],
                "active_skills": ["visualization"],
            }
        ],
        "latency_breakdown": [],
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
        "full_skill_coverage": False,
        "total_clarification_turns": 0,
        "turns": [
            {
                "turn_id": "t1",
                "expected_skill": "visualization",
                "skill_routing": False,
                "output_present": False,
                "output_correct": None,
                "activated_skills": ["other_skill"],
                "active_skills": ["other_skill"],
            }
        ],
        "latency_breakdown": [],
    }
