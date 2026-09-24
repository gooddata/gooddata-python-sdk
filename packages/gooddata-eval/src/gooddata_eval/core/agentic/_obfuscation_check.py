# (C) 2026 GoodData Corporation. All rights reserved.
"""Deterministic leak verdict for the agentic_obfuscation kind.

Pure functions only: the caller collects the sinks, this module decides. A sink is any
JSON-like document -- the stored conversation read back over the API, or every Langfuse
trace of the conversation's session. A canary is found by exact substring over every string
leaf, so the verdict never depends on an LLM. JSON serialised inside a string (Langfuse
keeps span input that way) is decoded and walked too.

A sink that cannot be seen must not pass an absence check. Every turn therefore carries an
anchor, a non-sensitive fragment of the question, and a sink that does not show every
anchor is reported as blind instead of clean.
"""

from __future__ import annotations

import json
import re
from collections.abc import Iterator, Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

SINK_CONVERSATION_DB = "conversation_db"
SINK_LANGFUSE_TRACE = "langfuse_trace"
SINKS = (SINK_CONVERSATION_DB, SINK_LANGFUSE_TRACE)

# Classes whose value may be written with separators the detector ignores, so a leak of
# "4916 3385 0608 2832" must still match the compact nonce "4916338506082832".
_DIGIT_CLASSES = frozenset({"CREDIT_CARD", "IBAN"})
_SEPARATORS = re.compile(r"[\s\-]")
# Placeholder the AI-on-data trace redaction writes over Langfuse input and output. Behind it
# the Langfuse leg shows nothing, so an absence check there would prove nothing.
AI_ON_DATA_REDACTION = "<redacted: AI-on-data enabled>"
_ANCHOR_RUN = re.compile(r"[^\W_](?:[\w ]*[^\W_])?")
_ANCHOR_MIN = 12
_ANCHOR_MAX = 40


@dataclass(frozen=True)
class Occurrence:
    sink: str
    path: str
    needle: str


@dataclass
class CaseVerdict:
    failures: list[str] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)

    @property
    def passed(self) -> bool:
        return not self.failures


def iter_strings(value: Any, path: str = "$") -> Iterator[tuple[str, str]]:
    """Yield ``(path, text)`` for every string or number leaf and every key, decoding JSON held in a string.

    A string that parses as a JSON document is walked instead of being yielded whole, so a
    value spelled with escapes (``\\u0040``) is seen decoded and reported once. Numbers are
    leaves too: a numeric secret in a pasted JSON document decodes to an int. Keys are text a
    user can type as well -- a pasted config may key on an email -- so each is yielded at the
    path of its object with a ``<key>`` suffix.
    """
    if isinstance(value, bool):
        return
    if isinstance(value, int | float):
        yield path, str(value)
        return
    if isinstance(value, str):
        if value.lstrip()[:1] in ("{", "["):
            try:
                decoded = json.loads(value)
            except ValueError:
                pass
            else:
                yield from iter_strings(decoded, f"{path}<json>")
                return
        yield path, value
    elif isinstance(value, Mapping):
        for key, child in value.items():
            if isinstance(key, str):
                yield f"{path}.{key}<key>", key
            yield from iter_strings(child, f"{path}.{key}")
    elif isinstance(value, Sequence) and not isinstance(value, bytes | bytearray):
        for index, child in enumerate(value):
            yield from iter_strings(child, f"{path}[{index}]")


def canary_needles(canary: Mapping[str, Any]) -> list[str]:
    """Every spelling of the canary a leak may take: nonce, value and its declared variants."""
    keys = ("nonce", "value", "unescaped_value", "decoded_value", "compact_value")
    needles = [canary[key] for key in keys if isinstance(canary.get(key), str) and canary[key]]
    return list(dict.fromkeys(needles))


def find_canary(canary: Mapping[str, Any], sink: str, document: Any) -> list[Occurrence]:
    needles = canary_needles(canary)
    compact = {_SEPARATORS.sub("", n) for n in needles} if canary.get("class") in _DIGIT_CLASSES else set()
    found: list[Occurrence] = []
    for path, text in iter_strings(document):
        hit = next((n for n in needles if n in text), None)
        if hit is None and compact:
            squeezed = _SEPARATORS.sub("", text)
            hit = next((n for n in compact if n in squeezed), None)
        if hit is not None:
            found.append(Occurrence(sink, path, hit))
    return found


def contains(document: Any, needle: str) -> bool:
    return any(needle in text for _, text in iter_strings(document))


