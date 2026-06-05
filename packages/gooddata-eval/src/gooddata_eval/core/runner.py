# (C) 2026 GoodData Corporation
"""Dataset run orchestration: per item, K single-turn runs, route by test_kind, aggregate pass@K."""

import time
import traceback
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass, field
from functools import partial
from typing import Callable, Protocol

from gooddata_eval.core.evaluators import get_evaluator, supported_test_kinds
from gooddata_eval.core.evaluators.base import ItemEvaluation
from gooddata_eval.core.models import ChatResult, DatasetItem


class ChatBackend(Protocol):
    def ask(self, question: str) -> ChatResult: ...


@dataclass
class ItemReport:
    id: str
    dataset_name: str
    test_kind: str
    question: str
    pass_at_k: bool = False
    skipped: bool = False
    error: str | None = None
    runs: int = 0
    latency_s: float = 0.0  # total wall-clock across this item's runs
    best_detail: dict = field(default_factory=dict)

    @property
    def avg_latency_s(self) -> float:
        return self.latency_s / self.runs if self.runs else 0.0

    @property
    def quality_score(self) -> float:
        """Fraction of bool-valued strict checks in best_detail that are True.

        Falls back to 1.0 if pass_at_k else 0.0 when no bool checks exist
        (e.g. text evaluators where best_detail has no bool flags).
        """
        checks = {k: v for k, v in self.best_detail.items() if isinstance(v, bool)}
        if checks:
            return sum(1 for v in checks.values() if v) / len(checks)
        return 1.0 if self.pass_at_k else 0.0


@dataclass
class EvalReport:
    model: str | None
    provider_name: str = ""
    provider_type: str = ""
    workspace_id: str = ""
    items: list[ItemReport] = field(default_factory=list)
    wall_clock_s: float = 0.0  # actual elapsed time; differs from latency_s under concurrency

    @property
    def total(self) -> int:
        return len(self.items)

    @property
    def passed(self) -> int:
        return sum(1 for i in self.items if i.pass_at_k)

    @property
    def skipped(self) -> int:
        return sum(1 for i in self.items if i.skipped)

    @property
    def errored(self) -> int:
        return sum(1 for i in self.items if i.error is not None)

    @property
    def latency_s(self) -> float:
        return sum(i.latency_s for i in self.items)

    @property
    def total_runs(self) -> int:
        return sum(i.runs for i in self.items)

    @property
    def avg_latency_s(self) -> float:
        total_runs = self.total_runs
        return self.latency_s / total_runs if total_runs else 0.0

    @property
    def avg_quality_score(self) -> float:
        """Mean quality_score across evaluated (non-skipped, non-errored) items."""
        evaluated = [i.quality_score for i in self.items if not i.skipped and i.error is None]
        return sum(evaluated) / len(evaluated) if evaluated else 0.0


# A per-run progress callback: (run_index, runs_total, passed, latency_s) -> None
RunCallback = Callable[[int, int, bool, float], None]


def _run_one_item(
    item: DatasetItem, backend: ChatBackend, runs: int, on_run_done: RunCallback | None = None
) -> ItemReport:
    report = ItemReport(id=item.id, dataset_name=item.dataset_name, test_kind=item.test_kind, question=item.question)
    if item.test_kind not in supported_test_kinds():
        report.skipped = True
        return report

    evaluator = get_evaluator(item.test_kind)
    best: ItemEvaluation | None = None
    try:
        for run_index in range(1, runs + 1):
            t0 = time.perf_counter()
            chat_result = backend.ask(item.question)
            evaluation = evaluator.evaluate(item, chat_result)
            latency = time.perf_counter() - t0
            report.runs += 1
            report.latency_s += latency
            if best is None or evaluation.rank_key > best.rank_key:
                best = evaluation
            if evaluation.passed:
                report.pass_at_k = True
            if on_run_done is not None:
                on_run_done(run_index, runs, evaluation.passed, latency)
    except Exception as e:  # agent/network/parse failure for this item
        report.error = f"{type(e).__name__}: {e}"
        if best is not None:
            report.best_detail = best.detail
        return report

    if best is not None:
        report.best_detail = best.detail
    return report


def _forward_run_event(
    user_cb: "Callable[[int, int, int, int, bool, float], None]",
    item_index: int,
    total: int,
    run_index: int,
    runs_total: int,
    passed: bool,
    latency: float,
) -> None:
    user_cb(item_index, total, run_index, runs_total, passed, latency)


def run_items(
    items: list[DatasetItem],
    backend: ChatBackend,
    *,
    runs: int = 2,
    model: str | None = None,
    provider_name: str = "",
    provider_type: str = "",
    workspace_id: str = "",
    on_item_start: Callable[[int, int, DatasetItem], None] | None = None,
    on_run_done: Callable[[int, int, int, int, bool, float], None] | None = None,
    on_item_done: Callable[[int, int, ItemReport], None] | None = None,
    on_langfuse_item_done: Callable[[int, int, ItemReport], None] | None = None,
    concurrency: int = 1,
) -> EvalReport:
    """Run every item K times, routing by test_kind, and aggregate pass@K.

    Optional callbacks stream progress without coupling core to any I/O library
    (index/run_index are 1-based):
      - on_item_start(index, total, item)                          before an item's runs begin
      - on_run_done(index, total, run_index, runs, passed, latency) after each individual run
      - on_item_done(index, total, report)                         after an item is fully evaluated
      - on_langfuse_item_done(index, total, report)                after non-skipped, non-errored items only

    concurrency > 1 dispatches items to a ThreadPoolExecutor so multiple
    questions are sent to the agent simultaneously. Each item still runs
    --runs times sequentially (pass@K). Results are collected in input order.
    """
    concurrency = max(1, concurrency)
    report = EvalReport(
        model=model, provider_name=provider_name, provider_type=provider_type, workspace_id=workspace_id
    )
    total = len(items)

    def _process_item(index: int, item: DatasetItem) -> ItemReport:
        try:
            if on_item_start is not None:
                on_item_start(index, total, item)
        except Exception:  # non-fatal — callback must not abort a parallel run
            traceback.print_exc()
        run_cb = partial(_forward_run_event, on_run_done, index, total) if on_run_done is not None else None
        item_report = _run_one_item(item, backend, runs, on_run_done=run_cb)
        try:
            if on_item_done is not None:
                on_item_done(index, total, item_report)
            if on_langfuse_item_done is not None and not item_report.skipped and item_report.error is None:
                on_langfuse_item_done(index, total, item_report)
        except Exception:  # non-fatal — log but don't abort
            traceback.print_exc()
        return item_report

    _t0 = time.perf_counter()
    if concurrency <= 1:
        for index, item in enumerate(items, start=1):
            report.items.append(_process_item(index, item))
    else:
        # Dispatch concurrently; collect in original order.
        with ThreadPoolExecutor(max_workers=concurrency) as pool:
            futures = {pool.submit(_process_item, index, item): index for index, item in enumerate(items, start=1)}
            results: dict[int, ItemReport] = {}
            for future in as_completed(futures):
                idx = futures[future]
                results[idx] = future.result()
        for index in range(1, total + 1):
            report.items.append(results[index])
    report.wall_clock_s = time.perf_counter() - _t0
    return report
