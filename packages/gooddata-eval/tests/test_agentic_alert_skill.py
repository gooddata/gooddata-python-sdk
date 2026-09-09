# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
from contextlib import ExitStack, contextmanager
from unittest.mock import MagicMock, patch

import pytest
from gooddata_eval.core.agentic._catalog import AnomalyDetectionGranularity
from gooddata_eval.core.agentic.alert_skill import (
    AlertEvaluation,
    AlertSkillAssertionError,
    _check_attributes,
    _check_filters,
    _check_granularity,
    _check_recipients,
    _check_trigger,
    _deep_subset,
    _normalize_expected_output,
    _to_number,
    evaluate_agentic_alert_skill,
    generate_simulated_alert_response,
    render_alert_proposal,
    run_agentic_alert_skill,
)
from gooddata_eval.core.models import ChatResult

_DATE_FILTER = {
    "relativeDateFilter": {
        "dataset": {"identifier": {"id": "order_date", "type": "dataset"}},
        "granularity": "MONTH",
        "from": -1,
        "to": -1,
    }
}
_ATTR_FILTER = {
    "positiveAttributeFilter": {
        "label": {"identifier": {"id": "customer_country", "type": "label"}},
        "in": {"values": ["United States"]},
    }
}

# Group-by entries arrive in two vocabularies for the same thing: fixtures author the AAC
# tool-input form, `create_metric_alert` receives the resolved AFM form forwarded verbatim
# from prepare_metric_alert_proposal. A test pairing AFM against AFM would prove nothing.
_AFM_MONTH_GROUPING = {
    "localIdentifier": "a0",
    "label": {"identifier": {"id": "customer_created_date.month", "type": "label"}},
}
_AFM_BRAND_GROUPING = {
    "localIdentifier": "a0",
    "label": {"identifier": {"id": "product_brand", "type": "label"}},
}
_AAC_MONTH_GROUPING = {"using": "label/customer_created_date.month"}
_AAC_BRAND_GROUPING = {"using": "label/product_brand"}

_PROPOSAL = {
    "title": "# of Orders Alert - Greater Than 500",
    "cta": "Should I create this alert?",
    "recipients": [{"email": "admin@gooddata.com"}],
    "dashboard": {"id": "dash-1", "title": "Orders overview"},
    "alert": {
        "trigger": "ALWAYS",
        "condition": {"comparison": {"operator": "GREATER_THAN", "right": {"value": 500}}},
        "execution": {"measures": [{"opaque": "afm"}]},
    },
}


def _no_alert_chat_result() -> ChatResult:
    """A turn where the agent refuses outright -- no tool calls, so no alert is created."""
    return ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "created_visualizations": None,
            "tool_call_events": [],
            "reasoning_step_count": 1,
        }
    )


@contextmanager
def _patched(client, *, simulated_reply=None, delete_alert=False):
    """Patch alert_skill's ChatClient, and optionally its simulated user and alert cleanup.

    ``simulated_reply`` is what the simulated user answers; ``delete_alert`` stubs out the
    teardown call a run makes for an alert it created. Yields the
    ``generate_simulated_alert_response`` mock, or None when the test asked for no reply.
    """
    with ExitStack() as stack:
        stack.enter_context(patch("gooddata_eval.core.agentic.alert_skill.ChatClient", return_value=client))
        mock_sim = None
        if simulated_reply is not None:
            mock_sim = stack.enter_context(
                patch(
                    "gooddata_eval.core.agentic.alert_skill.generate_simulated_alert_response",
                    return_value=simulated_reply,
                )
            )
        if delete_alert:
            stack.enter_context(patch("gooddata_eval.core.agentic.alert_skill._delete_alert"))
        yield mock_sim


def test_to_number_int():
    assert _to_number("42") == 42


def test_to_number_float():
    assert abs(_to_number("3.14") - 3.14) < 1e-9


def test_to_number_none():
    assert _to_number("abc") is None


def test_deep_subset_simple():
    assert _deep_subset({"a": 1}, {"a": 1, "b": 2}) is True


def test_deep_subset_missing_key():
    assert _deep_subset({"a": 1, "c": 3}, {"a": 1}) is False


