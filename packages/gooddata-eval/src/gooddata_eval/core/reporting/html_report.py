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


def _redact_item(item: dict) -> dict:
    out = {k: v for k, v in item.items() if k not in _REDACTED_ITEM_FIELDS}
    detail = out.get("detail")
    if isinstance(detail, dict):
        out["detail"] = {k: v for k, v in detail.items() if k not in _REDACTED_DETAIL_FIELDS}
    return out


def _redact(doc: dict) -> dict:
    """Strip internal ids and replace model names with stable aliases.

    Per-item latency and pass/fail survive -- those are facts about the run a customer is
    entitled to. What goes is anything that identifies our infrastructure or discloses
    which model was under test.
    """
    alias = {label: f"Model {chr(65 + n)}" for n, label in enumerate(doc.get("runs", {}))}
    runs = {
        alias[label]: {
            **run,
            "model": alias[label],
            "workspace_id": "",
            "items": {item_id: _redact_item(item) for item_id, item in (run.get("items") or {}).items()},
        }
        for label, run in doc.get("runs", {}).items()
    }
    comparison = {
        alias[label]: {**entry, "provider_name": ""}
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
