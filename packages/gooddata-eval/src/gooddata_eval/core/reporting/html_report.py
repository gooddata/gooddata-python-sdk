# (C) 2026 GoodData Corporation
"""Render one or more JSON reports as a single self-contained HTML file.

This is a *view* over ``json_report.py``'s output, never a second source of truth: it
adds no numbers of its own, it only makes the existing ones navigable. The result is one
file with no external references -- it opens over ``file://``, attaches to a Jira issue
and survives a Slack thread, which is most of the point.

Passing several JSON files merges them into one report, each becoming its own column.
That is how run-over-run comparison works: no database, no run registry, just the files
you already have on disk.
"""

from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

import orjson

_TEMPLATE = Path(__file__).with_name("report_template.html")
_PLACEHOLDER = "__GD_EVAL_DATA__"

# Dropped outright (not blanked) from a redacted report, so it cannot be un-redacted by
# reading the embedded data blob: internal ids, and the model's own raw reasoning text.
_REDACTED_ITEM_FIELDS = frozenset({"conversation_id", "response_id", "reasoning"})

# Same, one level down inside `detail`. The transcript goes because the simulated user is
# primed with the expected output -- showing the exchange discloses how we score, not just
# what scored. `turns` (a count) stays: "this needed a clarification round" is a fair fact.
# tool_calls goes because a tool result carries semantic-layer internals and real query
# rows; `latency_breakdown` stays, so the redacted timeline still shows which tool ran and
# for how long, just not what it was handed or what came back.
_REDACTED_DETAIL_FIELDS = frozenset({"transcript", "tool_calls"})

# Same again, one level down inside each `failed_runs` entry. The per-run records carry
# their *own* ids and their own raw reasoning (`reasoning_steps`), so redacting only the
# item's top level left the identical content exposed one level deeper -- the top-level
# `reasoning` dropped while the same text survived verbatim in `failed_runs`.
#
# Kept on purpose, matching what the top level keeps: `reasoning_step_count` (a count, like
# `detail.turns`), `tool_call_count`/`tool_names` (which tool ran, never its arguments or
# its result -- the same line `latency_breakdown` draws), and the run's verdict, error and
# timings, which are facts about the run rather than about our infrastructure.
_REDACTED_RUN_FIELDS = frozenset({"conversation_id", "response_id", "reasoning_steps"})


def _redact_detail(detail: dict) -> dict:
    return {k: v for k, v in detail.items() if k not in _REDACTED_DETAIL_FIELDS}


def _redact_failed_run(run: dict) -> dict:
    out = {k: v for k, v in run.items() if k not in _REDACTED_RUN_FIELDS}
    detail = out.get("detail")
    if isinstance(detail, dict):
        out["detail"] = _redact_detail(detail)
    return out


def _redact_item(item: dict) -> dict:
    out = {k: v for k, v in item.items() if k not in _REDACTED_ITEM_FIELDS}
    detail = out.get("detail")
    if isinstance(detail, dict):
        out["detail"] = _redact_detail(detail)
    failed_runs = out.get("failed_runs")
    if isinstance(failed_runs, list):
        out["failed_runs"] = [_redact_failed_run(run) if isinstance(run, dict) else run for run in failed_runs]
    return out


def _model_of(label: str, run: dict) -> str:
    """The model a run is of, read as the page reads it: the run's own `model`, else what follows the source in its label."""
    return run.get("model") or (label.split(" · ", 1)[1] if " · " in label else label)