def test_check_trigger_missing_or_null_defaults_to_always():
    # "Every time" is the product default -> the agent may omit the trigger arg
    # entirely, or serialise it as null. Both must count as ALWAYS, not a mismatch.
    expected = _normalize_expected_output({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert _check_trigger(expected, {"operator": "GREATER_THAN"}) is True  # key absent
    assert _check_trigger(expected, {"trigger": None}) is True  # present-but-null (the bug)
    assert _check_trigger(expected, {"trigger": "ALWAYS"}) is True


def test_check_trigger_once_needs_explicit_once():
    # A "One time" expectation must still require an explicit ONCE - the null-default
    # fix must not turn a wrong/absent trigger into a pass here.
    expected = _normalize_expected_output({"Operator": "LESS_THAN", "Trigger": "One time"})
    assert _check_trigger(expected, {"trigger": "ONCE"}) is True
    assert _check_trigger(expected, {"trigger": None}) is False  # null != ONCE
    assert _check_trigger(expected, {"trigger": "ONCE_PER_INTERVAL"}) is False  # real model error stays a fail


# --- filters: "no filters" is an expectation, "unspecified" is not (QA-28623) ---------------
#
# `_check_filters` used to return True whenever the expectation was empty, so an alert that
# bolted on an unrequested relativeDateFilter scored filters_correct=1 and the drift the
# ticket is about was invisible in the eval and on the trace.


def test_check_filters_stated_none_rejects_extra_date_filter():
    expected = _normalize_expected_output({"Operator": "GREATER_THAN", "Time window/Filters": "None (All time)"})
    assert expected.filters == []  # stated, not merely absent
    assert _check_filters(expected, {"filters": []}) is True
    assert _check_filters(expected, {}) is True
    assert _check_filters(expected, {"filters": [_DATE_FILTER]}) is False


def test_check_filters_unspecified_is_not_asserted():
    # Prose-only expectation: describes a filter the alert must have, but not comparably.
    # Demanding emptiness here would fail an alert whose filters are in fact correct.
    expected = _normalize_expected_output(
        {"Operator": "LESS_THAN", "Time window/Filters": "Customer Country = United States"}
    )
    assert expected.filters is None
    assert _check_filters(expected, {"filters": [_ATTR_FILTER, _DATE_FILTER]}) is True


def test_check_filters_absent_time_window_is_not_asserted():
    expected = _normalize_expected_output({"Operator": "ANOMALY"})
    assert expected.filters is None
    assert _check_filters(expected, {"filters": [_DATE_FILTER]}) is True


def test_check_filters_explicit_list_still_requires_subset():
    expected = _normalize_expected_output({"Operator": "LESS_THAN", "Filters": [_ATTR_FILTER]})
    assert _check_filters(expected, {"filters": [_ATTR_FILTER]}) is True
    assert _check_filters(expected, {"filters": []}) is False
    # An extra filter beyond the expected list is still a length mismatch -> fail.
    assert _check_filters(expected, {"filters": [_ATTR_FILTER, _DATE_FILTER]}) is False


def test_normalize_expected_filters_prefers_machine_readable_list():
    # Both columns present: the list wins over the prose, which merely paraphrases it.
    expected = _normalize_expected_output(
        {"Operator": "LESS_THAN", "Filters": [_ATTR_FILTER], "Time window/Filters": "Customer Country = United States"}
    )
    assert expected.filters == [_ATTR_FILTER]


def test_normalize_expected_filters_reads_none_marker_from_filters_column():
    expected = _normalize_expected_output({"Operator": "LESS_THAN", "Filters": "None (All time)"})
    assert expected.filters == []


def test_normalize_expected_filters_treats_prose_filters_column_as_unspecified():
    # Prose in `Filters` used to be returned verbatim, so `_check_filters` compared a string to a
    # list of filter dicts and could never pass — a guaranteed failure for a correct alert.
    expected = _normalize_expected_output({"Operator": "LESS_THAN", "Filters": "Product Category = X"})
    assert expected.filters is None
    assert _check_filters(expected, {"filters": [_ATTR_FILTER]}) is True


def test_check_recipients_matches_external_recipients_without_sdk():
    # The common path never needs a network call at all -- confirms adding the
    # internal_recipients fallback doesn't force a lookup when it isn't needed.
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    mock_sdk = MagicMock()
    assert _check_recipients(expected, {"recipients": ["user@example.com"]}, sdk=mock_sdk) is True
    mock_sdk._client.entities_api.get_all_entities_users.assert_not_called()


def test_check_recipients_matches_internal_recipients_via_resolved_user_id():
    # Some notification channels are workspace-restricted to internal users --
    # create_metric_alert then addresses the alert by internal user id via
    # `internal_recipients`, never by email, so the plain email/external-recipients
    # comparison alone can never match this delivery path.
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.return_value.data = [
        MagicMock(id="user.abc123"),
    ]
    assert _check_recipients(expected, {"internal_recipients": ["user.abc123"]}, sdk=mock_sdk) is True
    mock_sdk._client.entities_api.get_all_entities_users.assert_called_once_with(filter="email=in=('user@example.com')")


def test_check_recipients_matches_internal_recipients_as_a_bare_string():
    # internal_recipients is declared `anyOf: [array of string, string, null]` in the
    # create_metric_alert tool schema -- a single id as a bare string is schema-legal,
    # not a malformed call. Confirmed live: gpt-5.5 passed a bare string for a
    # single-recipient alert and this comparison silently failed before the fix.
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.return_value.data = [
        MagicMock(id="user.abc123"),
    ]
    assert _check_recipients(expected, {"internal_recipients": "user.abc123"}, sdk=mock_sdk) is True


def test_check_recipients_escapes_apostrophe_in_email_for_rsql_filter():
    # o'hara@example.com must not break the RSQL filter string -- the apostrophe
    # has to be escaped before interpolation, same as the query engine requires.
    expected = _normalize_expected_output({"Recipients": ["o'hara@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.return_value.data = [
        MagicMock(id="user.abc123"),
    ]
    assert _check_recipients(expected, {"internal_recipients": ["user.abc123"]}, sdk=mock_sdk) is True
    mock_sdk._client.entities_api.get_all_entities_users.assert_called_once_with(
        filter="email=in=('o\\'hara@example.com')"
    )


def test_check_recipients_resolves_multiple_emails_in_a_single_bulk_request():
    # N expected recipients must cost one request, not N -- confirmed against the
    # live Users entities API that RSQL `=in=(...)` returns only the matching subset.
    expected = _normalize_expected_output({"Recipients": ["a@example.com", "b@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.return_value.data = [
        MagicMock(id="user.a"),
        MagicMock(id="user.b"),
    ]
    assert _check_recipients(expected, {"internal_recipients": ["user.a", "user.b"]}, sdk=mock_sdk) is True
    mock_sdk._client.entities_api.get_all_entities_users.assert_called_once_with(
        filter="email=in=('a@example.com','b@example.com')"
    )


def test_check_recipients_internal_recipients_mismatch_still_fails():
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.return_value.data = [
        MagicMock(id="someone.else"),
    ]
    assert _check_recipients(expected, {"internal_recipients": ["user.abc123"]}, sdk=mock_sdk) is False


def test_check_recipients_internal_recipients_without_sdk_fails_gracefully():
    # No sdk available to resolve the email -> no crash, just no match (the plain
    # external-recipients comparison already ran and failed by this point).
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    assert _check_recipients(expected, {"internal_recipients": ["user.abc123"]}, sdk=None) is False


def test_check_recipients_resolution_failure_fails_gracefully():
    # A lookup error (permissions, network) must not crash the evaluation --
    # it just means this comparison path can't match, same as no sdk at all.
    expected = _normalize_expected_output({"Recipients": ["user@example.com"]})
    mock_sdk = MagicMock()
    mock_sdk._client.entities_api.get_all_entities_users.side_effect = RuntimeError("boom")
    assert _check_recipients(expected, {"internal_recipients": ["user.abc123"]}, sdk=mock_sdk) is False


def test_alert_evaluation_strict_pass():
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=True,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
    )
    assert ev.strict_pass is True


def test_alert_evaluation_strict_fail():
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=False,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
    )
    assert ev.strict_pass is False


def test_run_agentic_alert_skill_no_alert_created():
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = _no_alert_chat_result()
    mock_client._base = "http://host/api/v1/actions/workspaces/ws1/ai"
    mock_client._auth = {"Authorization": "Bearer tok"}

    with _patched(mock_client):
        summary = run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
        )

    assert summary.pass_at_k is False
    assert summary.best.eval.alert_created is False
    mock_client.close.assert_called_once()


def test_run_agentic_alert_skill_uses_initial_conversation_for_run_0():
    mock_client = MagicMock()
    mock_client.send_message.return_value = _no_alert_chat_result()
    with _patched(mock_client):
        run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    mock_client.create_conversation.assert_not_called()
    mock_client.delete_conversation.assert_not_called()


def test_run_agentic_alert_skill_creates_fresh_conversations_for_remaining_runs():
    mock_client = MagicMock()
    mock_client.create_conversation.side_effect = ["fresh-1", "fresh-2"]
    mock_client.send_message.return_value = _no_alert_chat_result()
    with _patched(mock_client):
        run_agentic_alert_skill(
            host="http://host/api/v1/actions/workspaces/ws1/ai",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=3,
            max_iterations=1,
            initial_conversation_id="existing-conv",
        )
    assert mock_client.create_conversation.call_count == 2
    assert mock_client.delete_conversation.call_count == 2


# --- simulated user prompt (QA-28623) --------------------------------------------------------
#
# The drift these rules guard against was the sim-user's, not the agent's: asked "what time
# window should each check use? Day / Week / Month" it volunteered "monthly", then confirmed a
# summary that plainly read "Trigger: once per month".


def _sim_user_prompt(expected_output: dict, question: str = "") -> str:
    """Run the sim-user against a stub OpenAI client and return the system prompt it built."""
    fake_openai = MagicMock()
    fake_openai.return_value.chat.completions.create.return_value = MagicMock(
        choices=[MagicMock(message=MagicMock(content="ok"))]
    )
    with (
        patch("gooddata_eval.core.agentic.alert_skill._OpenAI", fake_openai),
        patch.dict("os.environ", {"OPENAI_API_KEY": "test-key"}),
    ):
        generate_simulated_alert_response(
            "What time period should each check cover?",
            _normalize_expected_output(expected_output),
            [],
            question=question,
        )
    call = fake_openai.return_value.chat.completions.create.call_args
    return call.kwargs["messages"][0]["content"]


def test_sim_user_states_always_trigger_in_natural_language():
    # `trigger=ALWAYS` alone left the sim-user silent about cadence; it must now ask for it
    # in words a role-playing user would actually use.
    prompt = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    assert "EVERY TIME" in prompt
    assert "not once per day, week or month" in prompt


def test_sim_user_asks_for_always_cadence_when_fixture_omits_trigger():
    # A fixture with no Trigger still demands ALWAYS (the product default `_check_trigger`
    # asserts), so rule 6 must ask for it rather than echo the "not specified" placeholder.
    prompt = _sim_user_prompt({"Operator": "GREATER_THAN"})
    assert "EVERY TIME" in prompt


def test_sim_user_states_once_trigger_in_natural_language():
    prompt = _sim_user_prompt({"Operator": "LESS_THAN", "Trigger": "One time"})
    assert "ONLY THE FIRST TIME" in prompt


def test_sim_user_goal_renders_omitted_trigger_as_always():
    # Rule 3 tells the sim-user to accept fields the goal reports as "not specified". Leaving the
    # trigger placeholder in the goal therefore licensed it to confirm a ONCE / ONCE_PER_INTERVAL
    # proposal — which `_check_trigger` then fails, because an omitted trigger means ALWAYS.
    expected = {"Operator": "GREATER_THAN"}
    prompt = _sim_user_prompt(expected)
    assert "trigger=ALWAYS" in prompt
    assert "trigger=not specified" not in prompt
    assert _check_trigger(_normalize_expected_output(expected), {"trigger": "ONCE"}) is False


def test_sim_user_prompt_carries_the_original_request():
    # The opening question goes straight to the agent, so the sim-user's first call has an empty
    # history. Rule 5's "the filters your original request implies" needs the request in view.
    question = "Notify me when the number of orders from the United States falls below 100"
    prompt = _sim_user_prompt({"Operator": "LESS_THAN", "Threshold": "100"}, question=question)
    assert question in prompt


def test_run_agentic_alert_skill_passes_question_to_sim_user():
    # Interaction: the agent asks for a filter the fixture never restates, so the sim-user can
    # only supply it by reading the original request out of its own prompt.
    question = "Notify me when the number of orders from the United States falls below 100"
    asked_turn = ChatResult.model_validate(
        {"text_response": "Which country should the alert filter on?", "tool_call_events": []}
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "tool_call_events": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "LESS_THAN", "threshold": 100}',
                    "result": '{"id": "alert-1"}',
                }
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.send_message.side_effect = [asked_turn, created_turn]

    with _patched(mock_client, simulated_reply="United States.", delete_alert=True) as mock_sim:
        run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question=question,
            expected_output={"operator": "LESS_THAN", "threshold": 100},
            k=1,
            max_iterations=6,
            initial_conversation_id="conv-1",
        )

    assert mock_sim.call_args.kwargs["question"] == question
    # The agent message stays positional so existing callers/patches keep working.
    assert mock_sim.call_args.args[0] == "Which country should the alert filter on?"


def test_sim_user_goal_states_between_bounds():
    # BETWEEN keeps its value in threshold_from/to, so `threshold` is None. Reporting the goal
    # as "not specified" made the sim-user demand the agent delete both bounds — impossible, so
    # it looped until max_iterations and the alert was never created (gpt56luna run, item _5).
    prompt = _sim_user_prompt(
        {"Operator": "BETWEEN", "Threshold_from": 50000, "Threshold_to": 200000, "Trigger": "Every time"}
    )
    assert "threshold=between 50000 and 200000" in prompt
    assert "threshold=not specified" not in prompt


def test_sim_user_accepts_fields_the_goal_leaves_unspecified():
    # Rule 3 must not turn an absent expectation into a correction demand.
    prompt = _sim_user_prompt({"Operator": "ANOMALY"})
    assert "'not specified' is one you have NO expectation about" in prompt
    assert "never ask for it to be removed" in prompt
    # The phrase must survive literal concatenation intact — a line break mid-sentence used to
    # render it as "'not    specified'", which the sim-user reads as a different instruction.
    assert "'not    specified'" not in prompt


def test_sim_user_refuses_invented_time_window_when_no_filters_expected():
    prompt = _sim_user_prompt({"Operator": "GREATER_THAN", "Time window/Filters": "None (All time)"})
    assert "NO filters" in prompt
    assert "last Day / Week / Month" in prompt
    assert "all time" in prompt


def test_sim_user_is_not_told_no_filters_when_expectation_is_unstated():
    # Prose-only expectation normalizes to None, not []. Claiming "NO filters" there would make
    # the sim-user refuse the country filter this request genuinely implies — the fixture would
    # still pass (filters are not asserted) while testing much less than it looks like.
    prompt = _sim_user_prompt({"Operator": "LESS_THAN", "Time window/Filters": "Customer Country = United States"})
    assert "NO filters" not in prompt
    assert "do not invent an evaluation period" in prompt


def test_sim_user_refuses_extra_filters_when_filters_expected():
    prompt = _sim_user_prompt({"Operator": "LESS_THAN", "Filters": [_ATTR_FILTER]})
    assert "NOTHING else" in prompt
    assert "refuse it" in prompt


def test_sim_user_verifies_trigger_and_filters_before_confirming():
    # Rule 3 checked recipients only, so a summary showing the wrong trigger was rubber-stamped.
    prompt = _sim_user_prompt({"Operator": "GREATER_THAN", "Trigger": "Every time"})
    rule_3 = prompt.split("3.", 1)[1].split("4.", 1)[0]
    for field in ("recipients", "trigger", "filters", "threshold", "operator"):
        assert field in rule_3, f"final-summary check must cover {field}"
    assert "do NOT confirm" in rule_3


def test_render_alert_proposal_keeps_verifiable_fields_and_drops_afm():
    rendered = render_alert_proposal(_PROPOSAL)
    # The CTA leads so the simulated user reads it as a question.
    assert rendered.startswith("Should I create this alert?")
    # Rule 3 of the sim-user prompt requires verifying recipients against its goal.
    assert "admin@gooddata.com" in rendered
    assert "GREATER_THAN" in rendered
    assert "Orders overview" in rendered
    # Opaque AFM wire dicts must not crowd out the fields above.
    assert "execution" not in rendered


def test_render_alert_proposal_drops_afm_when_execution_is_the_only_alert_field():
    # Truthiness-gated replacement used to leave the original execution-bearing dict in place.
    rendered = render_alert_proposal({"alert": {"execution": {"measures": [{"opaque": "afm"}]}}})
    assert "execution" not in rendered
    assert "opaque" not in rendered


def test_render_alert_proposal_falls_back_to_default_cta():
    assert render_alert_proposal({}).startswith("Should I create this alert?")


def test_run_agentic_alert_skill_answers_proposal_only_confirmation_turn():
    """GDAI-2032 regression: confirmation turn has no text part, only an alertProposal.

    Without the fallback the simulated user is handed an empty agent message, so the agent
    never receives an explicit "yes" and create_metric_alert is never called.
    """
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [_PROPOSAL],
            "tool_call_events": [
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None}
            ],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "tool_call_events": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
        }
    )
    mock_client = MagicMock()
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with _patched(
        mock_client, simulated_reply="Yes, please proceed to create the alert.", delete_alert=True
    ) as mock_sim:
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=6,
            initial_conversation_id="conv-1",
        )

    agent_message = mock_sim.call_args.args[0]
    assert "Should I create this alert?" in agent_message
    assert "admin@gooddata.com" in agent_message
    assert summary.best.eval.alert_created is True
    assert summary.best.alert_id == "alert-1"


