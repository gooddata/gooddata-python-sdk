# (C) 2026 GoodData Corporation
"""Agentic visualization evaluator — ported from gdc-nas tavern-e2e app/vis_agentic.py."""

import re
from dataclasses import dataclass, replace
from datetime import date
from typing import Any

from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import (
    ChatResult,
    CreatedVisualization,
    DatasetItem,
    ToolCallEvent,
    timeline_detail,
)
from gooddata_eval.core.scoring import (
    check_filters,
    check_sorts,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
    normalized_filters,
    normalized_sorts,
    validate_cross_references,
)

_NO_FILTERS: dict[str, list[str]] = {"date": [], "ranking": [], "attribute": []}


@dataclass
class EvaluationResult:
    visualization_created: bool
    cross_ref_valid: bool
    metrics_correct: bool
    dimensions_correct: bool
    filters_correct: bool
    sorts_correct: bool
    viz_type_hard: bool
    filter_date_score: bool
    filter_ranking_score: bool
    filter_attribute_score: bool
    skill_activated: bool
    cross_ref_errors: list[str]
    expected_metric_uris: set[str]
    actual_metric_uris: set[str]
    expected_dim_uris: set[str]
    actual_dim_uris: set[str]
    # Filters in the canonical form equality is tested on, keyed by the category each
    # `filter_*_score` covers. Reported alongside the booleans because a filter mismatch
    # is otherwise undiagnosable from a finished run.
    expected_filters: dict[str, list[str]]
    actual_filters: dict[str, list[str]]
    expected_sorts: list[str]
    actual_sorts: list[str]
    # Whether the agent ran the chart it built (see `execution_signals`). It gates
    # `strict_pass` only on an item whose expected output sets `requires_execution`: a
    # chart the user only looks at needs no run, a question that asks for a number does.
    executed: bool = False
    requires_execution: bool = False
    # Whether a number in the reply matches a value the chart returned. None when the reply
    # states no number. Reported only: reading numbers out of prose has false hits.
    stated_value_matches: bool | None = None

    @property
    def strict_pass(self) -> bool:
        return (
            self.visualization_created
            and self.cross_ref_valid
            and self.metrics_correct
            and self.dimensions_correct
            and self.filters_correct
            and self.sorts_correct
            and self.viz_type_hard
            and (self.executed or not self.requires_execution)
        )

    @property
    def strict_checks_passed_count(self) -> int:
        return sum(
            [
                self.cross_ref_valid,
                self.metrics_correct,
                self.dimensions_correct,
                self.filters_correct,
                self.sorts_correct,
                self.viz_type_hard,
            ]
        )


# A number as prose writes it: a sign before or after an optional currency symbol, thousands
# separators, decimals, then an optional K/M/B scale or a percent sign. Not preceded or
# followed by a word character, so "Q3", "viz_1" and "2x" are not read as numbers.
_NUMBER_RE = re.compile(
    r"(?<![\w.])(?P<sign>[-+]?)[$€£]?(?P<sign2>[-+]?)(?P<int>\d{1,3}(?:,\d{3})+|\d+)(?:\.(?P<frac>\d+))?"
    r"\s?(?P<suffix>[kKmMbB%])?(?!\w)"
)
_SCALES = {"k": 1e3, "m": 1e6, "b": 1e9}


def _numbers_in(text: str) -> list[tuple[float, int, str]]:
    """(value, decimals, suffix) for every number written in ``text``; suffix is lowercased."""
    out: list[tuple[float, int, str]] = []
    for m in _NUMBER_RE.finditer(text):
        integer, fraction = m.group("int").replace(",", ""), m.group("frac") or ""
        suffix = (m.group("suffix") or "").lower()
        value = float(f"{integer}.{fraction}" if fraction else integer)
        if "-" in (m.group("sign"), m.group("sign2")):
            value = -value
        out.append((value, len(fraction), suffix))
    return out


def _stated_matches(stated: tuple[float, int, str], raw: list[float], formatted: list[tuple[float, str]]) -> bool:
    """Whether one number from the reply is a rounding of a returned value."""
    value, decimals, suffix = stated
    half_step = 0.5 * 10**-decimals + 1e-9
    # Same number and same scale: "1.2" does not quote a formatted "1.2M".
    if any(abs(f - value) < 1e-9 and f_suffix == suffix for f, f_suffix in formatted):
        return True
    for v in raw:
        # A percent states the fraction times 100: "10%" quotes 0.1, and "0.1%" does not.
        if suffix == "%":
            if abs(v * 100 - value) <= half_step:
                return True
            continue
        scale = _SCALES.get(suffix, 1.0)
        if abs(v - value * scale) <= half_step * scale:
            return True
    return False


