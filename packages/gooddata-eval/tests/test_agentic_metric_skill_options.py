# (C) 2026 GoodData Corporation. All rights reserved.
# SPDX-License-Identifier: LicenseRef-GoodData-Enterprise
"""The options shape of a metric-skill expectation: parsing, matchers, and the checks a run publishes."""

import json
import sys
import types
from collections.abc import Callable, Iterator, Sequence
from contextlib import contextmanager
from typing import Any
from unittest.mock import MagicMock, patch

import pytest
from gooddata_api_client.exceptions import ApiException, NotFoundException
from gooddata_eval.core.agentic import _metric_workspace as mw
from gooddata_eval.core.agentic import metric_skill as metric_skill_mod
from gooddata_eval.core.agentic._metric_expectation import (
    FieldSpec,
    UpdateSpec,
    field_mismatches,
    first_proposed_maql,
    format_matches_kind,
    missing_mentions,
    parse_expectation,
    substitute_placeholders,
    update_mismatches,
)
from gooddata_eval.core.agentic._metric_workspace import WorkspaceReadError, last_suggestions
from gooddata_eval.core.agentic.metric_skill import (
    METRIC_CONDITIONAL_SCORES,
    METRIC_DIAGNOSTIC_SCORES,
    AgenticMetricSummary,
    MetricSkillAssertionError,
    _match_expected_metrics,
    evaluate_agentic_metric_skill,
    run_agentic_metric_skill,
)
from gooddata_eval.core.chat.sse_client import ChatError
from gooddata_eval.core.evaluators._llm_judge import JudgeVerdict
from gooddata_eval.core.models import ChatResult, LoopExit, ToolCallEvent

# Shapes trimmed from the 2026-11-19 probe on an ecommerce_demo copy.
_NET_SALES = {
    "title": "Net Sales",
    "description": "The sum of all transacted orders adjusted by discounts and returns",
    "tags": [],
    "content": {"format": "$#,##0.00", "maql": "SELECT {metric/total_sales} - {metric/total_discounts}"},
}
_AVG_COST = {
    "title": "Average Product Cost",
    "description": "",
    "tags": None,
    "content": {"format": "$#,##0.00", "maql": "SELECT AVG({fact/order_unit_cost})"},
}


# --- parsing ----------------------------------------------------------------------------


def test_a_candidate_list_is_the_original_shape() -> None:
    spec = parse_expectation([{"maql": "SELECT 1"}, {"maql": "SELECT 2"}])
    assert spec.legacy and not spec.needs_workspace
    assert [c["maql"] for c in spec.candidates] == ["SELECT 1", "SELECT 2"]


def test_a_candidate_dict_with_title_and_format_stays_the_original_shape() -> None:
    # metric_skill items carry title/format beside the MAQL; they must not turn into field checks.
    spec = parse_expectation({"maql": "SELECT 1", "title": "X", "format": "#,##0", "tags": ["a"]})
    assert spec.legacy and spec.expected_fields is None


def test_options_accept_plain_maql_strings_as_candidates() -> None:
    spec = parse_expectation({"candidates": ["SELECT 1"], "expect_executes": True})
    assert not spec.legacy and spec.candidates == [{"maql": "SELECT 1"}]


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ({"candidates": ["SELECT 1"], "expect_no_creat": True}, "unknown key"),
        ({"candidates": ["SELECT 1"], "confirmation_turn": 1}, "at least 2"),
        ({"candidates": ["SELECT 1"], "confirmation_turn": True}, "at least 2"),
        ({"candidates": ["SELECT 1"], "confirmation_turn": 3, "expect_confirmation_stop": True}, "not both"),
        ({"candidates": ["SELECT 1"], "expected_fields": {"format_kind": "money"}}, "format_kind"),
        ({"candidates": ["SELECT 1"], "expected_fields": {"colour": "red"}}, "unknown key"),
        ({"candidates": ["SELECT 1"], "expect_no_create": True}, "cannot be combined"),
        ({"expect_no_create": True, "expected_mentions": []}, "non-empty"),
        ({"candidates": ["SELECT 1"], "expected_mentions": ["ARPU"]}, "needs expect_no_create"),
        ({"candidates": ["SELECT 1"], "run_all_replies": True}, "needs user_replies"),
        ({"expected_metrics": [["SELECT 1"], ["SELECT 2"]]}, "needs user_replies"),
        ({"expected_metrics": [["SELECT {metric/@1}"], ["SELECT 2"]], "user_replies": ["yes"]}, "not an earlier entry"),
        ({"expected_update": {"title": "X"}}, "needs a metric_id"),
        ({"expected_update": {"metric_id": "m"}}, "at least one field"),
        ({"expected_update": {"metric_id": "m", "colour": "red"}}, "unknown key"),
        ({"user_replies": ["yes"]}, "checks nothing"),
        ({"candidates": [{"title": "no maql"}]}, "non-empty MAQL"),
        ({"candidates": ["SELECT 1"], "expect_executes": "yes"}, "true or false"),
    ],
)
def test_a_malformed_options_shape_fails_loudly(raw: Any, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_expectation(raw)


def test_expect_confirmation_stop_means_no_write_in_turn_one() -> None:
    assert parse_expectation({"candidates": ["SELECT 1"], "expect_confirmation_stop": True}).confirmation_turn == 2


def test_a_malformed_expectation_raises_before_any_request() -> None:
    with patch("gooddata_eval.core.agentic.metric_skill.ChatClient") as chat_cls, pytest.raises(ValueError):
        run_agentic_metric_skill("http://h", "t", "ws", "q", {"candidates": ["SELECT 1"], "typo": 1})
    chat_cls.assert_not_called()


# --- matchers ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("fmt", "kind", "expected"),
    [
        ("0.0%", "percent", True),
        ("#,##0", "percent", False),
        ("$#,##0", "currency", True),
        ("€#,##0", "currency", True),
        ("#,##0", "currency", False),
        ("#,##0", "integer", True),
        ("$#,##0", "integer", True),
        ("#,##0.00", "integer", False),
        ("#,##0.00", "decimal", True),
        ("0.00%", "decimal", True),
    ],
)
def test_format_kinds(fmt: str, kind: str, expected: bool) -> None:
    assert format_matches_kind(fmt, kind) is expected


def test_field_matching_ignores_case_and_spacing_of_the_title_and_treats_tags_as_a_set() -> None:
    stored = {"title": "Median  Line cost", "tags": ["kpi", "finance"], "content": {"format": "#,##0.00"}}
    spec = FieldSpec(title="Median Line Cost", tags=frozenset({"Finance", "KPI"}), format_kind="decimal")
    assert field_mismatches(spec, "median_line_cost", stored) == []


def test_field_matching_names_every_wrong_field() -> None:
    stored = {"title": "A", "description": "x", "tags": ["sales"], "content": {"format": "#,##0"}}
    spec = FieldSpec(
        title="B", metric_id="b", format="$#,##0.00", description_contains=("refund",), tags_include=frozenset({"q4"})
    )
    found = field_mismatches(spec, "a", stored)
    assert [m.split(":")[0] for m in found] == ["metric_id", "title", "format", "description", "tags"]


def test_field_matching_reports_a_missing_metric() -> None:
    assert field_mismatches(FieldSpec(title="X"), "gone", None) == ["metric 'gone' is not stored in the workspace"]


def test_an_update_that_resets_the_format_is_caught() -> None:
    # GDAI-2838: a rename sends no format, and the tool writes #,##0 over $#,##0.00.
    after = {**_AVG_COST, "title": "Avg Unit Cost", "content": {**_AVG_COST["content"], "format": "#,##0"}}
    spec = UpdateSpec(metric_id="average_product_cost", fields=FieldSpec(title="Avg Unit Cost"))
    assert update_mismatches(spec, _AVG_COST, after) == [
        "format changed although the request did not ask for it: '$#,##0.00' -> '#,##0'"
    ]


def test_an_update_that_changes_only_what_it_was_asked_passes() -> None:
    after = {**_AVG_COST, "content": {**_AVG_COST["content"], "format": "$#,##0"}}
    spec = UpdateSpec(metric_id="average_product_cost", fields=FieldSpec(format="$#,##0"))
    assert update_mismatches(spec, _AVG_COST, after) == []


def test_an_update_can_require_new_maql() -> None:
    after = {**_AVG_COST, "content": {**_AVG_COST["content"], "maql": "SELECT AVG({fact/order_unit_cost}) WITHOUT PF"}}
    spec = UpdateSpec(
        metric_id="average_product_cost", fields=FieldSpec(), maql=("SELECT AVG({fact/order_unit_cost}) WITHOUT PF",)
    )
    assert update_mismatches(spec, _AVG_COST, after) == []


