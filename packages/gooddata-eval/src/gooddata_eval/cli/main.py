# (C) 2026 GoodData Corporation
"""`gd-eval` command-line entry point."""

import argparse
import os
import sys
import threading
from datetime import datetime, timezone
from pathlib import Path
from typing import get_args

import httpx
from gooddata_api_client.exceptions import ApiException
from rich.console import Console
from rich.table import Table

from gooddata_eval.cli.agentic_runner import AGENTIC_TEST_KINDS, run_agentic_items
from gooddata_eval.core.chat.sse_client import ChatClient
from gooddata_eval.core.config import DEFAULT_JUDGE_MODEL, JUDGE_MODEL_ENV_VAR, ReasoningEffort, RunConfig
from gooddata_eval.core.connection import ConnectionError_, resolve_connection
from gooddata_eval.core.dataset.local import load_local_dataset
from gooddata_eval.core.langfuse.sink import LangfuseSink
from gooddata_eval.core.models import ChatResult, DatasetItem
from gooddata_eval.core.reporting.console import render_comparison, render_console
from gooddata_eval.core.reporting.json_report import write_multi_model_report
from gooddata_eval.core.runner import ItemReport, run_items
from gooddata_eval.core.summary.http_client import SummaryClient
from gooddata_eval.core.timing import TIMERS_ENV_VAR
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
    run.add_argument(
        "--kind",
        dest="kind",
        default="visualization",
        metavar="TEST_KIND",
        help=(
            "Default test kind for dataset items that don't embed one. "
            "Use 'vis_agentic', 'agentic_visualization', 'agentic_metric_skill', etc. for multi-turn agentic eval. "
            "(default: visualization)"
        ),
    )
    run.add_argument(
        "--model",
        action="append",
        dest="models",
        metavar="MODEL",
        help=(
            "Model id to evaluate (e.g. --model gpt-5.2). "
            "Prefix with provider name or id to disambiguate: "
            "--model ProviderName/gpt-5.2 or --model provider_id/gpt-5.2. "
            "Repeat to compare multiple models. "
            "Default: workspace's current active model."
        ),
    )
    run.add_argument("--runs", type=int, default=2, help="Independent runs per item (pass@K). Default 2.")
    run.add_argument(
        "--concurrency",
        type=int,
        default=1,
        help="Number of items evaluated concurrently (default 1 = sequential). "
        "Increase to load-test the agent under simultaneous requests. Agentic kinds that "
        "create workspace objects (metric_skill, alert_skill, conversation, kda_skill) always "
        "run one at a time regardless, to avoid cross-test contamination.",
    )
    run.add_argument(
        "--judge-model",
        dest="judge_model",
        metavar="MODEL",
        help=f"OpenAI model for LLM-as-judge scoring (default: {DEFAULT_JUDGE_MODEL}). "
        "Also settable via GD_EVAL_JUDGE_MODEL. Two things to weigh before changing it: a "
        "model that rejects temperature=0 (the gpt-5 family does) makes verdicts "
        "non-deterministic, and picking the same model the agent runs means the judge "
        "grades its own family's output.",
    )
    run.add_argument(
        "--timers",
        action="store_true",
        help="Print per-turn [timer] diagnostics (agent response, judge, simulated user). "
        "Off by default because a large run emits hundreds of lines; the same measurements "
        "are always in the JSON report's latency_breakdown_s. Equivalent to GD_EVAL_TIMERS=1.",
    )
    run.add_argument("--json", dest="json_path", help="Write a JSON report to this path.")
    run.add_argument("--quiet", action="store_true", help="Suppress per-item progress output.")
    run.add_argument(
        "--preserve-failed",
        action="store_true",
        dest="preserve_failed",
        help="Keep failed conversations on the server for post-mortem inspection.",
    )
    run.add_argument(
        "--reasoning-effort",
        dest="reasoning_effort",
        choices=list(get_args(ReasoningEffort)),
        help="Reasoning effort requested per message. Requires the enableGenAiReasoningEffort "
        "feature flag on the target organization; without it the server ignores the value.",
    )
    run.add_argument(
        "--langfuse",
        action="store_true",
        help="Log scores and traces to Langfuse (requires --langfuse-dataset and LANGFUSE_* env vars).",
    )
    run.add_argument(
        "--agent-id",
        dest="agent_id",
        help=(
            "AI Hub agent id every conversation should target (or set GD_EVAL_AGENT_ID). "
            "GoodData has no admin-settable default agent -- without this, each conversation "
            "falls back to whichever agent the platform's last-used/last-edited heuristic "
            "resolves, which may not have every skill under test enabled."
        ),
    )
    models_cmd = sub.add_parser("models", help="List LLM providers and models configured in the org.")
    models_cmd.add_argument("--host", help="GoodData host URL.")
    models_cmd.add_argument("--token", help="API token (or set GOODDATA_TOKEN).")
    models_cmd.add_argument("--profile", help="Profile name in ~/.gooddata/profiles.yaml.")
    models_cmd.add_argument(
        "--workspace",
        help="Workspace id. When provided, marks the currently active model.",
    )
    return parser