def derive_anchor(question: str, canaries: Sequence[Mapping[str, Any]]) -> str | None:
    """The longest plain-word run of the question once every canary spelling is cut out.

    Word characters and spaces only, so escaping, JSON quoting and masking next to a canary
    cannot alter it between what was sent and what a sink stores.
    """
    fragments = [question]
    # Longest spelling first: cutting the nonce out of "john\\.canary2d8e@..." first would
    # leave "john\\." behind, and the anchor would then end in text the mask replaces.
    needles = sorted({n for canary in canaries for n in canary_needles(canary)}, key=len, reverse=True)
    for needle in needles:
        fragments = [piece for fragment in fragments for piece in fragment.split(needle)]
    runs = [match.group(0) for fragment in fragments for match in _ANCHOR_RUN.finditer(fragment)]
    best = max(runs, key=len, default="")
    if len(best) < _ANCHOR_MIN:
        return None
    return best[:_ANCHOR_MAX].rstrip()


def _declared_sinks(canary: Mapping[str, Any], key: str) -> list[str]:
    sinks = canary.get(key) or []
    unknown = [s for s in sinks if s not in SINKS]
    if unknown:
        raise ValueError(f"canary {canary.get('nonce')!r} names unknown sink(s) {unknown} in {key}")
    return list(sinks)


def _format(occurrences: Sequence[Occurrence], limit: int = 5) -> str:
    shown = ", ".join(f"{o.path} ({o.needle!r})" for o in occurrences[:limit])
    more = len(occurrences) - limit
    return shown + (f" and {more} more" if more > 0 else "")


def evaluate_case(
    expected: Mapping[str, Any],
    sinks: Mapping[str, Any],
    anchors: Sequence[str],
    *,
    turn_rejected: bool = False,
) -> CaseVerdict:
    """Decide one item from the collected sinks.

    ``sinks`` maps a sink name to its document, or to ``None`` when it was not collected
    (only allowed for the Langfuse leg of a rejected turn, which may export nothing).
    """
    verdict = CaseVerdict()
    status = expected.get("status", "enforced")
    visible: dict[str, bool] = {}

    for sink in SINKS:
        document = sinks.get(sink)
        if document is None:
            visible[sink] = False
            if not turn_rejected:
                verdict.failures.append(f"{sink}: not collected, so no absence claim can be made")
            continue
        if sink == SINK_LANGFUSE_TRACE and contains(document, AI_ON_DATA_REDACTION):
            verdict.failures.append(
                f"{sink}: trace input/output is replaced by {AI_ON_DATA_REDACTION!r} (enableAiOnData with "
                "enableGenAiTraceRedaction), so the obfuscation leg cannot be observed here"
            )
            visible[sink] = False
            continue
        missing = [anchor for anchor in anchors if not contains(document, anchor)]
        if missing and not turn_rejected:
            verdict.failures.append(f"{sink}: blind -- anchor(s) {missing} not found, the read-back is incomplete")
            visible[sink] = False
            continue
        visible[sink] = True

    for canary in expected.get("canaries", []):
        label = f"{canary.get('class')} {canary.get('nonce')!r}"
        for sink in _declared_sinks(canary, "absent_from"):
            # A blind sink still convicts: a canary it does show is a leak all the same.
            if sinks.get(sink) is None:
                continue
            occurrences = find_canary(canary, sink, sinks[sink])
            # Paths the item declares as not yet decided (e.g. conversation state the SC does
            # not rule on) are reported, never gated, until a decision turns them into leaks.
            record_only = [re.compile(p) for p in canary.get("record_only_paths") or []]
            recorded = [o for o in occurrences if any(r.search(o.path) for r in record_only)]
            gated = [o for o in occurrences if o not in recorded]
            if gated:
                verdict.failures.append(f"LEAK {label} in {sink}: {_format(gated)}")
            if recorded:
                verdict.notes.append(f"RECORDED {label} in {sink} (record-only path, not gated): {_format(recorded)}")
            marker = canary.get("mask_marker_present")
            if marker and not turn_rejected and visible.get(sink) and not contains(sinks[sink], marker):
                verdict.failures.append(f"{label}: mask marker {marker!r} missing from {sink}")
        for sink in _declared_sinks(canary, "present_in"):
            if not visible.get(sink):
                continue
            if not find_canary(canary, sink, sinks[sink]):
                if status == "known_limitation":
                    flip = (expected.get("known_limitation") or {}).get("flip_when", "")
                    verdict.failures.append(
                        f"{label} expected in {sink} ({status}) but is now masked -- the limitation no longer "
                        f"reproduces, update the fixture deliberately. flip_when: {flip}"
                    )
                else:
                    # An enforced present_in guards a value that is not sensitive: masking it is
                    # the defect (a false positive), not progress.
                    verdict.failures.append(
                        f"OVER-MASKED {label} in {sink}: expected unchanged but it was masked (false positive)"
                    )

    if turn_rejected and sinks.get(SINK_LANGFUSE_TRACE) is None:
        verdict.notes.append("rejected turn exported no Langfuse trace; only the database leg was asserted")
    return verdict