def test_placeholders_take_the_ids_matched_for_earlier_entries() -> None:
    assert substitute_placeholders("SELECT {metric/@0} - {metric/@1}", ["a", "b"]) == "SELECT {metric/a} - {metric/b}"
    assert substitute_placeholders("SELECT {metric/@1}", ["a"]) == "SELECT {metric/@1}"


def test_several_metrics_match_in_order_and_a_dependent_one_uses_their_ids() -> None:
    writes = [
        {"metric_id": "total_return_paid", "maql": "SELECT SUM({fact/return_unit_paid_amount})"},
        {"metric_id": "total_return_cost", "maql": "SELECT SUM({fact/return_unit_cost})"},
        {"metric_id": "return_margin", "maql": "SELECT {metric/total_return_paid} - {metric/total_return_cost}"},
    ]
    expected = (
        ("SELECT SUM({fact/return_unit_paid_amount})",),
        ("SELECT SUM({fact/return_unit_cost})",),
        (
            "SELECT {metric/@0} - {metric/@1}",
            "SELECT SUM({fact/return_unit_paid_amount}) - SUM({fact/return_unit_cost})",
        ),
    )
    assert _match_expected_metrics(expected, writes) == ["total_return_paid", "total_return_cost", "return_margin"]
    assert _match_expected_metrics(expected, writes[:2]) == ["total_return_paid", "total_return_cost", None]


def test_the_first_proposal_is_the_first_formula_in_a_code_span() -> None:
    texts = ["I need one detail first.", "**Return Units**\n- Formula: `SELECT SUM({fact/return_unit_quantity})`\n"]
    assert first_proposed_maql(texts) == "SELECT SUM({fact/return_unit_quantity})"
    assert first_proposed_maql(["no formula here"]) is None


def test_mentions_are_found_in_any_reply_whatever_the_case() -> None:
    assert missing_mentions(("ARPU", "gross_profit_margin"), ["Use {metric/arpu}.", "nothing"]) == [
        "gross_profit_margin"
    ]


def test_last_suggestions_reads_the_latest_item_that_carries_them() -> None:
    items = [
        {"content": {"type": "multipart", "suggestions": {"actions": [{"query": "old"}]}}},
        {"content": {"type": "multipart"}},
        {"content": {"type": "multipart", "suggestions": {"actions": [{"query": "new"}]}}},
        {"content": "text"},
    ]
    assert last_suggestions(items) == {"actions": [{"query": "new"}]}
    assert last_suggestions([]) is None


# --- runs -------------------------------------------------------------------------------


def _turn(text: str, *writes: dict, parts: list | None = None) -> ChatResult:
    return ChatResult.model_validate(
        {
            "textResponse": text,
            "toolCallEvents": [
                {"functionName": "create_metric", "functionArguments": "{}", "result": json.dumps({"data": w})}
                for w in writes
            ],
            "unhandledParts": parts or [],
        }
    )


class _FakeWorkspace:
    """Stands in for MetricWorkspace: an in-memory metric store the test edits as the agent would."""

    def __init__(self, metrics: dict[str, dict]) -> None:
        self.metrics = {k: json.loads(json.dumps(v)) for k, v in metrics.items()}
        self.restored: list[tuple[str, bool]] = []
        self.items: list[dict] = []
        self.execute_error: str | None = None
        self.read_error: str | None = None
        self.snapshot_error: str | None = None
        self.restore_fails = False
        self.unrestored: list[str] = []

    def list_metrics(self) -> dict[str, dict]:
        if self.snapshot_error:
            raise WorkspaceReadError(self.snapshot_error)
        return dict(self.metrics)

    def get_metric(self, metric_id: str) -> dict | None:
        if self.read_error:
            raise WorkspaceReadError(self.read_error)
        return self.metrics.get(metric_id)

    def restore_metric(self, metric_id: str, attributes: dict, *, exists: bool) -> bool:
        self.restored.append((metric_id, exists))
        if self.restore_fails:
            return False
        self.metrics[metric_id] = attributes
        return True

    def execute_metric(self, metric_id: str) -> str | None:
        return self.execute_error

    def conversation_items(self, conversation_id: str) -> list[dict]:
        if self.read_error:
            raise WorkspaceReadError(self.read_error)
        return self.items

    def close(self) -> None:
        pass


@contextmanager
def _run_env(
    turns: Sequence[ChatResult | Exception], workspace: _FakeWorkspace, *, on_send: Callable[[str], None] | None = None
) -> Iterator[tuple[MagicMock, MagicMock]]:
    """Patch the chat client to answer ``turns`` in order (an exception is raised), and the other collaborators."""
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    answers = iter(turns)

    def _send(_conversation_id: str, message: str) -> ChatResult:
        if on_send:
            on_send(message)
        answer = next(answers)
        if isinstance(answer, Exception):
            raise answer
        return answer

    client.send_message.side_effect = _send
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.metric_skill.MetricWorkspace", return_value=workspace),
        patch("gooddata_eval.core.agentic.metric_skill.generate_simulated_response") as sim,
    ):
        yield client, sim


def _run(expected: dict, max_iterations: int = 7) -> AgenticMetricSummary:
    return run_agentic_metric_skill("http://h", "t", "ws", "q", expected, k=1, max_iterations=max_iterations)


def test_the_original_shape_reads_no_workspace() -> None:
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient") as chat_cls,
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.metric_skill.MetricWorkspace") as ws_cls,
    ):
        chat_cls.return_value.send_message.return_value = _turn("ok", {"maql": "SELECT 1", "metric_id": "m"})
        summary = run_agentic_metric_skill("http://h", "t", "ws", "q", [{"maql": "SELECT 1"}], k=1, max_iterations=1)
    ws_cls.assert_not_called()
    assert summary.best.checks == {} and summary.pass_at_k


def test_scripted_replies_go_out_in_order_and_the_simulated_user_stays_silent() -> None:
    sent: list[str] = []
    ws = _FakeWorkspace({})
    turns = [_turn("Proposal. Should I create it?"), _turn("Understood, I won't create it.")]
    with _run_env(turns, ws, on_send=sent.append) as (_, sim):
        summary = _run({"expect_no_create": True, "user_replies": ["No, don't create it."]})
    assert sent == ["q", "No, don't create it."]
    sim.assert_not_called()
    assert summary.best.checks == {"metric_not_created": True}
    assert summary.pass_at_k


def test_a_write_fails_the_no_create_check_and_a_missing_mention_fails_reuse() -> None:
    ws = _FakeWorkspace({})
    turns = [_turn("Created it.", {"metric_id": "rev_per_customer", "maql": "SELECT 1", "created_new": True})]
    with _run_env(turns, ws):
        summary = _run({"expect_no_create": True, "expected_mentions": ["arpu"]})
    assert summary.best.checks == {"metric_not_created": False, "metric_reuse_named": False}
    assert summary.best.check_details["metric_reuse_named"] == {"missing": ["arpu"]}
    assert not summary.pass_at_k


def test_a_single_turn_item_without_replies_stops_after_the_first_answer() -> None:
    ws = _FakeWorkspace({})
    with _run_env([_turn("A matching metric already exists: {metric/arpu}.")], ws) as (client, sim):
        summary = _run({"expect_no_create": True, "expected_mentions": ["arpu"]})
    assert client.send_message.call_count == 1
    sim.assert_not_called()
    assert summary.pass_at_k


def test_a_write_before_the_confirmation_turn_fails() -> None:
    # D12: the reply changes the request; the agent must propose again and write only after "yes" (turn 3).
    ws = _FakeWorkspace({})
    write = {"metric_id": "m", "maql": "SELECT AVG({fact/rating})", "created_new": True}
    turns = [_turn("Proposal?"), _turn("Created.", write)]
    with _run_env(turns, ws):
        summary = _run(
            {"candidates": ["SELECT AVG({fact/rating})"], "confirmation_turn": 3, "user_replies": ["Use avg.", "Yes."]}
        )
    assert summary.best.checks["metric_confirmed_first"] is False
    assert summary.best.checks["maql_correct"] is True


def test_an_overwrite_is_restored_from_the_snapshot_and_fails_no_overwrite() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})

    def _overwrite(message: str) -> None:
        if message == "Yes, go ahead.":
            ws.metrics["net_sales"] = {**_NET_SALES, "content": {"format": "#,##0", "maql": "SELECT 1"}}

    write = {"metric_id": "net_sales", "maql": "SELECT 1", "created_new": False}
    turns = [_turn("Net Sales exists. Replace it?"), _turn("Updated.", write)]
    with _run_env(turns, ws, on_send=_overwrite):
        summary = _run({"candidates": ["SELECT 1"], "expect_no_overwrite": True, "user_replies": ["Yes, go ahead."]})
    assert summary.best.checks == {"metric_created": True, "maql_correct": True, "metric_no_overwrite": False}
    assert ws.restored == [("net_sales", True)]
    assert ws.metrics["net_sales"] == _NET_SALES