def _aliases(doc: dict) -> dict[str, tuple[str, str]]:
    """Map each run label to its redacted ``(run label, model name)``.

    The alias follows the model, not the run: a model keeps one letter however many runs it has,
    so one model's history is never mistaken for several models. A model with a single run is just
    ``Model A``; one with several has its runs numbered in input order within the model
    (``Run 1 · Model A``, ``Run 2 · Model A``), which keeps their labels distinct and lets the page
    read them as one model's history. Letters go out in the order models first appear. As on the page,
    a model is told apart by its provider as well as its id.
    """
    runs = doc.get("runs") or {}
    comparison = doc.get("comparison") or {}
    identity = {
        label: ((comparison.get(label) or {}).get("provider_name") or "", _model_of(label, run))
        for label, run in runs.items()
    }
    letters: dict[tuple[str, str], str] = {}
    for model in identity.values():
        letters.setdefault(model, f"Model {chr(65 + len(letters))}")
    per_model = Counter(identity.values())
    seen: Counter[tuple[str, str]] = Counter()
    aliases: dict[str, tuple[str, str]] = {}
    for label, model in identity.items():
        seen[model] += 1
        name = letters[model]
        aliases[label] = (name if per_model[model] == 1 else f"Run {seen[model]} · {name}", name)
    return aliases


def _redact(doc: dict) -> dict:
    """Strip internal ids and replace model names with stable aliases.

    Per-item latency and pass/fail survive -- those are facts about the run a customer is
    entitled to. What goes is anything that identifies our infrastructure or discloses
    which model was under test.
    """
    alias = _aliases(doc)
    runs = {
        alias[label][0]: {
            **run,
            "model": alias[label][1],
            "workspace_id": "",
            "items": {item_id: _redact_item(item) for item_id, item in (run.get("items") or {}).items()},
        }
        for label, run in (doc.get("runs") or {}).items()
    }
    comparison = {
        alias[label][0]: {**entry, "provider_name": ""}
        for label, entry in (doc.get("comparison") or {}).items()
        if label in alias
    }
    return {"runs": runs, "comparison": comparison}


def merge_docs(docs: list[tuple[str, dict]]) -> dict:
    """Merge ``(source_label, json_report_doc)`` pairs into one multi-run document.

    With more than one source the source label is prefixed onto every run key, so the
    same model evaluated on two different days stays two distinct columns instead of one
    silently overwriting the other.
    """
    prefix = len(docs) > 1
    runs: dict[str, dict] = {}
    comparison: dict[str, dict] = {}
    for source, doc in docs:
        for label, run in (doc.get("runs") or {}).items():
            key = f"{source} · {label}" if prefix else label
            unique, n = key, 2
            while unique in runs:
                unique, n = f"{key} ({n})", n + 1
            runs[unique] = run
            entry = (doc.get("comparison") or {}).get(label)
            if entry is not None:
                comparison[unique] = entry
    return {"runs": runs, "comparison": comparison}


def load_report_files(paths: list[Path]) -> dict:
    """Read JSON report files and merge them into one document."""
    docs: list[tuple[str, dict]] = []
    for p in paths:
        path = Path(p)
        doc = orjson.loads(path.read_bytes())
        if "runs" not in doc:
            # A bare single-run dict from the older build_json_report shape.
            doc = {"runs": {doc.get("model") or path.stem: doc}, "comparison": {}}
        docs.append((path.stem, doc))
    return merge_docs(docs)


def build_html(doc: dict, redact: bool = False, title: str = "gd-eval report") -> str:
    """Render a merged report document into a standalone HTML page."""
    payload = {
        "title": title,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "redacted": redact,
        **(_redact(doc) if redact else {"runs": doc.get("runs") or {}, "comparison": doc.get("comparison") or {}}),
    }
    # "</" would close the host <script> tag early; "<\/" is an equivalent JSON escape and
    # "<" cannot occur outside a JSON string, so this is safe to apply to the whole blob.
    blob = orjson.dumps(payload).decode().replace("</", "<\\/")
    return _TEMPLATE.read_text(encoding="utf-8").replace(_PLACEHOLDER, blob)


def write_html_report(doc: dict, path: Path, redact: bool = False, title: str = "gd-eval report") -> None:
    Path(path).write_text(build_html(doc, redact=redact, title=title), encoding="utf-8")
