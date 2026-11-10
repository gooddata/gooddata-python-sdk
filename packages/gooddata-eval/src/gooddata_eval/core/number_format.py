# (C) 2026 GoodData Corporation
"""Whether the number format an agent wrote for a metric does what the user asked for.

The agent writes a `format` and a `format_example` (`{value, shown_as}`) for each formatted
metric, and the chart tool rejects the call unless the format renders `value` as
`shown_as`. So `shown_as` is how the chart really reads `value`. What the tool cannot know
is whether that reading is what the user asked for: a "millions" request answered with
`#,##0.0M` and the example `4,221,301,265.5M` passes the tool and shows a number a million
times too large (GDAI-2592). This module reads the example back against the user's intent.

An intent is one of:
- `{"divide_by": 1000000, "decimals": 1, "suffix": "M", "prefix": ""}`: value / divide_by;
- `{"kind": "auto_scale", "decimals": 1}`: B, M or K by the size of the value;
- `{"kind": "percent", "decimals": 1}`: a ratio times 100, with "%";
- `{"negative": "parentheses", "decimals": 0}`: a negative value written in parentheses;
- `None`: no format may be written at all.

The shown text is compared as a number, not as a string, because equally correct formats
differ in grouping and spacing: `#,##0.0,,M` reads `4,221.3M` and `#,,.0 M` reads `4221.3 M`.
"""

import re
from collections.abc import Mapping
from typing import Any

from gooddata_eval.core.models import ToolCallEvent
from gooddata_eval.core.scoring import resolve_alias_to_uri