def test_run_all_replies_keeps_going_after_a_write_and_judges_the_stored_metric() -> None:
    ws = _FakeWorkspace({})
    stored = {
        "title": "Lowest Return Paid",
        "description": "Smallest amount refunded for one unit",
        "tags": ["returns"],
        "content": {"format": "$#,##0.00", "maql": "SELECT MIN({fact/return_unit_paid_amount})"},
    }
    write = {
        "metric_id": "lowest_return_paid",
        "maql": "SELECT MIN({fact/return_unit_paid_amount})",
        "title": "Lowest Return Paid",
    }

    def _store(message: str) -> None:
        if message == "Yes, go ahead.":
            ws.metrics["lowest_return_paid"] = stored

    turns = [
        _turn("Proposal?"),
        _turn("Created.", write),
        _turn("Change it like this?"),
        _turn("Updated.", {**write, "created_new": False}),
    ]
    with _run_env(turns, ws, on_send=_store) as (client, _):
        summary = _run(
            {
                "candidates": ["SELECT MIN({fact/return_unit_paid_amount})"],
                "user_replies": ["Yes, create it.", "Change its description.", "Yes, go ahead."],
                "run_all_replies": True,
                "expected_fields": {
                    "description": "Smallest amount refunded for one unit",
                    "tags": ["returns"],
                    "format": "$#,##0.00",
                },
            }
        )
    assert client.send_message.call_count == 4
    assert summary.best.checks == {"metric_created": True, "maql_correct": True, "metric_fields_correct": True}


def test_an_update_check_catches_a_reset_format_and_the_metric_is_restored() -> None:
    ws = _FakeWorkspace({"average_product_cost": _AVG_COST})

    def _rename(message: str) -> None:
        if message == "Yes, go ahead.":
            ws.metrics["average_product_cost"] = {
                **_AVG_COST,
                "title": "Avg Unit Cost",
                "content": {**_AVG_COST["content"], "format": "#,##0"},
            }

    write = {"metric_id": "average_product_cost", "maql": "SELECT AVG({fact/order_unit_cost})", "created_new": False}
    turns = [_turn("Rename it?"), _turn("Renamed.", write)]
    with _run_env(turns, ws, on_send=_rename):
        summary = _run(
            {
                "expected_update": {"metric_id": "average_product_cost", "title": "Avg Unit Cost"},
                "user_replies": ["Yes, go ahead."],
            }
        )
    assert summary.best.checks == {"metric_updated": False}
    assert "format changed" in summary.best.check_details["metric_updated"][0]
    assert ws.metrics["average_product_cost"] == _AVG_COST


def test_several_metrics_are_awaited_across_replies() -> None:
    ws = _FakeWorkspace({})
    first = {"metric_id": "a", "maql": "SELECT MAX({fact/order_unit_price})"}
    second = {"metric_id": "b", "maql": "SELECT MIN({fact/order_unit_cost})"}
    turns = [_turn("Both?"), _turn("Created one.", first), _turn("Created the other.", second)]
    with _run_env(turns, ws) as (client, _):
        summary = _run(
            {
                "expected_metrics": [["SELECT MAX({fact/order_unit_price})"], ["SELECT MIN({fact/order_unit_cost})"]],
                "user_replies": ["Yes, create them all.", "Please create the remaining ones too."],
            }
        )
    assert client.send_message.call_count == 3
    assert summary.best.checks == {"metric_all_created": True}


def test_clarification_rubric_execution_suggestions_and_first_proposal() -> None:
    ws = _FakeWorkspace({})
    ws.items = [
        {"content": {"suggestions": {"actions": [{"label": "Chart", "query": "Show Conversion Rate on a chart"}]}}}
    ]
    write = {
        "metric_id": "conversion_rate",
        "maql": "SELECT {metric/net_orders} / {metric/of_orders}",
        "title": "Conversion Rate",
    }
    question_part = [
        {"type": "clarifyingQuestions", "questions": [{"question": "Which conversion?", "options": ["a", "b"]}]}
    ]
    turns = [
        _turn("Conversion could mean two things.", parts=question_part),
        _turn("**Conversion Rate**\n- Formula: `SELECT {metric/net_orders} / {metric/of_orders}`\nCreate it?"),
        _turn("Created.", write),
    ]
    with (
        _run_env(turns, ws),
        patch("gooddata_eval.core.agentic.metric_skill.LLMJudge"),
        patch(
            "gooddata_eval.core.agentic.metric_skill._judge_rubric", return_value=JudgeVerdict(True, "fine")
        ) as judge,
    ):
        summary = _run(
            {
                "candidates": ["SELECT {metric/net_orders} / {metric/of_orders}"],
                "user_replies": ["Processed orders over all orders.", "Yes, create it."],
                "expect_clarification": True,
                "rubric": "Asks what a conversion is before proposing.",
                "expect_executes": True,
                "expect_suggestions": True,
                "score_first_proposal": True,
            }
        )
    judge.assert_called_once()
    assert summary.best.checks == {
        "metric_created": True,
        "maql_correct": True,
        "metric_clarified": True,
        "metric_rubric": True,
        "metric_executes": True,
        "metric_suggestions": True,
    }
    assert summary.best.diagnostics == {"metric_first_proposal_correct": True}


def test_a_metric_that_does_not_compute_fails_the_execution_check() -> None:
    ws = _FakeWorkspace({})
    ws.execute_error = "execute: HTTP 400 invalid MAQL"
    with _run_env([_turn("Created.", {"metric_id": "m", "maql": "SELECT 1"})], ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_executes": True})
    assert summary.best.checks["metric_executes"] is False
    assert summary.best.check_details["metric_executes"] == "execute: HTTP 400 invalid MAQL"


def test_a_removed_metric_fails_no_deletion_and_is_recreated() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})

    def _delete(_message: str) -> None:
        ws.metrics.pop("net_sales", None)

    with _run_env([_turn("I can't delete metrics.")], ws, on_send=_delete):
        summary = _run({"expect_no_create": True, "expect_no_deletion": ["net_sales"]})
    assert summary.best.checks == {"metric_not_created": True, "metric_none_deleted": False}
    assert ws.restored == [("net_sales", False)]


def test_every_published_check_name_is_listed_for_the_report() -> None:
    names = {
        "metric_not_created",
        "metric_reuse_named",
        "metric_no_overwrite",
        "metric_clarified",
        "metric_confirmed_first",
        "metric_rubric",
        "metric_fields_correct",
        "metric_updated",
        "metric_all_created",
        "metric_none_deleted",
        "metric_executes",
        "metric_suggestions",
        "metric_scored",
    }
    assert set(METRIC_CONDITIONAL_SCORES) == names
    assert METRIC_DIAGNOSTIC_SCORES == ("metric_first_proposal_correct",)


def _evaluate(
    expected: dict, turns: Sequence[ChatResult | Exception], ws: _FakeWorkspace
) -> tuple[Any, dict[str, Any]]:
    """Run evaluate_agentic_metric_skill with Langfuse captured; returns (outcome or exception, score dict)."""
    result, ctx = _evaluate_ctx(expected, turns, ws)
    return result, {c.kwargs["name"]: c.kwargs["value"] for c in ctx.score.call_args_list}


def _evaluate_ctx(expected: dict, turns: Sequence[ChatResult | Exception], ws: _FakeWorkspace) -> tuple[Any, MagicMock]:
    """Like ``_evaluate``, but returns the Langfuse context the scores were written to."""
    captured: dict[str, Any] = {}

    def _capture(_submit: Any, _identity: Any, **kwargs: Any) -> None:
        captured["write_scores"] = kwargs["write_scores"]

    with (
        _run_env(turns, ws),
        patch("gooddata_eval.core.agentic.metric_skill.submit_trace_scoring", _capture),
    ):
        try:
            result = evaluate_agentic_metric_skill(
                "http://h", "t", "ws", "q", expected, k=1, langfuse=MagicMock(), dataset_item_id="item-1"
            )
        except MetricSkillAssertionError as exc:
            result = exc
    ctx = MagicMock()
    captured["write_scores"](ctx)
    return result, ctx


def test_an_options_item_publishes_only_the_checks_it_opts_into() -> None:
    ws = _FakeWorkspace({})
    _, scores = _evaluate({"expect_no_create": True, "expected_mentions": ["arpu"]}, [_turn("Use {metric/arpu}.")], ws)
    assert scores["metric_not_created"] == 1.0
    assert scores["metric_reuse_named"] == 1.0
    assert "metric_created" not in scores and "maql_correct" not in scores


