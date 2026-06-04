# (C) 2026 GoodData Corporation
"""`gd-eval` command-line entry point."""

import argparse
import sys
from datetime import datetime, timezone
from pathlib import Path

import httpx
from gooddata_api_client.exceptions import ApiException
from rich.console import Console

from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import RunConfig
from gooddata_eval.core.connection import ConnectionError_, resolve_connection
from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.langfuse.sink import LangfuseSink
from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.reporting.console import render_console
from gooddata_eval.core.reporting.json_report import write_json_report
from gooddata_eval.core.runner import ItemReport, run_items
from gooddata_eval.core.summary.http_client import SummaryClient
from gooddata_eval.core.workspace import ModelResolutionError, WorkspaceModelController

_EXIT_OK = 0
_EXIT_OPERATIONAL_ERROR = 2
_SUMMARY_TEST_KIND = "dashboard_summary"


class _RoutingBackend:
    """Dispatch each item to the right backend by test_kind.

    `dashboard_summary` items go to the dedicated summary endpoint; everything
    else uses the conversational chat endpoint.
    """

    def __init__(self, chat: ChatClient, summary: SummaryClient):
        self._chat = chat
        self._summary = summary

    def ask(self, item: DatasetItem) -> ChatResult:
        if item.test_kind == _SUMMARY_TEST_KIND:
            return self._summary.ask(item)
        return self._chat.ask(item)

    def close(self) -> None:
        for backend in (self._chat, self._summary):
            if hasattr(backend, "close"):
                backend.close()


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="gd-eval", description="Evaluate the GoodData AI agent.")
    sub = parser.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run an evaluation dataset.")
    run.add_argument("--host", help="GoodData host URL.")
    run.add_argument("--token", help="API token (or set GOODDATA_TOKEN).")
    run.add_argument("--profile", help="Profile name in ~/.gooddata/profiles.yaml.")
    run.add_argument("--workspace", required=True, help="Workspace id.")
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--dataset", help="Path to a folder of dataset JSON files.")
    source.add_argument("--langfuse-dataset", dest="langfuse_dataset", help="Langfuse dataset name.")
    run.add_argument("--model", help="Model id (default: workspace's current active model).")
    run.add_argument(
        "--provider",
        help="LLM provider name or id (default: the workspace's active provider; "
        "auto-selected when --model is offered by exactly one provider).",
    )
    run.add_argument("--runs", type=int, default=2, help="Independent runs per item (pass@K). Default 2.")
    run.add_argument("--json", dest="json_path", help="Write a JSON report to this path.")
    run.add_argument("--quiet", action="store_true", help="Suppress per-item progress output.")
    run.add_argument(
        "--langfuse",
        action="store_true",
        help="Log scores and traces to Langfuse (requires --langfuse-dataset and LANGFUSE_* env vars).",
    )
    return parser


def parse_args(argv: list[str]) -> argparse.Namespace:
    return _build_parser().parse_args(argv)


def _truncate(text: str, limit: int = 80) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _make_progress_callbacks(console: Console):
    """Build (on_item_start, on_run_done, on_item_done) callbacks that stream progress."""

    def on_item_start(index: int, total: int, item: DatasetItem) -> None:
        console.print(f"[dim]\\[{index}/{total}][/dim] [cyan]{item.id}[/cyan] {_truncate(item.question)}")

    def on_run_done(index: int, total: int, run_index: int, runs: int, passed: bool, latency: float) -> None:
        tag = "[green]pass[/green]" if passed else "[red]fail[/red]"
        console.print(f"[dim]\\[{index}/{total}][/dim]     run {run_index}/{runs}  {tag}  [dim]{latency:.2f}s[/dim]")

    def on_item_done(index: int, total: int, report: ItemReport) -> None:
        if report.skipped:
            tag = "[yellow]SKIP[/yellow]"
        elif report.error:
            tag = "[red]ERR [/red]"
        elif report.pass_at_k:
            tag = "[green]PASS[/green]"
        else:
            tag = "[red]FAIL[/red]"
        if report.skipped:
            suffix = ""
        else:
            quality_str = f"{report.quality_score:.0%}"
            suffix = (
                f" [dim]({report.latency_s:.2f}s total, {report.avg_latency_s:.2f}s avg, "
                f"quality={quality_str}, {report.runs} run(s))[/dim]"
            )
        console.print(f"[dim]\\[{index}/{total}][/dim]   -> {tag} [cyan]{report.id}[/cyan]{suffix}")

    return on_item_start, on_run_done, on_item_done


