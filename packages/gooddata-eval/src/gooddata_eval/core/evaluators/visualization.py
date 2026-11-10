# (C) 2026 GoodData Corporation
"""Agentic visualization evaluator — ported from gdc-nas tavern-e2e app/vis_agentic.py."""

import re
from collections.abc import Mapping
from dataclasses import dataclass, field, replace
from datetime import date
from typing import Any

from gooddata_eval.core.chat.render import render_answer_text
from gooddata_eval.core.chat.sse_client import ADHOC_VIZ_ID
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import (
    ChatResult,
    CreatedVisualization,
    DatasetItem,
    ToolCallEvent,
    timeline_detail,
)
from gooddata_eval.core.number_format import check_format_intents, validate_format_intents
from gooddata_eval.core.scoring import (
    bucket_layout,
    check_buckets,
    check_filters,
    check_metric_layout,
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
    # Whether each field sits in the expected bucket. None when the expectation does not ask
    # (`buckets_strict`), so the check neither gates nor shows.
    buckets_correct: bool | None = None
    expected_buckets: dict[str, list[str]] | None = None
    actual_buckets: dict[str, list[str]] | None = None
    # Why `metrics_correct` is False although the metric set matched: order or axis.
    metric_layout_problems: list[str] = field(default_factory=list)
    # The item-level checks of `ExpectationOptions`. None means the item does not ask for one.
    expects_visualization: bool = True
    visualization_optional: bool = False
    answer_correct: bool | None = None
    answer_problems: list[str] = field(default_factory=list)
    format_correct: bool | None = None
    format_problems: list[str] = field(default_factory=list)
    part_present: bool | None = None

    @property
    def scored_without_chart(self) -> bool:
        """Whether the run is scored on the answer alone: no chart is expected, or an optional one was not shown."""
        return not self.expects_visualization or (self.visualization_optional and not self.visualization_created)

    @property
    def strict_pass(self) -> bool:
        if self.scored_without_chart:
            return not self.visualization_created and self.answer_correct is not False
        return (
            self.visualization_created
            and self.cross_ref_valid
            and self.metrics_correct
            and self.dimensions_correct
            and self.filters_correct
            and self.sorts_correct
            and self.viz_type_hard
            and (self.executed or not self.requires_execution)
            and self.buckets_correct is not False
            and self.answer_correct is not False
            and self.format_correct is not False
            and self.part_present is not False
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
                self.buckets_correct is True,
                self.answer_correct is True,
                self.format_correct is True,
                self.part_present is True,
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


@dataclass(frozen=True)
class ExpectationOptions:
    """The item-level keys of a visualization expectation, beside its candidate charts.

    Every key is opt-in: the defaults score an item exactly as before they existed.
    - ``expects_visualization`` False: the agent must answer without a chart, for example by
      asking for the part the request leaves out. The run then stops after one turn, since a
      simulated reply would push the agent into building the chart.
    - ``visualization_optional``: either outcome is right -- an answer without a chart, scored on the
      answer alone, or a chart, scored against the candidates and the answer. For a request
      the chart type cannot draw as asked, where asking back and building the closest chart
      with an explanation are both correct. The run stops after one turn, as above.
    - ``answer_must_include`` / ``answer_must_not_match``: regular expressions, matched without
      regard to case against everything the final turn said. Every ``must_include`` pattern has
      to match and no ``must_not_match`` pattern may.
    - ``format_intents``: per metric uri, how its numbers must read (see ``number_format``).
    - ``requires_visualization_part``: the chart must come back as a part of the answer. Without
      it, a chart that exists only in the tool arguments is scored like one the user saw.
    """

    requires_execution: bool = False
    expects_visualization: bool = True
    visualization_optional: bool = False
    answer_must_include: tuple[str, ...] = ()
    answer_must_not_match: tuple[str, ...] = ()
    format_intents: Mapping[str, Mapping[str, Any] | None] | None = None
    requires_visualization_part: bool = False


def _regex_error(pattern: str) -> str | None:
    try:
        re.compile(pattern)
    except re.error as exc:
        return str(exc)
    return None


def _patterns(expected_output: dict, key: str) -> tuple[str, ...]:
    patterns = expected_output.get(key, [])
    if not isinstance(patterns, list) or not all(isinstance(p, str) and p for p in patterns):
        raise ValueError(f"{key} must be a list of regular expressions, got {patterns!r}")
    for pattern in patterns:
        error = _regex_error(pattern)
        if error is not None:
            raise ValueError(f"{key} holds an invalid regular expression {pattern!r}: {error}")
    return tuple(patterns)


# Every key a visualization expectation may state: the candidates and the options above.
_EXPECTATION_KEYS = frozenset(
    {
        "visualization",
        "expected_outputs",
        "requires_execution",
        "expects_visualization",
        "visualization_optional",
        "answer_must_include",
        "answer_must_not_match",
        "format_intents",
        "requires_visualization_part",
    }
)


def _candidate_charts(expected_output: dict) -> list[object]:
    """The candidate charts an expectation lists, in either the `visualization` or the `expected_outputs` form."""
    raw = expected_output.get("visualization")
    charts = raw if isinstance(raw, list) else [raw] if raw is not None else []
    for entry in expected_output.get("expected_outputs") or []:
        charts.append(entry.get("visualization", entry) if isinstance(entry, dict) else entry)
    return charts


def _unread_chart_keys(chart: object) -> list[str]:
    """Keys of a candidate chart that `CreatedVisualization` does not read, so its parse would drop them."""
    if not isinstance(chart, dict):
        return []
    fields = CreatedVisualization.model_fields
    read = set(fields) | {info.alias for info in fields.values() if info.alias}
    return sorted(set(chart) - read)


def expectation_options(expected_output: object) -> ExpectationOptions:
    """Read and validate the item-level keys of a visualization expectation.

    Raises:
        ValueError: a key is malformed. Loud, before any request: a typo would otherwise
            assert nothing and read green.
    """
    if not isinstance(expected_output, dict):
        return ExpectationOptions()
    # A misspelled key would otherwise be dropped, and the check it asks for would never run.
    unknown = sorted(set(expected_output) - _EXPECTATION_KEYS)
    if unknown:
        raise ValueError(f"the expectation states {unknown}, which is not one of {sorted(_EXPECTATION_KEYS)}")
    for chart in _candidate_charts(expected_output):
        unread = _unread_chart_keys(chart)
        if unread:
            raise ValueError(f"a candidate chart states {unread}, which the chart model does not read")
    expects = expected_output.get("expects_visualization", True)
    if not isinstance(expects, bool):
        raise ValueError(f"expects_visualization must be true or false, got {expects!r}")
    optional = expected_output.get("visualization_optional", False)
    if not isinstance(optional, bool):
        raise ValueError(f"visualization_optional must be true or false, got {optional!r}")
    if optional and not expects:
        raise ValueError("visualization_optional and expects_visualization false contradict each other")
    # Checked here because every path reads the options: a candidate parser that only drops
    # the candidates would score a contradictory item as a no-chart item.
    if not expects and any(expected_output.get(key) is not None for key in ("visualization", "expected_outputs")):
        raise ValueError("an expectation without a chart must not list 'visualization' candidates")
    part = expected_output.get("requires_visualization_part", False)
    if not isinstance(part, bool):
        raise ValueError(f"requires_visualization_part must be true or false, got {part!r}")
    intents = expected_output.get("format_intents")
    if intents is not None:
        validate_format_intents(intents)
    if not expects and (intents is not None or part):
        raise ValueError("an expectation without a chart cannot state format_intents or requires_visualization_part")
    return ExpectationOptions(
        requires_execution=requires_execution_of(expected_output),
        expects_visualization=expects,
        visualization_optional=optional,
        answer_must_include=_patterns(expected_output, "answer_must_include"),
        answer_must_not_match=_patterns(expected_output, "answer_must_not_match"),
        format_intents=intents,
        requires_visualization_part=part,
    )


def check_answer(text: str, must_include: tuple[str, ...], must_not_match: tuple[str, ...]) -> list[str]:
    """What the answer text gets wrong against the patterns; [] when it gets nothing wrong.

    A typographic apostrophe is read as a plain one, so "aren’t" matches a pattern written
    with "aren't".
    """
    text = text.replace("\u2019", "'")
    problems = [f"the answer does not match {p!r}" for p in must_include if not re.search(p, text, re.IGNORECASE)]
    for pattern in must_not_match:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            problems.append(f"the answer matches {pattern!r}: {match.group(0)!r}")
    return problems


def with_options(
    ev: EvaluationResult,
    options: ExpectationOptions,
    actual: CreatedVisualization | None,
    tool_call_events: list[ToolCallEvent],
    answer_text: str,
    *,
    interrupted: bool = False,
) -> EvaluationResult:
    """``ev`` with the item-level checks of ``options`` applied.

    ``interrupted`` marks a run whose chat request failed: its answer is cut off, so it
    cannot pass an item that accepts no chart.
    """
    asks_answer = bool(options.answer_must_include or options.answer_must_not_match)
    answer_problems = (
        check_answer(answer_text, options.answer_must_include, options.answer_must_not_match) if asks_answer else []
    )
    # The fallback chart, built from the tool arguments when the answer carried no part, has
    # this id. The user never saw it, so it is no chart for an item that accepts none.
    shown = actual is not None and actual.id != ADHOC_VIZ_ID
    accepts_no_chart = not options.expects_visualization or options.visualization_optional
    if accepts_no_chart and not shown:
        ev = replace(ev, visualization_created=False)
    # An item that accepts no chart still needs an answer. A silent turn ends with none, and a
    # failed chat request with a cut-off one. Either would otherwise pass as a correct "no chart".
    if accepts_no_chart and not shown and interrupted:
        answer_problems = [*answer_problems, "the chat request failed before the answer ended"]
    elif accepts_no_chart and not shown and not answer_text.strip():
        answer_problems = [*answer_problems, "the agent returned neither a chart nor an answer"]
    checks_answer = asks_answer or bool(answer_problems)
    format_problems = check_format_intents(options.format_intents, tool_call_events) if options.format_intents else []
    return replace(
        ev,
        expects_visualization=options.expects_visualization,
        visualization_optional=options.visualization_optional,
        answer_correct=not answer_problems if checks_answer else None,
        answer_problems=answer_problems,
        format_correct=not format_problems if options.format_intents else None,
        format_problems=format_problems,
        part_present=shown if options.requires_visualization_part else None,
    )


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
            buckets_correct=False if expected.buckets_strict else None,
            expected_buckets=bucket_layout(expected) if expected.buckets_strict else None,
        )
    cross_ref_valid, cross_ref_errors = validate_cross_references(actual)
    act_metric_uris = get_metric_uri_set(actual)
    act_dim_uris = get_dimension_uri_set(actual)
    filter_scores = check_filters(expected, actual, today)
    metric_layout_problems = check_metric_layout(expected, actual)
    return EvaluationResult(
        visualization_created=True,
        cross_ref_valid=cross_ref_valid,
        metrics_correct=act_metric_uris == exp_metric_uris and not metric_layout_problems,
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
        buckets_correct=check_buckets(expected, actual),
        expected_buckets=bucket_layout(expected) if expected.buckets_strict else None,
        actual_buckets=bucket_layout(actual) if expected.buckets_strict else None,
        metric_layout_problems=metric_layout_problems,
    )


def _no_candidate_result(actual: CreatedVisualization | None, skill_activated: bool) -> EvaluationResult:
    """The result for an item that expects no chart: only whether one was built counts."""
    return EvaluationResult(
        visualization_created=actual is not None,
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
        cross_ref_errors=[],
        expected_metric_uris=set(),
        actual_metric_uris=get_metric_uri_set(actual) if actual else set(),
        expected_dim_uris=set(),
        actual_dim_uris=get_dimension_uri_set(actual) if actual else set(),
        expected_filters={category: [] for category in _NO_FILTERS},
        actual_filters={category: [] for category in _NO_FILTERS},
        expected_sorts=[],
        actual_sorts=[],
        expects_visualization=False,
    )


def _evaluate_against_candidates(
    expected_outputs: list[CreatedVisualization],
    actual: CreatedVisualization | None,
    skill_activated: bool = False,
    today: date | None = None,
) -> tuple[EvaluationResult, CreatedVisualization | None]:
    if not expected_outputs:
        return _no_candidate_result(actual, skill_activated), None
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
    if expected_output.get("expects_visualization") is False:
        # `expectation_options`, read first, has rejected candidates listed beside the flag.
        return []
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
    answer = {
        **({"answer_correct": ev.answer_correct} if ev.answer_correct is not None else {}),
        **({"answer_problems": ev.answer_problems} if ev.answer_problems else {}),
    }
    if ev.scored_without_chart:
        return {
            "no_chart": not ev.visualization_created,
            **answer,
            "skill_activated": ev.skill_activated,
            "actual_metric_uris": sorted(ev.actual_metric_uris),
            "actual_dim_uris": sorted(ev.actual_dim_uris),
        }
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
        **({"metric_layout_problems": ev.metric_layout_problems} if ev.metric_layout_problems else {}),
        # Top level only when the expectation asks for it: a check the item does not gate on
        # must not lift `quality_score`, which counts every top-level boolean.
        **({"buckets_correct": ev.buckets_correct} if ev.buckets_correct is not None else {}),
        **(
            {"buckets": {"expected": ev.expected_buckets, "actual": ev.actual_buckets}}
            if ev.expected_buckets is not None
            else {}
        ),
        # Nested: `quality_score` counts every top-level boolean, and a check an item does not
        # gate on must not lower it. `executed` joins the top level only when it gates.
        "execution": {
            "executed": ev.executed,
            "required": ev.requires_execution,
            "stated_value_matches": ev.stated_value_matches,
        },
        **({"executed": ev.executed} if ev.requires_execution else {}),
        **answer,
        **({"format_correct": ev.format_correct} if ev.format_correct is not None else {}),
        **({"format_problems": ev.format_problems} if ev.format_problems else {}),
        **({"part_present": ev.part_present} if ev.part_present is not None else {}),
    }


class VisualizationEvaluator:
    test_kind = "visualization"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        options = expectation_options(item.expected_output)
        candidates = _parse_expected(item.expected_output)
        actual = _extract_actual(chat_result)
        skill_activated = _check_visualization_skill_activated(chat_result.tool_call_events)
        ev, _best_expected = _evaluate_against_candidates(candidates, actual, skill_activated)
        ev = with_execution(ev, chat_result.tool_call_events, chat_result.text_response, options.requires_execution)
        ev = with_options(ev, options, actual, chat_result.tool_call_events, render_answer_text(chat_result))
        return ItemEvaluation(
            passed=ev.strict_pass,
            rank_key=(ev.strict_pass, ev.strict_checks_passed_count),
            detail={
                **evaluation_result_detail(ev),
                **timeline_detail(chat_result.tool_call_events, chat_result.reasoning_step_events),
            },
        )