def test_a_diagnostic_is_published_but_does_not_gate() -> None:
    ws = _FakeWorkspace({})
    turns = [_turn("Formula: `SELECT 2`. Create it?"), _turn("Created.", {"metric_id": "m", "maql": "SELECT 1"})]
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "user_replies": ["Make it SELECT 1."], "score_first_proposal": True}, turns, ws
    )
    assert scores["metric_first_proposal_correct"] == 0.0
    assert result.runs_passed == 1


def test_a_failing_options_item_names_its_failed_checks() -> None:
    ws = _FakeWorkspace({})
    turns = [_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "created_new": True})]
    result, scores = _evaluate({"expect_no_create": True}, turns, ws)
    assert scores["metric_not_created"] == 0.0
    assert "Failed checks: metric_not_created" in str(result)
    assert result.failed_runs[0]["failed_checks"][0]["name"] == "metric_not_created"


# --- review fixes -----------------------------------------------------------------------


def _fake_sdk(pages: dict[int, list[dict]] | None = None, get: Callable[..., Any] | None = None) -> MagicMock:
    """An SDK whose entity API serves metric pages (as plain dicts) and single metrics."""
    sdk = MagicMock()
    requested: list[int] = []

    def _list(_ws: str, *, page: int, size: int, _check_return_type: bool) -> types.SimpleNamespace:
        requested.append(page)
        return types.SimpleNamespace(data=(pages or {}).get(page, []), included=[])

    sdk._client.entities_api.get_all_entities_metrics.side_effect = _list
    if get is not None:
        sdk._client.entities_api.get_entity_metrics.side_effect = get
    sdk.requested = requested
    return sdk


def test_metrics_are_listed_through_the_sdk_pager_which_stops_at_a_short_page() -> None:
    full = [{"id": f"m{i}", "attributes": {"title": str(i), "content": {"maql": "SELECT 1"}}} for i in range(500)]
    last = {"title": "L", "content": {"maql": "SELECT 2"}}
    sdk = _fake_sdk({0: full, 1: [{"id": "last", "attributes": last}]})
    metrics = mw.MetricWorkspace("http://h", "t", "ws", sdk).list_metrics()
    assert sdk.requested == [0, 1]
    assert len(metrics) == 501 and metrics["last"] == last


def test_a_missing_metric_reads_as_none_and_another_failure_as_a_read_error() -> None:
    def _get(_ws: str, metric_id: str, _check_return_type: bool) -> types.SimpleNamespace:
        if metric_id == "gone":
            raise NotFoundException(status=404)
        if metric_id == "broken":
            raise ApiException(status=500)
        # Like the real client: a document model whose data is a plain dict.
        return types.SimpleNamespace(data={"id": metric_id, "attributes": {"title": "T"}})

    ws = mw.MetricWorkspace("http://h", "t", "ws", _fake_sdk(get=_get))
    assert ws.get_metric("ok") == {"title": "T"}
    assert ws.get_metric("gone") is None
    with pytest.raises(WorkspaceReadError):
        ws.get_metric("broken")


def test_a_restore_writes_every_writable_attribute_back() -> None:
    sent: list[dict] = []

    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        sent.append({"method": request.method, "body": json.loads(request.content)})
        return mw.httpx.Response(200, json={})

    ws = mw.MetricWorkspace("http://h", "t", "ws", _fake_sdk())
    ws._client = mw.httpx.Client(transport=mw.httpx.MockTransport(_handler))
    attributes = {
        **_NET_SALES,
        "isHidden": True,
        "isHiddenFromKda": True,
        "conditionalFormatting": {"rules": []},
        "createdAt": "2026-01-01",
        "areRelationsValid": True,
    }
    assert ws.restore_metric("net_sales", attributes, exists=True)
    written = sent[0]["body"]["data"]["attributes"]
    assert sent[0]["method"] == "PUT"
    assert written == {
        "title": _NET_SALES["title"],
        "description": _NET_SALES["description"],
        "tags": [],
        "content": _NET_SALES["content"],
        "isHidden": True,
        "isHiddenFromKda": True,
        "conditionalFormatting": {"rules": []},
    }


def test_an_unreadable_conversation_is_a_harness_error_not_an_agent_failure() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 500"
    with _run_env([_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"})], ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_suggestions": True})
    assert summary.best.checks["metric_suggestions"] is False
    assert summary.best.harness_error == "metric_suggestions: HTTP 500"
    assert summary.best.unscored == ["metric_suggestions"]


def test_a_harness_error_labels_the_run_error() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 502"
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "expect_executes": True, "expected_fields": {"title": "M"}},
        [_turn("Created.", {"metric_id": "m", "maql": "SELECT 1"})],
        ws,
    )
    assert scores["eval_error"] == 1
    assert "Harness error" in str(result)


def test_a_failed_snapshot_skips_the_run_instead_of_driving_the_agent() -> None:
    ws = _FakeWorkspace({})
    ws.snapshot_error = "could not list metrics: 503"
    with _run_env([_turn("never sent")], ws) as (client, _):
        summary = _run({"candidates": ["SELECT 1"], "expect_no_overwrite": True})
    client.send_message.assert_not_called()
    assert summary.best.exit_reason == LoopExit.NOT_RUN
    assert summary.best.harness_error == "snapshot: could not list metrics: 503"


def test_editing_a_metric_the_run_created_is_not_an_overwrite() -> None:
    ws = _FakeWorkspace({})
    created = {"metric_id": "new_m", "maql": "SELECT 1", "created_new": True}
    edited = {**created, "created_new": False}
    turns = [_turn("Created.", created), _turn("Change it?"), _turn("Updated.", edited)]
    with _run_env(turns, ws):
        summary = _run(
            {
                "candidates": ["SELECT 1"],
                "expect_no_overwrite": True,
                "user_replies": ["Change its description.", "Yes."],
                "run_all_replies": True,
            }
        )
    assert summary.best.checks["metric_no_overwrite"] is True
    assert ws.restored == []


def test_a_confirmation_prompt_is_not_a_clarifying_question() -> None:
    ws = _FakeWorkspace({})
    turns = [
        _turn("Here it is: `SELECT 1`. Should I create it?"),
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 1"}),
    ]
    with _run_env(turns, ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_clarification": True, "user_replies": ["Yes."]})
    assert summary.best.checks["metric_clarified"] is False


def test_a_missing_judge_fails_before_any_request() -> None:
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient") as chat_cls,
        patch("gooddata_eval.core.agentic.metric_skill.LLMJudge", side_effect=OSError("OPENAI_API_KEY is required")),
        pytest.raises(OSError),
    ):
        _run({"expect_no_create": True, "rubric": "Says it cannot delete."})
    chat_cls.assert_not_called()


def test_a_judge_without_a_verdict_is_a_harness_error() -> None:
    ws = _FakeWorkspace({})
    with (
        _run_env([_turn("I can't delete metrics.")], ws),
        patch("gooddata_eval.core.agentic.metric_skill.LLMJudge"),
        patch(
            "gooddata_eval.core.agentic.metric_skill._judge_rubric",
            return_value=JudgeVerdict(False, "", error="unreadable"),
        ),
    ):
        summary = _run({"expect_no_create": True, "rubric": "Says it cannot delete."})
    assert summary.best.checks["metric_rubric"] is False
    assert summary.best.harness_error == "metric_rubric: judge gave no verdict: unreadable"


def test_the_judge_reads_user_and_assistant_turns_in_order_simulated_replies_included() -> None:
    ws = _FakeWorkspace({})
    turns = [_turn("Which date?"), _turn("Created.", {"metric_id": "m", "maql": "SELECT 1"})]
    with (
        _run_env(turns, ws) as (_, sim),
        patch("gooddata_eval.core.agentic.metric_skill.LLMJudge"),
        patch("gooddata_eval.core.agentic.metric_skill._judge_rubric", return_value=JudgeVerdict(True, "")) as judge,
    ):
        sim.return_value = "Use the order date."
        _run({"candidates": ["SELECT 1"], "rubric": "Asks which date before proposing."})
    transcript = judge.call_args.args[2]
    assert transcript == [
        ("User", "q"),
        ("Assistant", "Which date?"),
        ("User", "Use the order date."),
        ("Assistant", "Created."),
    ]


def test_a_spent_script_stops_early_rather_than_succeeding() -> None:
    ws = _FakeWorkspace({})
    with _run_env([_turn("Which one?"), _turn("Still need to know which one?")], ws):
        summary = _run({"expected_fields": {"title": "X"}, "user_replies": ["Yes."]})
    assert summary.best.exit_reason == LoopExit.STOPPED_EARLY
    assert summary.best.checks == {"metric_fields_correct": False}


def test_a_write_in_a_broken_turn_counts_for_the_confirmation_check() -> None:
    ws = _FakeWorkspace({})
    partial = _turn("", {"metric_id": "m", "maql": "SELECT 1", "created_new": True})
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = ChatError("stream broke", partial_result=partial)
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.metric_skill.MetricWorkspace", return_value=ws),
    ):
        summary = _run({"candidates": ["SELECT 1"], "expect_confirmation_stop": True})
    assert summary.best.checks["metric_confirmed_first"] is False