def test_run_agentic_alert_skill_accumulates_reasoning_steps_across_iterations():
    proposal_turn = ChatResult.model_validate(
        {
            "text_response": None,
            "alertProposals": [_PROPOSAL],
            "toolCallEvents": [
                {"functionName": "prepare_metric_alert_proposal", "functionArguments": "{}", "result": None}
            ],
            "reasoningSteps": ["step one"],
        }
    )
    created_turn = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "toolCallEvents": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
            "reasoningSteps": ["step two"],
        }
    )
    mock_client = MagicMock()
    mock_client.send_message.side_effect = [proposal_turn, created_turn]

    with _patched(mock_client, simulated_reply="Yes, please proceed to create the alert.", delete_alert=True):
        summary = run_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=6,
            initial_conversation_id="conv-1",
        )

    assert summary.best.reasoning_steps == ["step one", "step two"]


def test_evaluate_agentic_alert_skill_returns_reasoning_steps_on_pass():
    chat_result = ChatResult.model_validate(
        {
            "text_response": "Alert created.",
            "toolCallEvents": [
                {
                    "functionName": "create_metric_alert",
                    "functionArguments": '{"operator": "GREATER_THAN", "threshold": 500}',
                    "result": '{"id": "alert-1"}',
                }
            ],
            "reasoningSteps": ["thinking about it"],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = chat_result

    with _patched(mock_client, delete_alert=True):
        outcome = evaluate_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Notify me whenever the number of orders goes above 500",
            expected_output={"operator": "GREATER_THAN", "threshold": 500},
            k=1,
            max_iterations=1,
        )

    assert outcome.reasoning_steps == ["thinking about it"]
    assert outcome.conversation_id == "conv-1"
    assert outcome.response_id is None
    assert outcome.detail == {
        "alert_created": True,
        "operator_correct": True,
        "threshold_correct": True,
        "trigger_correct": True,
        "filters_correct": True,
        "metric_correct": True,
        "recipients_correct": True,
        "attributes_correct": True,
        "granularity_correct": True,
        "actual_alert_arguments": {"operator": "GREATER_THAN", "threshold": 500},
        "latency_breakdown": [],
    }


def test_evaluate_agentic_alert_skill_attaches_reasoning_steps_to_exception_on_fail():
    chat_result = ChatResult.model_validate(
        {
            "text_response": "I cannot create the alert",
            "toolCallEvents": [],
            "reasoningSteps": ["confused thinking"],
        }
    )
    mock_client = MagicMock()
    mock_client.create_conversation.return_value = "conv-1"
    mock_client.send_message.return_value = chat_result

    with _patched(mock_client), pytest.raises(AlertSkillAssertionError) as exc_info:
        evaluate_agentic_alert_skill(
            host="http://host",
            token="tok",
            workspace_id="ws1",
            question="Create alert",
            expected_output={"operator": "GREATER_THAN", "threshold": 100},
            k=1,
            max_iterations=1,
        )
    assert exc_info.value.reasoning_steps == ["confused thinking"]
    assert exc_info.value.conversation_id == "conv-1"
    assert exc_info.value.response_id is None
    assert exc_info.value.detail == {
        "alert_created": False,
        "operator_correct": False,
        "threshold_correct": False,
        "trigger_correct": False,
        "filters_correct": False,
        "metric_correct": False,
        "recipients_correct": False,
        "attributes_correct": False,
        "granularity_correct": False,
        "actual_alert_arguments": {},
        "latency_breakdown": [],
    }


# --- attributes: a date narrows an alert as a group-by too ----------------------------------
#
# `_check_filters` reads only `filters`, and a group-by in `attributes` narrows an alert just
# as much: it makes the alert fire per period value instead of on the latest one, which is a
# different alert from the one the fixture describes. The expectation mirrors the `filters`
# contract — absent means unasserted, `[]` means "no grouping", a list means that grouping —
# but the comparison cannot: the fixture side is AAC-shaped and the actual side is AFM-shaped,
# so both are canonicalised to a label id first.


def test_check_attributes_absent_expectation_is_not_asserted():
    expected = _normalize_expected_output({"Operator": "GREATER_THAN"})
    assert expected.attributes is None
    assert _check_attributes(expected, {"attributes": [_AFM_MONTH_GROUPING]}) is True


def test_explicit_empty_attributes_rejects_month_grouping():
    expected = _normalize_expected_output({"Attributes": []})
    assert expected.attributes == []
    assert _check_attributes(expected, {"attributes": [_AFM_MONTH_GROUPING]}) is False


def test_explicit_empty_attributes_accepts_no_grouping():
    expected = _normalize_expected_output({"Attributes": []})
    assert _check_attributes(expected, {"attributes": []}) is True
    assert _check_attributes(expected, {}) is True
    assert _check_attributes(expected, {"attributes": None}) is True


def test_display_format_none_reads_as_no_grouping():
    """Fixtures are written in display format, where "None" is how absence is spelled."""
    expected = _normalize_expected_output({"Attributes": "None"})
    assert expected.attributes == []
    assert _check_attributes(expected, {"attributes": [_AFM_MONTH_GROUPING]}) is False


def test_aac_expectation_matches_resolved_afm_actual():
    """The two sides name the same grouping in different vocabularies and must still match."""
    expected = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    assert _check_attributes(expected, {"attributes": [_AFM_BRAND_GROUPING]}) is True


def test_stored_product_brand_fixture_still_passes():
    """The one dataset item that already carries an Attributes expectation, verbatim."""
    expected = _normalize_expected_output(
        {
            "Metric": "Returns (returns)",
            "Operator": "GREATER_THAN",
            "Threshold": "30",
            "Attributes": [{"using": "label/product_brand"}],
            "Time window/Filters": "For: each value of Product Brand",
        }
    )
    actual = {
        "attributes": [{"localIdentifier": "a0", "label": {"identifier": {"id": "product_brand", "type": "label"}}}]
    }
    assert _check_attributes(expected, actual) is True


def test_afm_spelled_expectation_matches_the_same_actual():
    """A fixture may also be written AFM-side; both spellings mean one grouping."""
    expected = _normalize_expected_output({"Attributes": [_AFM_BRAND_GROUPING]})
    assert _check_attributes(expected, {"attributes": [_AFM_BRAND_GROUPING]}) is True


def test_date_group_by_keeps_its_granularity_suffix():
    """`customer_created_date.month` and `customer_created_date` are different groupings."""
    expected = _normalize_expected_output({"Attributes": [_AAC_MONTH_GROUPING]})
    assert _check_attributes(expected, {"attributes": [_AFM_MONTH_GROUPING]}) is True
    coarser = {"localIdentifier": "a0", "label": {"identifier": {"id": "customer_created_date", "type": "label"}}}
    assert _check_attributes(expected, {"attributes": [coarser]}) is False


def test_bare_string_and_identifier_spellings_are_accepted():
    for spelling in ("product_brand", "label/product_brand", {"identifier": {"id": "product_brand"}}):
        expected = _normalize_expected_output({"Attributes": [spelling]})
        assert _check_attributes(expected, {"attributes": [_AFM_BRAND_GROUPING]}) is True


def test_explicit_attributes_list_rejects_no_grouping():
    expected = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    assert _check_attributes(expected, {"attributes": []}) is False
    assert _check_attributes(expected, {}) is False


def test_explicit_attributes_list_rejects_an_added_date_grouping():
    """Requiring a grouping must not license a second, unrequested one."""
    expected = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    actual = {"attributes": [_AFM_BRAND_GROUPING, _AFM_MONTH_GROUPING]}
    assert _check_attributes(expected, actual) is False


def test_grouping_comparison_is_order_insensitive():
    expected = _normalize_expected_output({"Attributes": [_AAC_MONTH_GROUPING, _AAC_BRAND_GROUPING]})
    actual = {"attributes": [_AFM_BRAND_GROUPING, _AFM_MONTH_GROUPING]}
    assert _check_attributes(expected, actual) is True


def test_show_all_values_is_not_asserted():
    """The check compares identity; per-entry properties are the agent's to choose."""
    expected = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    actual = {"attributes": [{**_AFM_BRAND_GROUPING, "showAllValues": True}]}
    assert _check_attributes(expected, actual) is True


def test_unrecognised_expectation_shape_raises():
    """A spelling the canonicaliser does not know must fail loudly, not compare unequal."""
    with pytest.raises(ValueError, match="expected group-by"):
        _normalize_expected_output({"Attributes": [{"dimension": "product_brand"}]})
    with pytest.raises(ValueError, match="expected group-by"):
        _normalize_expected_output({"Attributes": [{"using": "attribute/product_brand"}]})


def test_malformed_actual_attributes_fail_rather_than_error():
    """A non-list argument is the agent answering wrongly, and a wrong answer is a FAIL.

    An ERROR would be excluded from the run's failure count, ranking a malformed answer
    above a merely wrong one.
    """
    expected_none = _normalize_expected_output({"Attributes": []})
    for malformed in ({}, "", 0, {"using": "label/product_brand"}, "product_brand"):
        assert _check_attributes(expected_none, {"attributes": malformed}) is False

    expected_brand = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    for malformed in ({}, "", 0, "product_brand", {"using": "label/product_brand"}):
        assert _check_attributes(expected_brand, {"attributes": malformed}) is False


def test_unrecognised_actual_shape_raises():
    expected = _normalize_expected_output({"Attributes": [_AAC_BRAND_GROUPING]})
    with pytest.raises(ValueError, match="actual group-by"):
        _check_attributes(expected, {"attributes": [{"dimension": "product_brand"}]})


def test_attributes_prose_is_not_asserted():
    """Prose describes a grouping without encoding it, so it cannot be compared."""
    expected = _normalize_expected_output({"Attributes": "Product Brand"})
    assert expected.attributes is None
    assert _check_attributes(expected, {"attributes": [_AFM_MONTH_GROUPING]}) is True


def test_attributes_expectation_of_a_wrong_type_fails_loudly():
    """A malformed fixture must not silently degrade into "not asserted"."""
    with pytest.raises(ValueError, match="Attributes"):
        _normalize_expected_output({"Attributes": 7})


def test_alert_evaluation_strict_fail_on_attributes_alone():
    """A group-by alone sinks strict_pass, with every other check passing."""
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=True,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
        attributes_correct=False,
    )
    assert ev.strict_pass is False