def parse_args(argv: list[str]) -> argparse.Namespace:
    return _build_parser().parse_args(argv)


def _apply_judge_model(model: str | None) -> None:
    """Publish --judge-model for the deep LLMJudge call sites; an explicit flag wins."""
    if model:
        os.environ[JUDGE_MODEL_ENV_VAR] = model


def _apply_timer_flag(enabled: bool) -> None:
    """Publish --timers for the deep [timer] call sites.

    An env var rather than a parameter because the emitters sit four layers down, and it is
    how this package already gates cross-cutting behaviour (see TAVERN_E2E_SKIP_TRACE_LINK).
    Only ever sets it -- never clears a value the caller exported themselves.
    """
    if enabled:
        os.environ[TIMERS_ENV_VAR] = "1"


def _warn_if_local_dataset_cannot_link(config: RunConfig, agentic_items: list) -> None:
    """Say up front that dataset-run assembly will fail, rather than after the run.

    --langfuse is refused outright with a local dataset because local item ids cannot be
    linked. But every evaluate_agentic_* falls back to try_make_langfuse_client() when the
    caller passes none, so with LANGFUSE_* exported the linking runs anyway and each
    conversation earns a 404 from dataset-run-items -- arriving in a block at the very end
    of the run, long after the flag that would have prevented it could be changed. The
    fallback is deliberate (direct library and tavern callers rely on it), so this warns
    instead of disabling it.
    """
    from gooddata_eval.core.agentic._langfuse import SKIP_ENV_VAR, langfuse_credentials_present  # noqa: PLC0415
    from gooddata_eval.core.config import env_flag  # noqa: PLC0415

    if not agentic_items or config.dataset_folder is None:
        return
    if not langfuse_credentials_present() or env_flag(SKIP_ENV_VAR):
        return
    print(
        f"warning: --dataset is a local folder, so its item ids are not Langfuse dataset item ids. "
        f"Traces will be found and scored, but the per-run grouping that makes models comparable "
        f"cannot be created and each conversation will report a 404 from dataset-run-items. "
        f"Use --langfuse-dataset for comparable runs, or set {SKIP_ENV_VAR}=1 to skip trace linking.",
        file=sys.stderr,
    )


def _truncate(text: str, limit: int = 80) -> str:
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _parse_model_arg(val: str) -> tuple[str | None, str]:
    """Parse a model argument that may include a provider prefix.

    Accepts two forms:
      "gpt-5.2"                   → (None, "gpt-5.2")
      "ProviderName/gpt-5.2"      → ("ProviderName", "gpt-5.2")
      "provider_id.../model_id"   → ("provider_id...", "model_id")

    The provider part (if present) is passed to resolve_and_activate and
    accepted as either a provider name or provider id.
    """
    if "/" in val:
        provider_ref, _, model_id = val.partition("/")
        return provider_ref.strip() or None, model_id.strip()
    return None, val


def _make_progress_callbacks(console: Console):
    """Build (on_item_start, on_run_done, on_item_done) callbacks that stream progress.

    A threading lock guards all console.print() calls so that concurrent
    ``--concurrency 2+`` workers do not deadlock when stdout is piped
    (e.g. running in a background process).
    """
    _print_lock = threading.Lock()

    def on_item_start(index: int, total: int, item: DatasetItem) -> None:
        with _print_lock:
            console.print(f"[dim]\\[{index}/{total}][/dim] [cyan]{item.id}[/cyan] {_truncate(item.question)}")

    def on_run_done(index: int, total: int, run_index: int, runs: int, passed: bool, latency: float) -> None:
        tag = "[green]pass[/green]" if passed else "[red]fail[/red]"
        with _print_lock:
            console.print(
                f"[dim]\\[{index}/{total}][/dim]     run {run_index}/{runs}  {tag}  [dim]{latency:.2f}s[/dim]"
            )

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
        with _print_lock:
            console.print(f"[dim]\\[{index}/{total}][/dim]   -> {tag} [cyan]{report.id}[/cyan]{suffix}")

    return on_item_start, on_run_done, on_item_done


def _load_dataset(config: RunConfig):
    if config.dataset_folder is not None:
        return load_local_dataset(config.dataset_folder)
    from gooddata_eval.core.dataset.langfuse_source import load_langfuse_dataset  # noqa: PLC0415

    if config.langfuse_dataset is None:  # pragma: no cover - argparse mutually-exclusive group guarantees one is set
        raise ValueError("Either --dataset or --langfuse-dataset is required.")
    return load_langfuse_dataset(config.langfuse_dataset, default_test_kind=config.kind)