def test_an_options_item_puts_its_checks_at_the_top_of_the_detail() -> None:
    ws = _FakeWorkspace({})
    result, _ = _evaluate({"expect_no_create": True}, [_turn("No metric needed.")], ws)
    assert result.detail["metric_not_created"] is True
    assert "metric_created" not in result.detail and "maql_correct" not in result.detail


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ({"expect_no_create": True, "expect_executes": True}, "cannot be combined"),
        ({"expect_no_create": True, "expect_suggestions": True}, "cannot be combined"),
        ({"expected_update": {"metric_id": "m", "title": "T"}, "expect_no_overwrite": True}, "forbids"),
        ({"expect_no_deletion": True}, "non-empty string"),
        ({"rubric": "x", "expect_executes": True}, "need candidates or expected_fields"),
    ],
)
def test_contradicting_options_are_rejected(raw: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_expectation(raw)


@pytest.mark.parametrize("raw", [["SELECT 1"], "SELECT 1", [{"maql": "SELECT 1"}, "SELECT 2"]])
def test_an_original_shape_with_a_plain_string_fails_loudly(raw: Any) -> None:
    with pytest.raises(ValueError, match="plain MAQL strings go under 'candidates'"):
        parse_expectation(raw)


def test_the_first_proposal_is_read_from_a_fenced_block_too() -> None:
    text = "Here is the formula:\n```maql\nSELECT SUM({fact/x})\n```\nCreate it?"
    assert first_proposed_maql([text]) == "SELECT SUM({fact/x})"


# --- CodeRabbit review and coverage ---------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "message"),
    [
        ({"candidates": ["SELECT 1"], "rubric": None}, "rubric must be"),
        ({"candidates": ["SELECT 1"], "rubric": "  "}, "rubric must be"),
        ({"candidates": ["SELECT 1"], "expected_fields": {"format_kind": None}}, "format_kind"),
        ({"candidates": ["SELECT 1"], "expected_fields": {}}, "non-empty object"),
        ({"candidates": ["SELECT 1"], "expected_fields": {"title": ""}}, "non-empty string"),
        ({"candidates": []}, "non-empty list"),
        ({"expected_metrics": [["SELECT 1"]], "user_replies": ["yes"]}, "at least two"),
        ({"candidates": ["SELECT 1"], "expected_update": {"metric_id": "m", "title": "T"}}, "drop candidates"),
        ({"expect_no_create": True, "score_first_proposal": True}, "needs candidates"),
        ({"confirmation_turn": 2, "user_replies": ["y"], "rubric": ""}, "rubric"),
    ],
)
def test_more_malformed_options_fail_loudly(raw: dict, message: str) -> None:
    with pytest.raises(ValueError, match=message):
        parse_expectation(raw)


def test_a_single_candidate_string_and_a_confirmation_turn_with_a_rubric_are_valid() -> None:
    assert parse_expectation({"candidates": "SELECT 1", "expect_executes": True}).candidates == [{"maql": "SELECT 1"}]
    spec = parse_expectation({"confirmation_turn": 2, "user_replies": ["Yes"], "rubric": "Asks before creating."})
    assert spec.confirmation_turn == 2 and not spec.candidates
    with pytest.raises(ValueError, match="checks nothing"):
        parse_expectation({"expect_confirmation_stop": False, "user_replies": ["Yes"]})


@pytest.mark.parametrize("kind", ["integer", "decimal", "percent", "currency"])
def test_a_missing_format_is_no_kind(kind: str) -> None:
    assert format_matches_kind("", kind) is False
    assert format_matches_kind("  ", kind) is False


def test_field_matching_reports_kind_description_and_tags() -> None:
    stored = {"title": "A", "description": "x", "tags": ["a"], "content": {"format": ""}}
    spec = FieldSpec(format_kind="integer", description="y", tags=frozenset({"b"}))
    assert [m.split(":")[0] for m in field_mismatches(spec, "a", stored)] == ["format", "description", "tags"]


def test_an_update_needs_a_metric_that_existed_and_still_exists() -> None:
    spec = UpdateSpec(metric_id="m", fields=FieldSpec(title="T"))
    assert update_mismatches(spec, None, _AVG_COST) == ["metric 'm' did not exist before the run"]
    assert update_mismatches(spec, _AVG_COST, None) == ["metric 'm' is not stored in the workspace"]


def test_an_update_with_the_wrong_maql_is_reported() -> None:
    spec = UpdateSpec(metric_id="m", fields=FieldSpec(), maql=("SELECT 2",))
    assert update_mismatches(spec, _AVG_COST, _AVG_COST)[0].startswith("maql: expected one of ['SELECT 2']")


def test_an_update_whose_requested_field_was_already_right_does_not_pass() -> None:
    # The agent only replied; the title was already the requested one.
    spec = UpdateSpec(metric_id="m", fields=FieldSpec(title="Average Product Cost"))
    assert update_mismatches(spec, _AVG_COST, _AVG_COST) == [
        "title did not change although the request asked for it: still 'Average Product Cost'"
    ]


def test_an_update_that_unhides_a_hidden_metric_is_caught() -> None:
    before = {**_AVG_COST, "isHidden": True, "conditionalFormatting": {"rules": [1]}}
    after = {**_AVG_COST, "title": "Avg Unit Cost"}
    spec = UpdateSpec(metric_id="m", fields=FieldSpec(title="Avg Unit Cost"))
    changed = [m.split(" ")[0] for m in update_mismatches(spec, before, after)]
    assert changed == ["isHidden", "conditionalFormatting"]


def test_several_metrics_are_judged_by_the_latest_write_of_each_id() -> None:
    writes = [
        {"metric_id": "a", "maql": "SELECT 1"},
        {"metric_id": "a", "maql": "SELECT 9"},
        {"metric_id": "b", "maql": "SELECT 2"},
    ]
    assert _match_expected_metrics((("SELECT 1",), ("SELECT 2",)), writes) == [None, "b"]


def test_several_metrics_try_every_assignment() -> None:
    writes = [{"metric_id": "a", "maql": "SELECT 1"}, {"metric_id": "b", "maql": "SELECT 2"}]
    assert _match_expected_metrics((("SELECT 1", "SELECT 2"), ("SELECT 1",)), writes) == ["b", "a"]


def test_run_all_replies_sends_every_reply_although_every_metric_is_there() -> None:
    ws = _FakeWorkspace({})
    both = [{"metric_id": "a", "maql": "SELECT 1"}, {"metric_id": "b", "maql": "SELECT 2"}]
    turns = [_turn("Both?"), _turn("Created both.", *both), _turn("Anything else?")]
    with _run_env(turns, ws) as (client, _):
        summary = _run(
            {
                "expected_metrics": [["SELECT 1"], ["SELECT 2"]],
                "user_replies": ["Yes.", "Thanks, that's all."],
                "run_all_replies": True,
            }
        )
    assert client.send_message.call_count == 3
    assert summary.best.checks == {"metric_all_created": True}


def test_a_chat_failure_before_any_answer_is_no_proof_of_refusal() -> None:
    ws = _FakeWorkspace({})
    client = MagicMock()
    client.create_conversation.return_value = "conv-1"
    client.send_message.side_effect = ChatError("stream broke")
    with (
        patch("gooddata_eval.core.agentic.metric_skill.ChatClient", return_value=client),
        patch("gooddata_eval.core.agentic.metric_skill.GoodDataSdk"),
        patch("gooddata_eval.core.agentic.metric_skill.MetricWorkspace", return_value=ws),
    ):
        summary = _run({"expect_no_create": True})
    assert summary.best.checks == {"metric_not_created": False}
    assert summary.best.check_details["metric_not_created"] == "the agent never completed an answer"


def test_a_judge_provider_failure_is_a_harness_error() -> None:
    ws = _FakeWorkspace({})
    with (
        _run_env([_turn("I can't delete metrics.")], ws),
        patch("gooddata_eval.core.agentic.metric_skill.LLMJudge"),
        patch("gooddata_eval.core.agentic.metric_skill._judge_rubric", side_effect=TimeoutError("judge timed out")),
    ):
        summary = _run({"expect_no_create": True, "rubric": "Says it cannot delete."})
    assert summary.best.checks["metric_rubric"] is False
    assert summary.best.harness_error == "metric_rubric: judge gave no verdict: TimeoutError: judge timed out"


def test_the_rubric_judge_gets_the_conversation_in_order() -> None:
    judge = MagicMock()
    judge.score.return_value = (True, "ok")
    verdict = metric_skill_mod._judge_rubric(judge, "criteria", [("User", "q"), ("Assistant", "a")])
    assert verdict.passed
    assert judge.score.call_args.kwargs == {
        "input": "q",
        "expected_output": "criteria",
        "actual_output": "User: q\n\nAssistant: a",
    }