_INTENT_KEYS = frozenset({"kind", "divide_by", "decimals", "prefix", "suffix", "negative"})
_KINDS = frozenset({"auto_scale", "percent"})
_TIERS = ((1e9, "B"), (1e6, "M"), (1e3, "K"))
_NUMBER = re.compile(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?")


def validate_format_intents(intents: object) -> None:
    """Reject a malformed `format_intents` before any request.

    Raises:
        ValueError: the mapping or one of its intents is unusable.
    """
    if not isinstance(intents, Mapping) or not intents:
        raise ValueError(f"format_intents must map metric uris to an intent or null, got {intents!r}")
    for uri, intent in intents.items():
        if not isinstance(uri, str) or not uri.startswith(("metric/", "fact/")):
            raise ValueError(f"format_intents keys must be metric/ or fact/ uris, got {uri!r}")
        if intent is None:
            continue
        if not isinstance(intent, Mapping):
            raise ValueError(f"format_intents[{uri!r}] must be an object or null, got {intent!r}")
        unknown = sorted(set(intent) - _INTENT_KEYS)
        if unknown:
            raise ValueError(f"format_intents[{uri!r}] states {unknown}, which is not one of {sorted(_INTENT_KEYS)}")
        if intent.get("kind") is not None and intent["kind"] not in _KINDS:
            raise ValueError(f"format_intents[{uri!r}] kind must be one of {sorted(_KINDS)}, got {intent['kind']!r}")
        if intent.get("negative") not in (None, "parentheses"):
            raise ValueError(f"format_intents[{uri!r}] negative must be 'parentheses', got {intent['negative']!r}")
        decimals = intent.get("decimals", 0)
        if not isinstance(decimals, int) or isinstance(decimals, bool) or decimals < 0:
            raise ValueError(f"format_intents[{uri!r}] decimals must be a non-negative integer, got {decimals!r}")
        divide_by = intent.get("divide_by", 1)
        if not isinstance(divide_by, (int, float)) or isinstance(divide_by, bool) or divide_by <= 0:
            raise ValueError(f"format_intents[{uri!r}] divide_by must be a positive number, got {divide_by!r}")


def _authored_metric_entries(tool_call_events: list[ToolCallEvent]) -> dict[str, dict]:
    """The metric entries of the last successful `create_adhoc_visualization` call, by metric uri.

    `format_example` exists only in the tool arguments: the tool drops it from the chart it
    returns, so the chart part of the answer cannot be read for it. A metric sits in `metrics`,
    in a bubble chart's `size_by`, or in a repeater's `columns`, as the scorer counts it.
    """
    entries: dict[str, dict] = {}
    for tc in tool_call_events:
        if tc.function_name != "create_adhoc_visualization":
            continue
        result = tc.parsed_result()
        if not isinstance(result, dict) or result.get("status", "success") != "success":
            continue
        viz = tc.parsed_arguments().get("visualization")
        if not isinstance(viz, dict):
            continue
        fields = (viz.get("query") or {}).get("fields") or {}
        entries = {}
        for entry in [*(viz.get("metrics") or []), *(viz.get("size_by") or []), *(viz.get("columns") or [])]:
            if isinstance(entry, dict) and isinstance(entry.get("field"), str):
                entries[resolve_alias_to_uri(entry["field"], fields)] = entry
    return entries


def _target(intent: Mapping[str, Any], value: float) -> tuple[float, str, str, bool] | str:
    """`(number shown, prefix, suffix, parentheses)` the intent asks for, or why the example cannot tell."""
    divide_by = intent.get("divide_by", 1)
    prefix, suffix = intent.get("prefix", ""), intent.get("suffix", "")
    # Parentheses combine with any kind: they replace the sign, and the kind sets the number.
    parentheses = intent.get("negative") == "parentheses"
    if parentheses and value >= 0:
        return f"the example value {value} is not negative, so it cannot show the parentheses"
    magnitude = abs(value) if parentheses else value
    if intent.get("kind") == "percent":
        return magnitude * 100, prefix, "%", parentheses
    if intent.get("kind") == "auto_scale":
        for threshold, tier in _TIERS:
            if abs(value) >= threshold:
                return magnitude / threshold, prefix, tier, parentheses
        return f"the example value {value} is below a thousand, so it cannot show a B/M/K tier"
    # Only a real scaling needs a value it can divide: with no `divide_by`, 0.45 shows as is.
    if divide_by > 1 and abs(value) < divide_by:
        return f"the example value {value} is below {divide_by}, so it cannot show the scaling"
    return magnitude / divide_by, prefix, suffix, parentheses


def _read(shown: str, prefix: str, suffix: str, parentheses: bool) -> tuple[float, int] | None:
    """The number `shown` states and its decimal places, or None when it is not written that way."""
    text = "".join(shown.split())
    negative = False
    if parentheses:
        if not (text.startswith("(") and text.endswith(")")):
            return None
        text, negative = text[1:-1], True
    if text.startswith("-"):
        text, negative = text[1:], True
    if prefix and not text.startswith(prefix):
        return None
    text = text[len(prefix) :]
    if text.startswith("-"):
        text, negative = text[1:], True
    if suffix:
        if not text.endswith(suffix):
            return None
        text = text[: -len(suffix)]
    if not _NUMBER.fullmatch(text):
        return None
    number = float(text.replace(",", ""))
    decimals = len(text.split(".", 1)[1]) if "." in text else 0
    return (-number if negative else number), decimals


def format_problem(intent: Mapping[str, Any], example: object) -> str | None:
    """Why the example does not read the way the intent asks, or None when it does."""
    if not isinstance(example, Mapping):
        return "no format_example was written"
    value, shown = example.get("value"), example.get("shown_as")
    if not isinstance(value, (int, float)) or isinstance(value, bool) or not isinstance(shown, str):
        return f"the format_example {dict(example)!r} has no numeric value to check"
    target = _target(intent, float(value))
    if isinstance(target, str):
        return target
    number, prefix, suffix, parentheses = target
    decimals = intent.get("decimals", 0)
    read = _read(shown, prefix, suffix, parentheses)
    expected_text = f"{'(' if parentheses else ''}{prefix}{number:,.{decimals}f}{suffix}{')' if parentheses else ''}"
    if read is None:
        return f"{value} is shown as {shown!r}, expected {expected_text!r}"
    shown_number, shown_decimals = read
    wanted = -number if parentheses else number
    if shown_decimals != decimals or abs(shown_number - wanted) > 0.5 * 10**-decimals + 1e-9:
        return f"{value} is shown as {shown!r}, expected {expected_text!r}"
    return None


def check_format_intents(
    intents: Mapping[str, Mapping[str, Any] | None], tool_call_events: list[ToolCallEvent]
) -> list[str]:
    """Every metric with an intent must carry a format whose example reads as asked; [] when all do."""
    entries = _authored_metric_entries(tool_call_events)
    problems: list[str] = []
    for uri, intent in intents.items():
        entry = entries.get(uri)
        if intent is None:
            if entry is not None and entry.get("format"):
                problems.append(f"{uri}: a format {entry['format']!r} was written, but none was asked for")
            continue
        if entry is None or not entry.get("format"):
            problems.append(f"{uri}: no format was written")
            continue
        problem = format_problem(intent, entry.get("format_example"))
        if problem is not None:
            problems.append(f"{uri}: {problem} (format {entry['format']!r})")
    return problems
