# (C) 2026 GoodData Corporation
"""Registry mapping a dataset `test_kind` to its evaluator."""

from gooddata_eval.core.evaluators.alert_skill import AlertSkillEvaluator
from gooddata_eval.core.evaluators.base import Evaluator, ItemEvaluation
from gooddata_eval.core.evaluators.metric_skill import MetricSkillEvaluator
from gooddata_eval.core.evaluators.search_tool import SearchToolEvaluator
from gooddata_eval.core.evaluators.visualization import VisualizationEvaluator

__all__ = ["Evaluator", "ItemEvaluation", "get_evaluator", "supported_test_kinds"]

# Evaluators that do NOT require external credentials — imported and instantiated eagerly.
_EAGER_EVALUATORS: dict[str, Evaluator] = {
    ev.test_kind: ev
    for ev in (
        VisualizationEvaluator(),
        MetricSkillEvaluator(),
        AlertSkillEvaluator(),
        SearchToolEvaluator(),
    )
}

# LLM-judge evaluators (general_question, guardrail, dashboard_summary, knowledge_question)
# require the [llm-judge] extra. Their modules are imported lazily on first use so the CLI
# starts without openai.
#
# knowledge_question reuses GeneralQuestionEvaluator directly: both are free-text-rubric,
# LLM-judged prose answers -- knowledge_question just covers platform/product/policy facts
# instead of LDM-grounded ones. `ItemReport.test_kind` is tagged from the dataset item's own
# `test_kind` field (see runner.py), not from the evaluator class, so sharing one class
# across both kinds does not mislabel results.
_LAZY_EVALUATOR_MODULES: dict[str, str] = {
    "general_question": "gooddata_eval.core.evaluators.general_question",
    "guardrail": "gooddata_eval.core.evaluators.guardrail",
    "dashboard_summary": "gooddata_eval.core.evaluators.summary",
    "knowledge_question": "gooddata_eval.core.evaluators.general_question",
}
_LAZY_EVALUATOR_CLASSES: dict[str, str] = {
    "general_question": "GeneralQuestionEvaluator",
    "guardrail": "GuardrailEvaluator",
    "dashboard_summary": "DashboardSummaryEvaluator",
    "knowledge_question": "GeneralQuestionEvaluator",
}


def get_evaluator(test_kind: str) -> Evaluator:
    """Return the evaluator for `test_kind`, or raise KeyError if unsupported."""
    if test_kind in _EAGER_EVALUATORS:
        return _EAGER_EVALUATORS[test_kind]
    if test_kind in _LAZY_EVALUATOR_MODULES:
        import importlib  # noqa: PLC0415

        mod = importlib.import_module(_LAZY_EVALUATOR_MODULES[test_kind])
        cls = getattr(mod, _LAZY_EVALUATOR_CLASSES[test_kind])
        return cls()
    raise KeyError(test_kind)


def _openai_available() -> bool:
    import importlib.util  # noqa: PLC0415

    return importlib.util.find_spec("openai") is not None


def supported_test_kinds() -> set[str]:
    """Return all supported test_kind values.

    LLM-judge kinds (general_question, guardrail, dashboard_summary,
    knowledge_question) are excluded when the [llm-judge] extra (openai) is
    not installed — those items are skipped rather than erroring out mid-run.
    """
    kinds = set(_EAGER_EVALUATORS)
    if _openai_available():
        kinds |= set(_LAZY_EVALUATOR_MODULES)
    return kinds