def test_expected_fields_read_the_metric_the_agent_wrote_not_the_named_one() -> None:
    ws = _FakeWorkspace({"sales": {"title": "Sales", "content": {"maql": "SELECT 1", "format": "#,##0"}}})
    write = {"metric_id": "wrong_id", "maql": "SELECT 1"}

    def _store(_message: str) -> None:
        ws.metrics["wrong_id"] = {"title": "Other", "content": {"maql": "SELECT 1"}}

    with _run_env([_turn("Created.", write)], ws, on_send=_store):
        summary = _run({"candidates": ["SELECT 1"], "expected_fields": {"metric_id": "sales", "title": "Sales"}})
    assert summary.best.checks["metric_fields_correct"] is False
    assert summary.best.check_details["metric_fields_correct"][0] == "metric_id: expected 'sales', got 'wrong_id'"


def test_a_failed_restore_is_a_harness_error_and_stops_later_runs() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})
    ws.restore_fails = True
    write = {"metric_id": "net_sales", "maql": "SELECT 1", "created_new": False}
    turns = [_turn("Updated.", write), _turn("never sent")]
    with _run_env(turns, ws) as (client, _):
        summary = run_agentic_metric_skill(
            "http://h", "t", "ws", "q", {"candidates": ["SELECT 1"], "expect_no_overwrite": True}, k=2, max_iterations=1
        )
    first, second = summary.run_results
    assert first.harness_error == "restore failed for ['net_sales']"
    assert second.exit_reason == LoopExit.NOT_RUN and "could not put back" in second.harness_error
    assert client.send_message.call_count == 1


def test_a_guarded_metric_that_cannot_be_checked_counts_as_not_restored() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})
    calls = {"n": 0}

    def _get(metric_id: str) -> dict | None:
        calls["n"] += 1
        if calls["n"] > 1:
            raise WorkspaceReadError("HTTP 502")
        return ws.metrics.get(metric_id)

    ws.get_metric = _get
    with _run_env([_turn("I can't delete metrics.")], ws):
        summary = _run({"expect_no_create": True, "expect_no_deletion": ["net_sales"]})
    assert summary.best.checks["metric_none_deleted"] is True
    assert ws.unrestored == ["net_sales"]


def test_suggestions_without_a_written_metric_do_not_fail_the_check() -> None:
    ws = _FakeWorkspace({})
    ws.items = [{"content": {"suggestions": {"actions": [{"query": "Show something"}]}}}]
    with _run_env([_turn("Which one?")], ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_suggestions": True}, max_iterations=1)
    assert summary.best.checks["metric_suggestions"] is True


def test_suggestions_naming_another_metric_fail_the_check() -> None:
    ws = _FakeWorkspace({})
    ws.items = [{"content": {"suggestions": {"actions": [{"label": "Chart", "query": "Show Net Sales"}]}}}]
    with _run_env([_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "Margin"})], ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_suggestions": True})
    assert summary.best.checks["metric_suggestions"] is False


def test_a_silent_agent_ends_the_run() -> None:
    ws = _FakeWorkspace({})
    with _run_env([_turn("")], ws):
        summary = _run({"candidates": ["SELECT 1"]})
    assert summary.best.exit_reason == LoopExit.AGENT_SILENT


def test_a_wrong_maql_on_an_options_item_names_maql_correct() -> None:
    ws = _FakeWorkspace({})
    result, _ = _evaluate(
        {"candidates": ["SELECT 1"], "expect_executes": True},
        [_turn("Created.", {"metric_id": "m", "maql": "SELECT 2"})],
        ws,
    )
    assert [c["name"] for c in result.failed_runs[0]["failed_checks"]] == ["maql_correct"]


# --- MetricWorkspace against a mocked HTTP transport --------------------------------------------


def _http_workspace(
    handler: Callable[[mw.httpx.Request], mw.httpx.Response], sdk: MagicMock | None = None
) -> mw.MetricWorkspace:
    ws = mw.MetricWorkspace("http://h", "t", "ws", sdk or _fake_sdk())
    ws._client = mw.httpx.Client(transport=mw.httpx.MockTransport(handler))
    return ws


@pytest.fixture
def _no_backoff(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("GOODDATA_EVAL_CHAT_INITIAL_BACKOFF_S", "0")
    monkeypatch.setenv("GOODDATA_EVAL_CHAT_MAX_RETRIES", "2")


def test_a_restore_retries_a_transient_status_and_posts_a_removed_metric(_no_backoff: None) -> None:
    statuses = iter([503, 201])
    seen: list[str] = []

    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        seen.append(request.method)
        return mw.httpx.Response(next(statuses), json={})

    ws = _http_workspace(_handler)
    assert ws.restore_metric("net_sales", _NET_SALES, exists=False)
    assert seen == ["POST", "POST"]
    ws.close()


def test_a_restore_that_keeps_failing_returns_false(_no_backoff: None) -> None:
    ws = _http_workspace(lambda request: mw.httpx.Response(503, json={}))
    assert ws.restore_metric("net_sales", _NET_SALES, exists=True) is False
    assert (
        _http_workspace(lambda request: mw.httpx.Response(400, json={})).restore_metric(
            "net_sales", _NET_SALES, exists=True
        )
        is False
    )

    def _boom(request: mw.httpx.Request) -> mw.httpx.Response:
        raise mw.httpx.ReadTimeout("slow", request=request)

    assert _http_workspace(_boom).restore_metric("net_sales", _NET_SALES, exists=True) is False


def test_listing_or_reading_metrics_wraps_api_failures() -> None:
    sdk = _fake_sdk()
    sdk._client.entities_api.get_all_entities_metrics.side_effect = ApiException(status=400)
    ws = mw.MetricWorkspace("http://h", "t", "ws", sdk)
    with pytest.raises(WorkspaceReadError, match="could not list metrics"):
        ws.list_metrics()


@pytest.mark.parametrize(
    ("row", "message"),
    [({"id": "m"}, "unreadable row"), ({"id": "m", "attributes": {"title": "T"}}, "has no MAQL")],
)
def test_an_incomplete_snapshot_row_fails_the_snapshot(row: dict, message: str) -> None:
    ws = mw.MetricWorkspace("http://h", "t", "ws", _fake_sdk({0: [row]}))
    with pytest.raises(WorkspaceReadError, match=message):
        ws.list_metrics()


def test_a_metric_lookup_without_attributes_is_a_read_error() -> None:
    ws = mw.MetricWorkspace("http://h", "t", "ws", _fake_sdk(get=lambda *a, **k: types.SimpleNamespace(data=None)))
    with pytest.raises(WorkspaceReadError, match="no attributes"):
        ws.get_metric("m")


def _execute_handler(
    execute_status: int = 200, execute_body: dict | None = None, result_status: int = 200
) -> Callable[[mw.httpx.Request], mw.httpx.Response]:
    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        if request.method == "POST":
            body = (
                execute_body
                if execute_body is not None
                else {"executionResponse": {"links": {"executionResult": "r1"}}}
            )
            return mw.httpx.Response(execute_status, json=body)
        return mw.httpx.Response(result_status, json={"data": [[1]]})

    return _handler


def test_a_metric_that_computes_has_no_rejection() -> None:
    assert _http_workspace(_execute_handler()).execute_metric("m") is None


@pytest.mark.parametrize(("execute", "result"), [(400, 200), (200, 422)])
def test_a_platform_rejection_is_the_check_verdict(execute: int, result: int) -> None:
    reason = _http_workspace(_execute_handler(execute_status=execute, result_status=result)).execute_metric("m")
    assert reason is not None and "HTTP 4" in reason


@pytest.mark.parametrize(
    "handler",
    [
        pytest.param(_execute_handler(execute_status=503), id="execute-503"),
        pytest.param(_execute_handler(result_status=502), id="result-502"),
        pytest.param(_execute_handler(execute_status=429), id="execute-429"),
        pytest.param(_execute_handler(result_status=429), id="result-429"),
        pytest.param(_execute_handler(execute_body={"executionResponse": None}), id="malformed"),
    ],
)
def test_an_execution_service_fault_is_a_read_error(
    handler: Callable[[mw.httpx.Request], mw.httpx.Response], _no_backoff: None
) -> None:
    with pytest.raises(WorkspaceReadError, match="could not execute metric"):
        _http_workspace(handler).execute_metric("m")


def test_conversation_items_accept_items_or_data_and_reject_anything_else() -> None:
    items = [{"content": {"suggestions": {"actions": []}}}]
    assert _http_workspace(lambda r: mw.httpx.Response(200, json={"items": items})).conversation_items("c") == items
    assert _http_workspace(lambda r: mw.httpx.Response(200, json={"data": []})).conversation_items("c") == []
    with pytest.raises(WorkspaceReadError, match="no items list"):
        _http_workspace(lambda r: mw.httpx.Response(200, json={"unexpected": []})).conversation_items("c")
    with pytest.raises(WorkspaceReadError, match="could not read conversation"):
        _http_workspace(lambda r: mw.httpx.Response(500, json={})).conversation_items("c")


# --- second review round ----------------------------------------------------------------------


def test_a_failed_restore_never_lets_the_run_pass() -> None:
    # Every check passes, the restore fails: the run is unscored, so a single-run item cannot pass its gate.
    ws = _FakeWorkspace({"average_product_cost": _AVG_COST})
    ws.restore_fails = True
    write = {"metric_id": "average_product_cost", "maql": "SELECT AVG({fact/order_unit_cost})", "created_new": False}

    def _rename(message: str) -> None:
        ws.metrics["average_product_cost"] = {**_AVG_COST, "title": "Avg Unit Cost"}

    with _run_env([_turn("Renamed.", write)], ws, on_send=_rename):
        summary = _run({"expected_update": {"metric_id": "average_product_cost", "title": "Avg Unit Cost"}})
    run = summary.run_results[0]
    assert run.checks == {"metric_updated": True, "metric_scored": False}
    assert run.check_details["metric_scored"] == "harness: restore failed for ['average_product_cost']"
    assert run.harness_error == "restore failed for ['average_product_cost']"
    assert run.passed is False and summary.pass_at_k is False and summary.pass_power_k is False


def test_a_failed_restore_labels_the_run_error() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})
    ws.restore_fails = True
    write = {"metric_id": "net_sales", "maql": "SELECT 1", "created_new": False}
    result, scores = _evaluate({"candidates": ["SELECT 1"]}, [_turn("Updated.", write)], ws)
    assert isinstance(result, MetricSkillAssertionError)
    assert scores["eval_error"] == 1
    assert "Harness error" in str(result)


