# (C) 2026 GoodData Corporation
"""Agentic visualization evaluator — ported from gdc-nas tavern-e2e app/vis_agentic.py."""

from dataclasses import dataclass

from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, CreatedVisualization, DatasetItem
from gooddata_eval.core.scoring import (
    check_filters,
    check_viz_type,
    get_dimension_uri_set,
    get_metric_uri_set,
    validate_cross_references,
)


@dataclass
class EvaluationResult:
    visualization_created: bool
    cross_ref_valid: bool
    metrics_correct: bool
    dimensions_correct: bool
    filters_correct: bool
    viz_type_hard: bool
    filter_date_score: bool
    filter_ranking_score: bool
    filter_attribute_score: bool
    cross_ref_errors: list[str]
    expected_metric_uris: set[str]
    actual_metric_uris: set[str]
    expected_dim_uris: set[str]
    actual_dim_uris: set[str]

    @property
    def strict_pass(self) -> bool:
        return (
            self.visualization_created
            and self.cross_ref_valid
            and self.metrics_correct
            and self.dimensions_correct
            and self.filters_correct
            and self.viz_type_hard
        )

    @property
    def strict_checks_passed_count(self) -> int:
        return sum(
            [
                self.cross_ref_valid,
                self.metrics_correct,
                self.dimensions_correct,
                self.filters_correct,
                self.viz_type_hard,
            ]
        )


def _evaluate_visualization(expected: CreatedVisualization, actual: CreatedVisualization | None) -> EvaluationResult:
    exp_metric_uris = get_metric_uri_set(expected)
    exp_dim_uris = get_dimension_uri_set(expected)
    if actual is None:
        return EvaluationResult(
            visualization_created=False,
            cross_ref_valid=False,
            metrics_correct=False,
            dimensions_correct=False,
            filters_correct=False,
            viz_type_hard=False,
            filter_date_score=False,
            filter_ranking_score=False,
            filter_attribute_score=False,
            cross_ref_errors=["No visualization was created"],
            expected_metric_uris=exp_metric_uris,
            actual_metric_uris=set(),
            expected_dim_uris=exp_dim_uris,
            actual_dim_uris=set(),
        )
    cross_ref_valid, cross_ref_errors = validate_cross_references(actual)
    act_metric_uris = get_metric_uri_set(actual)
    act_dim_uris = get_dimension_uri_set(actual)
    filter_scores = check_filters(expected, actual)
    return EvaluationResult(
        visualization_created=True,
        cross_ref_valid=cross_ref_valid,
        metrics_correct=act_metric_uris == exp_metric_uris,
        dimensions_correct=act_dim_uris == exp_dim_uris,
        filters_correct=filter_scores.all_ok,
        viz_type_hard=check_viz_type(expected, actual),
        filter_date_score=filter_scores.date_ok,
        filter_ranking_score=filter_scores.ranking_ok,
        filter_attribute_score=filter_scores.attribute_ok,
        cross_ref_errors=cross_ref_errors,
        expected_metric_uris=exp_metric_uris,
        actual_metric_uris=act_metric_uris,
        expected_dim_uris=exp_dim_uris,
        actual_dim_uris=act_dim_uris,
    )


def _evaluate_against_candidates(
    expected_outputs: list[CreatedVisualization], actual: CreatedVisualization | None
) -> tuple[EvaluationResult, CreatedVisualization]:
    pairs = [(_evaluate_visualization(exp, actual), exp) for exp in expected_outputs]
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


class VisualizationEvaluator:
    test_kind = "visualization"

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation:
        candidates = _parse_expected(item.expected_output)
        actual = _extract_actual(chat_result)
        ev, _best_expected = _evaluate_against_candidates(candidates, actual)
        return ItemEvaluation(
            passed=ev.strict_pass,
            rank_key=(ev.strict_pass, ev.strict_checks_passed_count),
            detail={
                "visualization_created": ev.visualization_created,
                "cross_ref_valid": ev.cross_ref_valid,
                "cross_ref_errors": ev.cross_ref_errors,
                "metrics_correct": ev.metrics_correct,
                "dimensions_correct": ev.dimensions_correct,
                "filters_correct": ev.filters_correct,
                "filter_date_score": ev.filter_date_score,
                "filter_ranking_score": ev.filter_ranking_score,
                "filter_attribute_score": ev.filter_attribute_score,
                "viz_type_hard": ev.viz_type_hard,
                "expected_metric_uris": sorted(ev.expected_metric_uris),
                "actual_metric_uris": sorted(ev.actual_metric_uris),
                "expected_dim_uris": sorted(ev.expected_dim_uris),
                "actual_dim_uris": sorted(ev.actual_dim_uris),
            },
        )