def test_alert_evaluation_attributes_correct_defaults_to_true():
    """Fixtures stating no grouping expectation must not be failed by the new check."""
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=True,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
    )
    assert ev.attributes_correct is True
    assert ev.strict_pass is True


# --- ANOMALY granularity ----------------------------------------------------------------


def test_sim_user_supplies_the_granularity_an_anomaly_alert_needs():
    prompt = _sim_user_prompt({"Operator": "ANOMALY", "Granularity": "DAY", "Time window/Filters": "None (All time)"})
    assert "use DAY granularity" in prompt
    assert "never refuse to give one" in prompt


def test_sim_user_is_not_told_to_refuse_a_granularity_for_an_anomaly_alert():
    prompt = _sim_user_prompt({"Operator": "ANOMALY", "Time window/Filters": "None (All time)"})
    assert "invent" not in prompt.lower()


def test_sim_user_still_refuses_an_unrequested_granularity_for_a_normal_alert():
    prompt = _sim_user_prompt({"Operator": "GREATER_THAN", "Time window/Filters": "None (All time)"})
    assert "Do not invent an evaluation period, a granularity" in prompt
    assert "no date filter at all" in prompt


def test_sim_user_falls_back_to_day_when_an_anomaly_item_states_no_granularity():
    prompt = _sim_user_prompt({"Operator": "ANOMALY"})
    assert "use DAY granularity" in prompt