def _list_models(host: str, token: str, workspace_id: str | None) -> int:
    """List all LLM providers and their models; mark the active one if --workspace given."""
    from gooddata_eval.core.workspace import WorkspaceModelController  # noqa: PLC0415

    controller = WorkspaceModelController(host, token, workspace_id or "")
    info = controller._provider_info()  # {provider_id: {name, models: [{id, family}]}}

    active_provider_id: str | None = None
    active_model_id: str | None = None
    if workspace_id:
        active = controller.get_active()
        if active:
            active_provider_id = active.provider_id
            active_model_id = active.default_model_id

    console = Console()

    if not info:
        console.print("[yellow]No LLM providers configured in this organisation.[/yellow]")
        return _EXIT_OK

    table = Table(title=f"LLM Providers and Models{f' (workspace: {workspace_id})' if workspace_id else ''}")
    table.add_column("Provider")
    table.add_column("Provider ID")
    table.add_column("Model ID")
    table.add_column("Family")
    table.add_column("Active")

    for provider_id, pinfo in sorted(info.items(), key=lambda kv: kv[1].get("name") or kv[0]):
        name = pinfo.get("name") or provider_id
        models = pinfo.get("models") or []
        if not models:
            is_active_provider = provider_id == active_provider_id
            table.add_row(name, provider_id, "[dim](none listed)[/dim]", "", "◀" if is_active_provider else "")
        for i, model in enumerate(models):
            model_id = model.get("id", "?") if isinstance(model, dict) else str(model)
            family = model.get("family", "") if isinstance(model, dict) else ""
            is_active = provider_id == active_provider_id and model_id == active_model_id
            active_marker = "[green]◀ active[/green]" if is_active else ""
            table.add_row(
                name if i == 0 else "",
                provider_id if i == 0 else "",
                model_id,
                family,
                active_marker,
            )

    console.print(table)
    return _EXIT_OK


