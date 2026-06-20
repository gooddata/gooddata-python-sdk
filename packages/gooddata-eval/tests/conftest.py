# (C) 2026 GoodData Corporation
import json
import re
from pathlib import Path

import pytest

from gooddata_eval.core.models import ChatResult, DatasetItem

# Maps the human-readable trigger in dataset fixtures to the alert API value,
# mirroring AlertSkillEvaluator._TRIGGER_MAP.
_TRIGGER_MAP = {"Every time": "ALWAYS", "One time": "ONCE"}


@pytest.fixture
def fixtures_dir() -> Path:
    return Path(__file__).parent / "fixtures"


def _extract_metric_id(metric_str: str) -> str | None:
    match = re.search(r"\(([^)]+)\)\s*$", metric_str)
    return match.group(1) if match else None


def passing_chat_result_for(item: DatasetItem) -> ChatResult:
    """Synthesize a ChatResult that should make ``item`` pass its evaluator.

    Derives the response from the item's own ``expected_output`` so the
    deterministic evaluators (visualization, metric_skill, alert_skill,
    search_tool) score a pass. The LLM-judge kinds (general_question,
    guardrail, dashboard_summary) return plain text — the test must patch the
    judge to control their verdict.
    """
    kind = item.test_kind
    expected = item.expected_output

    if kind == "visualization":
        viz = expected["visualization"]
        return ChatResult.model_validate({"createdVisualizations": {"objects": [viz], "reasoning": ""}})

    if kind == "metric_skill":
        return ChatResult.model_validate(
            {
                "toolCallEvents": [
                    {
                        "functionName": "create_metric",
                        "functionArguments": "{}",
                        "result": json.dumps({"data": {"maql": expected["maql"], "format": expected["format"]}}),
                    }
                ]
            }
        )

    if kind == "alert_skill":
        args = {
            "operator": expected["Operator"],
            "threshold": expected["Threshold"],
            "trigger": _TRIGGER_MAP.get(expected["Trigger"], expected["Trigger"]),
            "metric": _extract_metric_id(expected["Metric"]),
            "recipients": [r.strip() for r in expected["Recipient(s)"].split(",") if r.strip()],
        }
        return ChatResult.model_validate(
            {"toolCallEvents": [{"functionName": "create_metric_alert", "functionArguments": json.dumps(args)}]}
        )

    if kind == "search_tool":
        call = expected["tool_call"]
        return ChatResult.model_validate(
            {
                "toolCallEvents": [
                    {
                        "functionName": call["function_name"],
                        "functionArguments": json.dumps(call["function_arguments"]),
                    }
                ]
            }
        )

    # general_question / guardrail / dashboard_summary: free text scored by the
    # LLM judge. Return a benign refusal/answer; tests patch the judge.
    return ChatResult.model_validate({"textResponse": "A coherent text answer."})


class PassingBackend:
    """ChatBackend that returns a passing ChatResult per item, tracking calls."""

    def __init__(self):
        self.calls: list[str] = []

    def ask(self, item: DatasetItem) -> ChatResult:
        self.calls.append(item.id)
        return passing_chat_result_for(item)


@pytest.fixture
def passing_backend() -> PassingBackend:
    return PassingBackend()