def _row_values(data: Any) -> tuple[list[float], list[tuple[float, str]]]:
    """Numeric cells of an execution result: the raw `rows`, and the (number, scale suffix)
    pairs read out of `formatted_rows` -- the display strings the agent is told to quote.
    A malformed result yields nothing rather than raising."""
    raw: list[float] = []
    formatted: list[tuple[float, str]] = []
    if not isinstance(data, dict):
        return raw, formatted
    rows, formatted_rows = data.get("rows"), data.get("formatted_rows")
    for row in rows if isinstance(rows, list) else []:
        if isinstance(row, dict):
            raw += [float(v) for v in row.values() if isinstance(v, (int, float)) and not isinstance(v, bool)]
    for row in formatted_rows if isinstance(formatted_rows, list) else []:
        if isinstance(row, dict):
            for v in row.values():
                if isinstance(v, str):
                    formatted += [(n[0], n[2]) for n in _numbers_in(v)]
    return raw, formatted


def execution_signals(tool_call_events: list[ToolCallEvent], reply_text: str | None) -> tuple[bool, bool | None]:
    """``(executed, stated_value_matches)`` for one conversation.

    ``executed`` is True when ``execute_visualization`` succeeded for a ref that a successful
    ``create_adhoc_visualization`` in the same conversation returned. The chart part of the
    answer carries no ref, so this cannot tell which of several built charts was shown.

    ``stated_value_matches`` is None when the reply states no number. Otherwise it is True
    when one of those numbers is a rounding of a value an execution returned, and False when
    none is -- including when nothing was executed, so the agent could not know the value.
    """
    created: set[str] = set()
    for tc in tool_call_events:
        if tc.function_name == "create_adhoc_visualization":
            result = tc.parsed_result()
            if not isinstance(result, dict):
                continue
            ref = result.get("ref") if result.get("status", "success") == "success" else None
            if isinstance(ref, str):
                created.add(ref)
    raw: list[float] = []
    formatted: list[tuple[float, str]] = []
    executed = False
    for tc in tool_call_events:
        if tc.function_name != "execute_visualization":
            continue
        result = tc.parsed_result()
        args = tc.parsed_arguments()
        if not isinstance(result, dict) or not isinstance(args, dict):
            continue
        ref = args.get("visualization_ref")
        if result.get("success") is True and isinstance(ref, str) and ref in created:
            executed = True
            r, f = _row_values(result.get("data"))
            raw += r
            formatted += f
    stated = _numbers_in(reply_text or "")
    if not stated:
        return executed, None
    return executed, any(_stated_matches(n, raw, formatted) for n in stated)


def with_execution(
    ev: EvaluationResult,
    tool_call_events: list[ToolCallEvent],
    reply_text: str | None,
    requires_execution: bool,
) -> EvaluationResult:
    """``ev`` with the execution signals of the conversation that produced it."""
    executed, stated_value_matches = execution_signals(tool_call_events, reply_text)
    return replace(
        ev, executed=executed, requires_execution=requires_execution, stated_value_matches=stated_value_matches
    )


def requires_execution_of(expected_output: object) -> bool:
    """The item-level `requires_execution` flag; absent or not a boolean reads as False."""
    return isinstance(expected_output, dict) and expected_output.get("requires_execution") is True


def _check_visualization_skill_activated(tool_call_events: list[ToolCallEvent]) -> bool:
    """Return True if set_skills was called with 'visualization' in skill_names."""
    for tc in tool_call_events:
        if tc.function_name == "set_skills":
            args = tc.parsed_arguments()
            skill_names = args.get("skill_names", [])
            if isinstance(skill_names, list) and "visualization" in skill_names:
                return True
    return False


def _evaluate_visualization(
    expected: CreatedVisualization,
    actual: CreatedVisualization | None,
    skill_activated: bool = False,
    today: date | None = None,
) -> EvaluationResult:
    # One anchor for the scoring and for the filters reported beside it. check_filters
    # already shares an anchor across its two sides, but resolving the reported filters
    # separately would let a run that straddles midnight report periods the score was
    # never computed from -- a detail that contradicts its own verdict.
    today = today or date.today()
    exp_metric_uris = get_metric_uri_set(expected)
    exp_dim_uris = get_dimension_uri_set(expected)
    if actual is None:
        return EvaluationResult(
            visualization_created=False,
            cross_ref_valid=False,
            metrics_correct=False,
            dimensions_correct=False,
            filters_correct=False,
            sorts_correct=False,
            viz_type_hard=False,
            filter_date_score=False,
            filter_ranking_score=False,
            filter_attribute_score=False,
            skill_activated=skill_activated,
            cross_ref_errors=["No visualization was created"],
            expected_metric_uris=exp_metric_uris,
            actual_metric_uris=set(),
            expected_dim_uris=exp_dim_uris,
            actual_dim_uris=set(),
            expected_filters=normalized_filters(expected, today),
            actual_filters={category: values.copy() for category, values in _NO_FILTERS.items()},
            expected_sorts=normalized_sorts(expected),
            actual_sorts=[],
        )
    cross_ref_valid, cross_ref_errors = validate_cross_references(actual)
    act_metric_uris = get_metric_uri_set(actual)
    act_dim_uris = get_dimension_uri_set(actual)
    filter_scores = check_filters(expected, actual, today)
    return EvaluationResult(
        visualization_created=True,
        cross_ref_valid=cross_ref_valid,
        metrics_correct=act_metric_uris == exp_metric_uris,
        dimensions_correct=act_dim_uris == exp_dim_uris,
        filters_correct=filter_scores.all_ok,
        sorts_correct=check_sorts(expected, actual),
        viz_type_hard=check_viz_type(expected, actual),
        filter_date_score=filter_scores.date_ok,
        filter_ranking_score=filter_scores.ranking_ok,
        filter_attribute_score=filter_scores.attribute_ok,
        skill_activated=skill_activated,
        cross_ref_errors=cross_ref_errors,
        expected_metric_uris=exp_metric_uris,
        actual_metric_uris=act_metric_uris,
        expected_dim_uris=exp_dim_uris,
        actual_dim_uris=act_dim_uris,
        expected_sorts=normalized_sorts(expected),
        actual_sorts=normalized_sorts(actual),
        expected_filters=normalized_filters(expected, today),
        actual_filters=normalized_filters(actual, today),
    )


