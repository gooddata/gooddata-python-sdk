# (C) 2026 GoodData Corporation. All rights reserved.
"""Agentic evaluation runner for gd-eval CLI — handles multi-turn agentic test kinds."""

from __future__ import annotations

import time
from typing import Any, TypedDict

from gooddata_eval.core.agentic._langfuse import HttpxLangfuseClient, make_langfuse_client
from gooddata_eval.core.agentic.alert_skill import evaluate_agentic_alert_skill
from gooddata_eval.core.agentic.conversation import ConversationFixture, evaluate_agentic_conversation
from gooddata_eval.core.agentic.general_question import evaluate_agentic_general_question
from gooddata_eval.core.agentic.guardrail import evaluate_agentic_guardrail
from gooddata_eval.core.agentic.metric_skill import evaluate_agentic_metric_skill
from gooddata_eval.core.agentic.search_tool import evaluate_agentic_search_tool
from gooddata_eval.core.agentic.visualization import evaluate_agentic_visualization
from gooddata_eval.core.models import CreatedVisualization, DatasetItem
from gooddata_eval.core.runner import EvalReport, ItemReport

_LfKw = TypedDict(
    "_LfKw",
    {
        "langfuse": Any,
        "dataset_item_id": str,
        "dataset_name": str,
        "run_timestamp": str,
        "model_version_override": str | None,
    },
    total=False,
)

AGENTIC_TEST_KINDS = frozenset(
    {
        "vis_agentic",  # production: expected_output.visualization (single/multi CreatedVisualization)
        "agentic_visualization",  # experimental: expected_output.expected_outputs (multi-candidate)
        "agentic_metric_skill",
        "agentic_alert_skill",
        "agentic_search",
        "agentic_general_question",
        "agentic_guardrail",
        "agentic_conversation",
    }
)


def _parse_visualization_expected(expected_output: Any) -> list[CreatedVisualization]:
    """Parse expected_output into a list of CreatedVisualization candidates.

    Accepts:
      {"expected_outputs": [{"visualization": {...}}, ...]}  <- agentic fixture format
      {"visualization": {...}} or {"visualization": [{...}]}  <- single/multi candidate
      [{"visualization": {...}}, ...]                          <- bare list
    """
    if isinstance(expected_output, dict):
        raw_list = expected_output.get("expected_outputs")
        if raw_list is not None:
            return [
                CreatedVisualization.model_validate(v.get("visualization", v) if isinstance(v, dict) else v)
                for v in raw_list
            ]
        raw_viz = expected_output.get("visualization")
        if raw_viz is not None:
            if isinstance(raw_viz, list):
                return [CreatedVisualization.model_validate(v) for v in raw_viz]
            return [CreatedVisualization.model_validate(raw_viz)]
    if isinstance(expected_output, list):
        return [
            CreatedVisualization.model_validate(v.get("visualization", v) if isinstance(v, dict) else v)
            for v in expected_output
        ]
    raise ValueError(
        f"Cannot parse agentic_visualization expected_output: {type(expected_output).__name__}. "
        'Expected {"expected_outputs": [...]} or {"visualization": {...}}.'
    )


def _dispatch_agentic(
    item: DatasetItem,
    host: str,
    token: str,
    workspace_id: str,
    k: int,
    langfuse: Any,
    run_ts: str,
    model_version_override: str | None,
) -> None:
    """Call the appropriate evaluate_agentic_* function for the item's test_kind."""
    kind = item.test_kind
    eo = item.expected_output
    lf_kw: _LfKw = {
        "langfuse": langfuse,
        "dataset_item_id": item.id,
        "dataset_name": item.dataset_name,
        "run_timestamp": run_ts,
        "model_version_override": model_version_override,
    }

    if kind in ("vis_agentic", "agentic_visualization"):
        evaluate_agentic_visualization(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_outputs=_parse_visualization_expected(eo),
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_metric_skill":
        evaluate_agentic_metric_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, (dict, list)) else {},
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_alert_skill":
        evaluate_agentic_alert_skill(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, dict) else {},
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_search":
        eo_dict = eo if isinstance(eo, dict) else {}
        tool_call = eo_dict.get("tool_call", {})
        expected_args = tool_call.get("function_arguments", eo_dict)
        evaluate_agentic_search_tool(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_tool_call=expected_args,
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_general_question":
        evaluate_agentic_general_question(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, str) else str(eo),
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_guardrail":
        evaluate_agentic_guardrail(
            host=host,
            token=token,
            workspace_id=workspace_id,
            question=item.question,
            expected_output=eo if isinstance(eo, str) else str(eo),
            k=k,
            **lf_kw,
        )
    elif kind == "agentic_conversation":
        fixture_data = eo.get("fixture") or eo if isinstance(eo, dict) else {}
        evaluate_agentic_conversation(
            host=host,
            token=token,
            workspace_id=workspace_id,
            fixture=ConversationFixture.model_validate(fixture_data),
            **lf_kw,
        )
    else:
        raise ValueError(f"Unknown agentic test kind: {kind!r}")


def run_agentic_items(
    items: list[DatasetItem],
    host: str,
    token: str,
    workspace_id: str,
    *,
    k: int = 2,
    model_version: str | None = None,
    use_langfuse: bool = False,
    run_ts: str,
    on_item_start: Any = None,
    on_item_done: Any = None,
) -> EvalReport:
    """Run agentic items through evaluate_agentic_* and return an EvalReport."""
    langfuse = make_langfuse_client() if use_langfuse else None

    report = EvalReport(model=model_version)
    total = len(items)

    for index, item in enumerate(items, start=1):
        if on_item_start is not None:
            try:
                on_item_start(index, total, item)
            except Exception:
                pass

        item_report = ItemReport(
            id=item.id,
            dataset_name=item.dataset_name,
            test_kind=item.test_kind,
            question=item.question,
        )
        t0 = time.perf_counter()
        try:
            _dispatch_agentic(item, host, token, workspace_id, k, langfuse, run_ts, model_version)
            item_report.pass_at_k = True
            item_report.runs = k
        except AssertionError as exc:
            item_report.pass_at_k = False
            item_report.runs = k
            print(f"[agentic] {item.id} FAIL: {exc}", flush=True)
        except Exception as exc:
            item_report.error = f"{type(exc).__name__}: {exc}"
            item_report.runs = 0
        finally:
            item_report.latency_s = time.perf_counter() - t0

        if on_item_done is not None:
            try:
                on_item_done(index, total, item_report)
            except Exception:
                pass

        report.items.append(item_report)

    if langfuse is not None:
        try:
            langfuse.flush()
            langfuse.close()
        except Exception:
            pass

    return report