def _load_dataset(config: RunConfig):
    if config.dataset_folder is not None:
        return load_local_dataset(config.dataset_folder)
    from gooddata_eval.core.dataset.langfuse_source import load_langfuse_dataset  # noqa: PLC0415

    if config.langfuse_dataset is None:  # pragma: no cover - argparse mutually-exclusive group guarantees one is set
        raise ValueError("Either --dataset or --langfuse-dataset is required.")
    return load_langfuse_dataset(config.langfuse_dataset)


def _run(config: RunConfig) -> int:
    # Enforce: --langfuse only valid with --langfuse-dataset
    if config.log_to_langfuse and config.langfuse_dataset is None:
        print(
            "error: --langfuse requires --langfuse-dataset (local datasets have no Langfuse item ids to link to).",
            file=sys.stderr,
        )
        return _EXIT_OPERATIONAL_ERROR

    items = _load_dataset(config)

    controller = WorkspaceModelController(config.host, config.token, config.workspace_id)
    resolved = controller.resolve_and_activate(config.model, config.provider_id)

    run_name = f"gd-eval-{datetime.now(timezone.utc).strftime('%Y-%m-%d-%H-%M')}-{resolved.model_id}"

    on_item_start = None
    on_run_done = None
    on_item_done = None
    if not config.quiet:
        progress_console = Console(stderr=True)
        switched = " [switched active provider]" if resolved.switched else ""
        provider_display = resolved.provider_name or resolved.provider_id
        progress_console.print(
            f"Evaluating {len(items)} item(s) on workspace '{config.workspace_id}' "
            f"(provider={provider_display}, model={resolved.model_id}){switched}..."
        )
        if config.log_to_langfuse:
            progress_console.print(f"Logging to Langfuse dataset run '{run_name}'...")
        on_item_start, on_run_done, on_item_done = _make_progress_callbacks(progress_console)

    on_langfuse_item_done = None
    if config.log_to_langfuse:
        assert config.langfuse_dataset is not None  # guarded above
        sink = LangfuseSink(dataset_name=config.langfuse_dataset, run_name=run_name)

        def on_langfuse_item_done(index: int, total: int, report: ItemReport) -> None:
            sink.log_item(report, dataset_item_id=report.id)

    backend = _RoutingBackend(
        ChatClient(host=config.host, token=config.token, workspace_id=config.workspace_id),
        SummaryClient(host=config.host, token=config.token, workspace_id=config.workspace_id),
    )
    try:
        report = run_items(
            items,
            backend,
            runs=config.runs,
            model=resolved.model_id,
            workspace_id=config.workspace_id,
            on_item_start=on_item_start,
            on_run_done=on_run_done,
            on_item_done=on_item_done,
            on_langfuse_item_done=on_langfuse_item_done,
        )
    finally:
        if hasattr(backend, "close"):
            backend.close()

    skipped_kinds = sorted({i.test_kind for i in report.items if i.skipped})
    if skipped_kinds:
        print(
            f"warning: skipped {sum(i.skipped for i in report.items)} item(s) with "
            f"unsupported test_kind(s): {', '.join(skipped_kinds)}",
            file=sys.stderr,
        )

    render_console(report)
    if config.json_path is not None:
        write_json_report(report, config.json_path)
    return _EXIT_OK


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    try:
        host, token = resolve_connection(host=args.host, token=args.token, profile=args.profile)
        config = RunConfig(
            host=host,
            token=token,
            workspace_id=args.workspace,
            dataset_folder=Path(args.dataset) if args.dataset else None,
            langfuse_dataset=args.langfuse_dataset,
            model=args.model,
            provider_id=args.provider,
            runs=args.runs,
            json_path=Path(args.json_path) if args.json_path else None,
            log_to_langfuse=args.langfuse,
            quiet=args.quiet,
        )
        return _run(config)
    except (
        ConnectionError_,
        ModelResolutionError,
        FileNotFoundError,
        ValueError,
        httpx.HTTPError,
        ApiException,
        RuntimeError,
    ) as e:
        print(f"error: {e}", file=sys.stderr)
        return _EXIT_OPERATIONAL_ERROR


if __name__ == "__main__":
    raise SystemExit(main())