def _run(config: RunConfig) -> int:
    if config.log_to_langfuse and config.langfuse_dataset is None:
        print(
            "error: --langfuse requires --langfuse-dataset (local datasets have no Langfuse item ids to link to).",
            file=sys.stderr,
        )
        return _EXIT_OPERATIONAL_ERROR

    items = _load_dataset(config)
    agentic_items = [i for i in items if i.test_kind in AGENTIC_TEST_KINDS]
    non_agentic_items = [i for i in items if i.test_kind not in AGENTIC_TEST_KINDS]
    _warn_if_local_dataset_cannot_link(config, agentic_items)
    models = config.models or []
    run_ts = datetime.now(timezone.utc).strftime("%Y-%m-%d-%H-%M")
    n_models = len(models) if models else 1

    controller = WorkspaceModelController(config.host, config.token, config.workspace_id)
    original_active = controller.get_active()

    progress_console = Console(stderr=True) if not config.quiet else None
    if progress_console:
        multi_suffix = f" — {n_models} model(s)" if n_models > 1 else ""
        progress_console.print(f"Evaluating {len(items)} item(s) on workspace '{config.workspace_id}'{multi_suffix}")

    reports: list = []
    try:
        for k, model_id in enumerate(models or [None], start=1):
            provider_ref, bare_model_id = _parse_model_arg(model_id or "")
            effective_provider = provider_ref
            try:
                resolved = controller.resolve_and_activate(bare_model_id or None, effective_provider)
            except (ModelResolutionError, httpx.HTTPError, ApiException, RuntimeError) as exc:
                print(f"warning: skipping model '{model_id}': {exc}", file=sys.stderr)
                continue

            if progress_console:
                if n_models > 1:
                    progress_console.print(f"\n── Model {k}/{n_models}: {resolved.model_id} " + "─" * 40)
                else:
                    switched = " [switched active provider]" if resolved.switched else ""
                    provider_display = resolved.provider_name or resolved.provider_id
                    progress_console.print(f"Provider={provider_display}, model={resolved.model_id}{switched}")

            run_name = f"gd-eval-{run_ts}-{resolved.model_id}"
            if config.reasoning_effort:
                # Without this two runs differing only by effort share a name and are
                # indistinguishable in the report, which is the comparison this exists for.
                run_name = f"{run_name}-effort-{config.reasoning_effort.lower()}"
            if progress_console and config.log_to_langfuse:
                progress_console.print(f"Logging to Langfuse run '{run_name}'...")

            on_item_start, on_run_done, on_item_done = (None, None, None)
            if progress_console:
                on_item_start, on_run_done, on_item_done = _make_progress_callbacks(progress_console)

            on_langfuse_item_done = None
            if config.log_to_langfuse:
                assert config.langfuse_dataset is not None
                sink = LangfuseSink(
                    dataset_name=config.langfuse_dataset,
                    run_name=run_name,
                    model_id=resolved.model_id,
                    provider_type=resolved.provider_type,
                    reasoning_effort=config.reasoning_effort,
                )

                def on_langfuse_item_done(
                    index: int,
                    total: int,
                    report: ItemReport,
                    _sink: LangfuseSink = sink,
                    _model_id: str = resolved.model_id,
                    _provider_type: str = resolved.provider_type,
                ) -> None:
                    _sink.log_item(report, dataset_item_id=report.id)

            # --- agentic items (multi-turn, use evaluate_agentic_*) ---
            agentic_report = None
            if agentic_items:
                agentic_report = run_agentic_items(
                    agentic_items,
                    host=config.host,
                    token=config.token,
                    workspace_id=config.workspace_id,
                    k=config.runs,
                    model_version=resolved.model_id,
                    reasoning_effort=config.reasoning_effort,
                    use_langfuse=config.log_to_langfuse,
                    run_ts=run_ts,
                    on_item_start=on_item_start,
                    on_item_done=on_item_done,
                    agent_id=config.agent_id,
                    concurrency=config.concurrency,
                )

            # --- non-agentic items (single-turn, use Evaluator) ---
            backend = _RoutingBackend(
                ChatClient(
                    host=config.host,
                    token=config.token,
                    workspace_id=config.workspace_id,
                    preserve_failed=config.preserve_failed,
                    reasoning_effort=config.reasoning_effort,
                    agent_id=config.agent_id,
                ),
                SummaryClient(host=config.host, token=config.token, workspace_id=config.workspace_id),
            )
            try:
                single_report = run_items(
                    non_agentic_items,
                    backend,
                    runs=config.runs,
                    model=resolved.model_id,
                    provider_name=resolved.provider_name or resolved.provider_id,
                    provider_type=resolved.provider_type,
                    workspace_id=config.workspace_id,
                    on_item_start=on_item_start,
                    on_run_done=on_run_done,
                    on_item_done=on_item_done,
                    on_langfuse_item_done=on_langfuse_item_done,
                    concurrency=config.concurrency,
                )
            finally:
                if hasattr(backend, "close"):
                    backend.close()

            # merge into a single report for display/export
            from gooddata_eval.core.runner import EvalReport  # noqa: PLC0415

            report = EvalReport(
                model=resolved.model_id,
                provider_name=resolved.provider_name or resolved.provider_id,
                provider_type=resolved.provider_type,
                workspace_id=config.workspace_id,
            )
            if agentic_report is not None:
                report.items.extend(agentic_report.items)
            report.items.extend(single_report.items)
            report.wall_clock_s = (agentic_report.wall_clock_s if agentic_report else 0.0) + single_report.wall_clock_s

            skipped_kinds = sorted({i.test_kind for i in report.items if i.skipped})
            if skipped_kinds:
                print(
                    f"warning: skipped {sum(i.skipped for i in report.items)} item(s) with "
                    f"unsupported test_kind(s): {', '.join(skipped_kinds)}",
                    file=sys.stderr,
                )

            render_console(report)
            reports.append(report)
    finally:
        try:
            controller.restore(original_active)
        except Exception as _restore_exc:
            print(
                f"warning: failed to restore workspace active model: {_restore_exc}",
                file=sys.stderr,
            )

    if not reports:
        print("error: no models evaluated successfully.", file=sys.stderr)
        return _EXIT_OPERATIONAL_ERROR

    if len(reports) > 1:
        render_comparison(reports)

    if config.json_path is not None:
        write_multi_model_report(reports, config.json_path)

    return _EXIT_OK


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv if argv is not None else sys.argv[1:])
    _apply_timer_flag(getattr(args, "timers", False))
    _apply_judge_model(getattr(args, "judge_model", None))
    if hasattr(args, "concurrency") and args.concurrency < 1:
        print("error: --concurrency must be >= 1.", file=sys.stderr)
        return _EXIT_OPERATIONAL_ERROR
    try:
        host, token = resolve_connection(host=args.host, token=args.token, profile=args.profile)
        if args.command == "models":
            return _list_models(host, token, getattr(args, "workspace", None))
        config = RunConfig(
            host=host,
            token=token,
            workspace_id=args.workspace,
            dataset_folder=Path(args.dataset) if args.dataset else None,
            langfuse_dataset=args.langfuse_dataset,
            models=args.models or [],
            runs=args.runs,
            concurrency=args.concurrency,
            json_path=Path(args.json_path) if args.json_path else None,
            log_to_langfuse=args.langfuse,
            quiet=args.quiet,
            kind=args.kind,
            preserve_failed=args.preserve_failed,
            reasoning_effort=args.reasoning_effort,
            agent_id=args.agent_id or os.environ.get("GD_EVAL_AGENT_ID"),
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
