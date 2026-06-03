# (C) 2026 GoodData Corporation
"""Generic evaluator contract shared by all test kinds."""

from dataclasses import dataclass, field
from typing import Any, Protocol, runtime_checkable

from gooddata_eval.core.models import ChatResult, DatasetItem


@dataclass
class ItemEvaluation:
    """Category-agnostic result of evaluating one agent run for one dataset item."""

    passed: bool
    rank_key: tuple[Any, ...]  # higher is better; used to pick the best run
    detail: dict[str, Any] = field(default_factory=dict)  # structured, for reports
    error: str | None = None  # set when the run could not be evaluated


@runtime_checkable
class Evaluator(Protocol):
    test_kind: str

    def evaluate(self, item: DatasetItem, chat_result: ChatResult) -> ItemEvaluation: ...