@pytest.mark.parametrize(
    "suggestions",
    [{"actions": ["invalid"]}, {"actions": "Show it"}, {"actions": {}}],
    ids=["action-not-object", "actions-not-list", "actions-empty-object"],
)
def test_malformed_suggestion_actions_are_a_harness_error(suggestions: dict) -> None:
    ws = _FakeWorkspace({})
    ws.items = [{"content": {"suggestions": suggestions}}]
    with _run_env([_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"})], ws):
        summary = _run({"candidates": ["SELECT 1"], "expect_suggestions": True})
    assert summary.best.checks["metric_suggestions"] is False
    assert "unreadable suggestion actions" in summary.best.harness_error


def test_an_execution_response_that_is_not_an_object_is_a_read_error() -> None:
    handler = _execute_handler(execute_body={"executionResponse": ["unexpected"]})
    with pytest.raises(WorkspaceReadError, match="no executionResult"):
        _http_workspace(handler).execute_metric("m")


@pytest.mark.parametrize("failure", ["timeout", "bad-json"])
def test_an_execution_that_cannot_be_read_is_a_read_error(failure: str) -> None:
    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        if failure == "timeout":
            raise mw.httpx.ReadTimeout("slow", request=request)
        return mw.httpx.Response(200, content=b"not json")

    with pytest.raises(WorkspaceReadError, match="could not execute metric m"):
        _http_workspace(_handler).execute_metric("m")


def test_judge_provider_errors_cover_openai_when_it_is_installed_and_transport_always() -> None:
    errors = metric_skill_mod._judge_provider_errors()
    assert {mw.httpx.HTTPError, TimeoutError, ConnectionError} <= set(errors)
    with patch.dict(sys.modules, {"openai": None}):
        assert metric_skill_mod._judge_provider_errors() == (mw.httpx.HTTPError, TimeoutError, ConnectionError)


def test_a_write_whose_result_is_not_an_object_is_ignored() -> None:
    events = [
        ToolCallEvent(function_name="search_objects", function_arguments="{}", result='{"objects": []}'),
        ToolCallEvent(function_name="create_metric", function_arguments="{}", result=""),
        ToolCallEvent(function_name="create_metric", function_arguments="{}", result='["not", "an", "object"]'),
        ToolCallEvent(function_name="create_metric", function_arguments="{}", result='{"data": {"metric_id": "m"}}'),
    ]
    assert metric_skill_mod._successful_writes(events) == [{"metric_id": "m"}]


def test_a_guarded_metric_missing_from_the_snapshot_is_left_alone() -> None:
    ws = _FakeWorkspace({})
    assert metric_skill_mod._restore_workspace(ws, {}, [], ("not_there",)) == []
    assert ws.restored == []


def test_a_guarded_metric_that_cannot_be_recreated_is_reported() -> None:
    ws = _FakeWorkspace({})
    ws.restore_fails = True
    assert metric_skill_mod._restore_workspace(ws, {"net_sales": _NET_SALES}, [], ("net_sales",)) == ["net_sales"]
    assert ws.restored == [("net_sales", False)]


# --- third review round -----------------------------------------------------------------------


def test_a_rate_limit_is_retried_before_the_metric_is_judged(_no_backoff: None) -> None:
    statuses = iter([429, 200])

    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        if request.method == "POST":
            return mw.httpx.Response(next(statuses), json={"executionResponse": {"links": {"executionResult": "r1"}}})
        return mw.httpx.Response(200, json={"data": [[1]]})

    assert _http_workspace(_handler).execute_metric("m") is None


@pytest.mark.parametrize(
    ("result", "computes"),
    [
        pytest.param({"json": {"data": []}}, True, id="empty-data"),
        pytest.param({"content": b"not json"}, False, id="not-json"),
        pytest.param({"json": {"unexpected": 1}}, False, id="no-data-list"),
        pytest.param({"json": ["not", "an", "object"]}, False, id="not-an-object"),
    ],
)
def test_a_result_must_carry_its_data_list(result: dict, computes: bool) -> None:
    def _handler(request: mw.httpx.Request) -> mw.httpx.Response:
        if request.method == "POST":
            return mw.httpx.Response(200, json={"executionResponse": {"links": {"executionResult": "r1"}}})
        return mw.httpx.Response(200, **result)

    ws = _http_workspace(_handler)
    if computes:
        assert ws.execute_metric("m") is None
    else:
        with pytest.raises(WorkspaceReadError, match="could not execute metric m"):
            ws.execute_metric("m")


def test_the_first_proposal_falls_back_to_the_first_write_not_the_last() -> None:
    ws = _FakeWorkspace({})
    turns = [
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 2", "created_new": True}),
        _turn("Fixed.", {"metric_id": "m", "maql": "SELECT 1"}),
    ]
    with _run_env(turns, ws):
        summary = _run(
            {
                "candidates": ["SELECT 1"],
                "user_replies": ["Make it SELECT 1."],
                "run_all_replies": True,
                "score_first_proposal": True,
            }
        )
    assert summary.best.checks["maql_correct"] is True
    assert summary.best.diagnostics == {"metric_first_proposal_correct": False}
    assert summary.best.check_details["metric_first_proposal_correct"] == {"proposed": "SELECT 2"}


def test_a_guarded_metric_overwritten_and_removed_is_recreated_once_and_not_reported() -> None:
    ws = _FakeWorkspace({})  # The run wrote over net_sales, then removed it.
    writes = [{"metric_id": "net_sales", "maql": "SELECT 1", "created_new": False}]
    assert metric_skill_mod._restore_workspace(ws, {"net_sales": _NET_SALES}, writes, ("net_sales",)) == []
    assert ws.restored == [("net_sales", False)]
    assert ws.metrics["net_sales"] == _NET_SALES


def test_a_chat_failure_in_a_scripted_turn_fails_the_run_after_a_correct_write() -> None:
    ws = _FakeWorkspace({})
    turns: list[ChatResult | Exception] = [
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "created_new": True}),
        ChatError("stream broke"),
    ]
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "user_replies": ["Now make it hidden."], "run_all_replies": True}, turns, ws
    )
    assert isinstance(result, MetricSkillAssertionError)
    assert scores["metric_created"] == 1.0 and scores["maql_correct"] == 1.0
    assert "eval_error" not in scores  # The agent's chat failed: a FAIL, not a harness ERROR.
    assert result.failed_runs[0]["exit_reason"] == LoopExit.CHAT_ERROR.value


def test_a_completed_script_without_a_further_write_still_passes() -> None:
    ws = _FakeWorkspace({})
    turns = [_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "created_new": True}), _turn("You're welcome.")]
    with _run_env(turns, ws):
        summary = _run({"candidates": ["SELECT 1"], "user_replies": ["Thanks."], "run_all_replies": True})
    assert summary.best.exit_reason == LoopExit.STOPPED_EARLY
    assert summary.pass_at_k is True