def test_normalize_expected_output_reads_granularity():
    assert _normalize_expected_output({"Operator": "ANOMALY", "Granularity": "WEEK"}).granularity == "WEEK"
    assert _normalize_expected_output({"Operator": "ANOMALY"}).granularity is None


def test_granularity_is_not_mistaken_for_a_filter():
    expected = _normalize_expected_output(
        {"Operator": "ANOMALY", "Granularity": "DAY", "Time window/Filters": "None (All time)"}
    )
    assert expected.filters == []
    assert expected.granularity == "DAY"


def test_granularity_is_asserted_when_the_fixture_states_one():
    expected = _normalize_expected_output({"Operator": "ANOMALY", "Granularity": "DAY"})
    assert _check_granularity(expected, {"granularity": "DAY"}) is True
    assert _check_granularity(expected, {"granularity": "MONTH"}) is False
    assert _check_granularity(expected, {}) is False


def test_granularity_comparison_is_case_insensitive():
    expected = _normalize_expected_output({"Operator": "ANOMALY", "Granularity": "day"})
    assert _check_granularity(expected, {"granularity": "DAY"}) is True


def test_granularity_is_unasserted_when_the_fixture_states_none():
    expected = _normalize_expected_output({"Operator": "GREATER_THAN"})
    assert _check_granularity(expected, {"granularity": "MONTH"}) is True
    assert _check_granularity(expected, {}) is True


def test_a_mismatched_granularity_fails_strict_pass():
    ev = AlertEvaluation(
        alert_created=True,
        operator_correct=True,
        threshold_correct=True,
        trigger_correct=True,
        filters_correct=True,
        metric_correct=True,
        recipients_correct=True,
        granularity_correct=False,
    )
    assert ev.strict_pass is False


def test_granularity_is_canonicalised_to_the_enum():
    expected = _normalize_expected_output({"Operator": "ANOMALY", "Granularity": " week "})
    assert expected.granularity is AnomalyDetectionGranularity.WEEK


def test_an_unknown_granularity_is_rejected_before_the_run_starts():
    with pytest.raises(ValueError, match="Invalid granularity"):
        _normalize_expected_output({"Operator": "ANOMALY", "Granularity": "fortnight"})


def test_every_gen_ai_interval_is_accepted():
    for value in ("HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR"):
        assert AnomalyDetectionGranularity.parse(value.lower()) is AnomalyDetectionGranularity(value)
    assert AnomalyDetectionGranularity.parse(None) is None
    assert AnomalyDetectionGranularity.parse("  ") is None