def _evaluate_against_candidates(
    expected_outputs: list[CreatedVisualization],
    actual: CreatedVisualization | None,
    skill_activated: bool = False,
    today: date | None = None,
) -> tuple[EvaluationResult, CreatedVisualization]:
    # Anchored once here too: the candidates are ranked against each other, so letting
    # each resolve its own today could rank them on spans from different days.
    today = today or date.today()
    pairs = [(_evaluate_visualization(exp, actual, skill_activated, today), exp) for exp in expected_outputs]
    best_result, best_expected = max(pairs, key=lambda p: (p[0].strict_pass, p[0].strict_checks_passed_count))
    return best_result, best_expected


def _parse_expected(expected_output: dict) -> list[CreatedVisualization]:
    if not isinstance(expected_output, dict):
        raise ValueError("'expected_output' must be a JSON object")
    raw_viz = expected_output.get("visualization")
    if raw_viz is None:
        raise ValueError("'expected_output.visualization' is required")
    if isinstance(raw_viz, list):
        if not raw_viz:
            raise ValueError("'expected_output.visualization' array must not be empty")
        return [CreatedVisualization.model_validate(v) for v in raw_viz]
    if isinstance(raw_viz, dict):
        return [CreatedVisualization.model_validate(raw_viz)]
    raise ValueError("'expected_output.visualization' must be a JSON object or non-empty array")


def _extract_actual(chat_result: ChatResult) -> CreatedVisualization | None:
    cv = chat_result.created_visualizations
    if cv is None or not cv.objects:
        return None
    return cv.objects[0]


def evaluation_result_detail(ev: EvaluationResult) -> dict:
    """The per-check breakdown reported as ``detail`` for a visualization evaluation.

    Shared by the single-shot evaluator below and the agentic path
    (``core/agentic/visualization.py``) so both report the exact same shape.
    """
    return {
        "visualization_created": ev.visualization_created,
        "cross_ref_valid": ev.cross_ref_valid,
        "cross_ref_errors": ev.cross_ref_errors,
        "metrics_correct": ev.metrics_correct,
        "dimensions_correct": ev.dimensions_correct,
        "filters_correct": ev.filters_correct,
        "sorts_correct": ev.sorts_correct,
        "filter_date_score": ev.filter_date_score,
        "filter_ranking_score": ev.filter_ranking_score,
        "filter_attribute_score": ev.filter_attribute_score,
        "viz_type_hard": ev.viz_type_hard,
        "skill_activated": ev.skill_activated,
        "expected_metric_uris": sorted(ev.expected_metric_uris),
        "actual_metric_uris": sorted(ev.actual_metric_uris),
        "expected_dim_uris": sorted(ev.expected_dim_uris),
        "actual_dim_uris": sorted(ev.actual_dim_uris),
        "expected_filters": ev.expected_filters,
        "actual_filters": ev.actual_filters,
        "expected_sorts": ev.expected_sorts,
        "actual_sorts": ev.actual_sorts,
        # Nested: `quality_score` counts every top-level boolean, and a check an item does not
        # gate on must not lower it. `executed` joins the top level only when it gates.
        "execution": {
            "executed": ev.executed,
            "required": ev.requires_execution,
            "stated_value_matches": ev.stated_value_matches,
        },
        **({"executed": ev.executed} if ev.requires_execution else {}),
    }


class VisualizationEvaluator:
    test_kind = "visualization"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        candidates = _parse_expected(item.expected_output)
        actual = _extract_actual(chat_result)
        skill_activated = _check_visualization_skill_activated(chat_result.tool_call_events)
        ev, _best_expected = _evaluate_against_candidates(candidates, actual, skill_activated)
        ev = with_execution(
            ev, chat_result.tool_call_events, chat_result.text_response, requires_execution_of(item.expected_output)
        )
        return ItemEvaluation(
            passed=ev.strict_pass,
            rank_key=(ev.strict_pass, ev.strict_checks_passed_count),
            detail={
                **evaluation_result_detail(ev),
                **timeline_detail(chat_result.tool_call_events, chat_result.reasoning_step_events),
            },
        )