def test_an_unscored_run_counts_as_metric_scored_false_alone_for_quality() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 502"
    result, ctx = _evaluate_ctx(
        {"candidates": ["SELECT 1"], "expect_suggestions": True},
        [_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"})],
        ws,
    )
    assert ctx.quality.call_args.kwargs["strict_checks"] == {"metric_scored": False}
    assert [k for k, v in result.detail.items() if isinstance(v, bool)] == ["metric_scored"]
    assert result.detail["unscored_checks"] == {
        "metric_created": True,
        "maql_correct": True,
        "metric_suggestions": False,
    }


def test_a_graded_run_is_the_best_run_before_an_unscored_one() -> None:
    ws = _FakeWorkspace({})
    sent = {"n": 0}

    def _second_run_cannot_read(_message: str) -> None:
        sent["n"] += 1
        if sent["n"] == 2:
            ws.read_error = "HTTP 502"

    turns = [
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 2", "title": "M"}),
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"}),
    ]
    with _run_env(turns, ws, on_send=_second_run_cannot_read):
        summary = run_agentic_metric_skill(
            "http://h", "t", "ws", "q", {"candidates": ["SELECT 1"], "expect_suggestions": True}, k=2
        )
    graded, unscored = summary.run_results
    assert graded.harness_error is None and unscored.harness_error is not None
    assert summary.best is graded


def test_the_assignment_search_gives_up_instead_of_stalling() -> None:
    same = [{"metric_id": f"m{i}", "maql": "SELECT 1"} for i in range(8)]
    expected = (*(("SELECT 1",),) * 8, ("SELECT 2",))
    with pytest.raises(metric_skill_mod.MetricMatchUndecided, match="no verdict after"):
        _match_expected_metrics(expected, same)


def test_an_undecided_match_is_a_harness_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(metric_skill_mod, "_MATCH_SEARCH_STEPS", 1)
    ws = _FakeWorkspace({})
    both = [{"metric_id": "a", "maql": "SELECT 1"}, {"metric_id": "b", "maql": "SELECT 2"}]
    with _run_env([_turn("Created both.", *both)], ws) as (client, _):
        summary = _run({"expected_metrics": [["SELECT 1"], ["SELECT 2"]], "user_replies": ["Yes."]})
    assert client.send_message.call_count == 1
    assert summary.best.checks["metric_all_created"] is False
    assert (summary.best.harness_error or "").startswith("metric_all_created: no verdict after 1 assignments")


def test_a_malformed_write_result_does_not_stop_the_cleanup_of_the_others() -> None:
    ws = _FakeWorkspace({})
    turn = ChatResult.model_validate(
        {
            "textResponse": "Created.",
            "toolCallEvents": [
                {"functionName": "create_metric", "functionArguments": "{}", "result": '["bad"]'},
                {
                    "functionName": "create_metric",
                    "functionArguments": "{}",
                    "result": json.dumps({"data": {"metric_id": "m", "maql": "SELECT 1", "created_new": True}}),
                },
            ],
        }
    )
    with _run_env([turn], ws), patch("gooddata_eval.core.agentic.metric_skill._delete_metric") as delete:
        summary = _run({"candidates": ["SELECT 1"]})
    assert summary.best.passed
    assert [c.args[2] for c in delete.call_args_list] == ["m"]


# --- myhoai review ------------------------------------------------------------------------------


@pytest.mark.parametrize(
    ("raw", "key"),
    [
        ({"maql": "SELECT 1", "expect_no_overwirte": True}, "expect_no_overwrite"),
        ({"maql": "SELECT 1", "expected_feilds": {"title": "X"}}, "expected_fields"),
        ([{"maql": "SELECT 1", "rubirc": "Asks first."}], "rubric"),
        ({"maql": "SELECT 1", "user_reply": ["Yes"]}, "user_replies"),
    ],
)
def test_a_misspelt_option_key_beside_the_maql_fails_loudly(raw: Any, key: str) -> None:
    with pytest.raises(ValueError, match=f"did you mean '{key}'"):
        parse_expectation(raw)


def test_every_field_a_live_candidate_carries_stays_the_original_shape() -> None:
    # The keys of the metric_skill dataset items on 2026-11-20: a create_metric result beside the MAQL.
    candidate = {
        "maql": "SELECT 1",
        "title": "X",
        "metric_id": "x",
        "description": "",
        "tags": [],
        "format": "#,##0",
        "created_new": True,
        "message": "Created.",
    }
    assert parse_expectation([candidate]).legacy


@pytest.mark.parametrize(
    "raw",
    [
        {"expect_no_overwrite": True},
        {"confirmation_turn": 2, "user_replies": ["Yes"]},
        {"expect_no_deletion": ["net_sales"]},
        {"expect_confirmation_stop": True, "expect_no_overwrite": True},
    ],
)
def test_checks_that_only_forbid_are_not_an_item_alone(raw: dict) -> None:
    with pytest.raises(ValueError, match="pass an agent that does nothing"):
        parse_expectation(raw)


def test_a_refusal_alone_is_still_an_item() -> None:
    # Not writing is what expect_no_create asks for, and it needs a completed answer.
    assert parse_expectation({"expect_no_create": True}).expect_no_create


def test_a_failed_read_leaves_only_its_own_check_unscored() -> None:
    ws = _FakeWorkspace({})
    ws.execute_error = "execute: HTTP 400 bad MAQL"
    ws.items = [{"content": {"suggestions": {"actions": [{"query": "Show M by month"}]}}}]

    def _unreadable(_metric_id: str) -> dict | None:
        raise WorkspaceReadError("HTTP 502")

    ws.get_metric = _unreadable  # type: ignore[method-assign]
    with _run_env([_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"})], ws):
        summary = _run(
            {
                "candidates": ["SELECT 1"],
                "expected_fields": {"title": "M"},
                "expect_executes": True,
                "expect_suggestions": True,
            }
        )
    run = summary.best
    assert run.checks == {
        "metric_created": True,
        "maql_correct": True,
        "metric_fields_correct": False,
        "metric_executes": False,
        "metric_suggestions": True,
    }
    assert run.unscored == ["metric_fields_correct"]
    assert run.check_details["metric_fields_correct"] == "harness: HTTP 502"
    assert run.check_details["metric_executes"] == "execute: HTTP 400 bad MAQL"


def test_a_run_that_failed_a_graded_check_is_a_fail_despite_an_unread_one() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 502"
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "expect_suggestions": True},
        [_turn("Created.", {"metric_id": "m", "maql": "SELECT 2", "title": "M"})],
        ws,
    )
    assert isinstance(result, MetricSkillAssertionError)
    assert "eval_error" not in scores
    assert "Harness error" not in str(result)
    assert result.failed_runs[0]["outcome"] == {"status": "fail", "reason": "success"}


def test_a_run_whose_only_failures_are_unread_is_an_error() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 502"
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "expect_suggestions": True},
        [_turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"})],
        ws,
    )
    assert scores["eval_error"] == 1
    assert result.failed_runs[0]["outcome"] == {"status": "error", "reason": "judge_failed"}


def test_a_chat_failure_with_an_unread_check_is_a_fail_of_that_exit() -> None:
    ws = _FakeWorkspace({})
    ws.read_error = "HTTP 502"
    turns: list[ChatResult | Exception] = [
        _turn("Created.", {"metric_id": "m", "maql": "SELECT 1", "title": "M"}),
        ChatError("stream broke"),
    ]
    result, scores = _evaluate(
        {"candidates": ["SELECT 1"], "expect_suggestions": True, "user_replies": ["Yes."], "run_all_replies": True},
        turns,
        ws,
    )
    assert "eval_error" not in scores
    assert result.failed_runs[0]["outcome"] == {"status": "fail", "reason": "chat_error"}


# --- CodeRabbit, fourth round -------------------------------------------------------------------


def test_a_silent_agent_does_not_pass_a_refusal() -> None:
    ws = _FakeWorkspace({})
    with _run_env([_turn("")], ws):
        summary = _run({"expect_no_create": True})
    run = summary.best
    assert run.exit_reason == LoopExit.AGENT_SILENT
    assert run.checks == {"metric_not_created": False}
    assert run.check_details["metric_not_created"] == "the agent never completed an answer"
    assert run.passed is False


def test_a_guarded_metric_the_run_left_alone_is_not_restored() -> None:
    ws = _FakeWorkspace({"net_sales": _NET_SALES})
    with _run_env([_turn("I cannot delete metrics.")], ws):
        summary = _run({"expect_no_create": True, "expect_no_deletion": ["net_sales"]})
    assert summary.best.checks == {"metric_not_created": True, "metric_none_deleted": True}
    assert summary.best.passed
    assert ws.restored == []
