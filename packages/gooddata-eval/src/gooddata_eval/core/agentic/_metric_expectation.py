# (C) 2026 GoodData Corporation. All rights reserved.
"""What a metric-skill item expects, parsed from its ``expected_output``, and the matchers that judge it.

An item states its expectation in one of two shapes. A list of ``{"maql": ...}`` candidates, or a
dict carrying one candidate, is the original shape: the agent must create one metric whose MAQL
matches a candidate. A dict that carries any key of ``OPTION_KEYS`` is the options shape: every key
is a check the item opts into, and an item without a key is not held to it. A malformed options dict
raises ``ValueError`` before any request, so a typo never reads green.
"""

from __future__ import annotations

import difflib
import re
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.evaluators._maql import normalize_maql

FORMAT_KINDS = ("percent", "currency", "integer", "decimal")

_FIELD_KEYS = (
    "title",
    "metric_id",
    "format",
    "format_kind",
    "format_contains",
    "description",
    "description_contains",
    "tags",
    "tags_include",
)
_UPDATE_KEYS = (*_FIELD_KEYS, "maql")
OPTION_KEYS = frozenset(
    {
        "candidates",
        "user_replies",
        "run_all_replies",
        "expect_no_create",
        "expected_mentions",
        "expect_no_overwrite",
        "expect_clarification",
        "confirmation_turn",
        "expect_confirmation_stop",
        "rubric",
        "expected_fields",
        "expected_update",
        "expected_metrics",
        "expect_no_deletion",
        "expect_executes",
        "score_first_proposal",
        "expect_suggestions",
    }
)

_CURRENCY_MARKS = ("$", "€", "£", "¥", "Kč")
_DECIMAL_RE = re.compile(r"\.[0#]")
_PLACEHOLDER_RE = re.compile(r"\{metric/@(\d+)\}")
# A formula in an inline code span or in a fenced block, with or without a language tag.
_PROPOSED_MAQL_RE = re.compile(r"```[a-zA-Z]*\s*(SELECT\b[^`]*?)\s*```|`(SELECT\b[^`]*)`", re.IGNORECASE)


@dataclass(frozen=True)
class FieldSpec:
    """Values the stored metric must carry. A field left as None or empty is not checked."""

    title: str | None = None
    metric_id: str | None = None
    format: str | None = None
    format_kind: str | None = None
    format_contains: tuple[str, ...] = ()
    description: str | None = None
    description_contains: tuple[str, ...] = ()
    tags: frozenset[str] | None = None
    tags_include: frozenset[str] = frozenset()


@dataclass(frozen=True)
class UpdateSpec:
    """An existing metric the agent must update: the listed fields change, every other field stays."""

    metric_id: str
    fields: FieldSpec
    maql: tuple[str, ...] = ()


@dataclass(frozen=True)
class MetricExpectation:
    """The parsed expectation of one metric-skill item."""

    candidates: list[dict] = field(default_factory=list)
    legacy: bool = True
    user_replies: tuple[str, ...] = ()
    run_all_replies: bool = False
    expect_no_create: bool = False
    expected_mentions: tuple[str, ...] = ()
    expect_no_overwrite: bool = False
    expect_clarification: bool = False
    confirmation_turn: int | None = None
    rubric: str | None = None
    expected_fields: FieldSpec | None = None
    expected_update: UpdateSpec | None = None
    expected_metrics: tuple[tuple[str, ...], ...] = ()
    # Ids of metrics that must still exist after the run. A list, not a flag: other items create and delete
    # their own metrics in the same workspace at the same time.
    expect_no_deletion: tuple[str, ...] = ()
    expect_executes: bool = False
    score_first_proposal: bool = False
    expect_suggestions: bool = False

    @property
    def needs_workspace(self) -> bool:
        """Whether a run reads the workspace's metrics through REST: every options-shape item does."""
        return not self.legacy


def _is_options_shape(raw: Any) -> bool:
    return isinstance(raw, dict) and any(key in OPTION_KEYS for key in raw)


def _misspelt_option_key(candidate: dict) -> tuple[str, str] | None:
    """A key of an original-shape candidate that reads as a misspelt option key, with the key it resembles.

    Such a key keeps the dict in the original shape, so the check it asks for would be dropped without a word. The
    fields a candidate carries beside its MAQL (title, format, tags, ...) resemble no option key.
    """
    for key in candidate:
        match = difflib.get_close_matches(str(key), OPTION_KEYS, n=1, cutoff=0.8)
        if match:
            return str(key), match[0]
    return None


def _strings(value: Any, name: str) -> tuple[str, ...]:
    """A non-empty string, or a list of them, as a tuple."""
    items = [value] if isinstance(value, str) else value
    if not isinstance(items, list) or not items or not all(isinstance(s, str) and s.strip() for s in items):
        raise ValueError(f"{name} must be a non-empty string or a list of them, got {value!r}")
    return tuple(items)


def _flag(raw: dict, name: str) -> bool:
    value = raw.get(name, False)
    if not isinstance(value, bool):
        raise ValueError(f"{name} must be true or false, got {value!r}")
    return value


def _candidates(value: Any, name: str) -> list[dict]:
    """``[{"maql": ...}]`` or a plain list of MAQL strings, as candidate dicts."""
    if isinstance(value, str):
        value = [value]
    if not isinstance(value, list) or not value:
        raise ValueError(f"{name} must be a non-empty list of MAQL candidates, got {value!r}")
    out: list[dict] = []
    for candidate in value:
        maql = candidate.get("maql") if isinstance(candidate, dict) else candidate
        if not isinstance(maql, str) or not maql.strip():
            raise ValueError(f"{name}: every candidate needs a non-empty MAQL, got {candidate!r}")
        out.append(candidate if isinstance(candidate, dict) else {"maql": maql})
    return out


def _field_spec(raw: Any, name: str, allowed: tuple[str, ...]) -> FieldSpec:
    if not isinstance(raw, dict) or not raw:
        raise ValueError(f"{name} must be a non-empty object, got {raw!r}")
    unknown = sorted(set(raw) - set(allowed))
    if unknown:
        raise ValueError(f"{name}: unknown key(s) {unknown}; allowed: {list(allowed)}")
    kind = raw.get("format_kind")
    if "format_kind" in raw and kind not in FORMAT_KINDS:
        raise ValueError(f"{name}.format_kind must be one of {FORMAT_KINDS}, got {kind!r}")
    for key in ("title", "metric_id", "format", "description"):
        if key in raw and (not isinstance(raw[key], str) or not raw[key].strip()):
            raise ValueError(f"{name}.{key} must be a non-empty string, got {raw[key]!r}")
    return FieldSpec(
        title=raw.get("title"),
        metric_id=raw.get("metric_id"),
        format=raw.get("format"),
        format_kind=kind,
        format_contains=_strings(raw["format_contains"], f"{name}.format_contains") if "format_contains" in raw else (),
        description=raw.get("description"),
        description_contains=(
            _strings(raw["description_contains"], f"{name}.description_contains")
            if "description_contains" in raw
            else ()
        ),
        tags=frozenset(_strings(raw["tags"], f"{name}.tags")) if "tags" in raw else None,
        tags_include=frozenset(_strings(raw["tags_include"], f"{name}.tags_include"))
        if "tags_include" in raw
        else frozenset(),
    )


def parse_expectation(raw: Any) -> MetricExpectation:
    """Parse and validate an item's ``expected_output``.

    Raises:
        ValueError: The options shape names an unknown key, a key holds the wrong type, two keys
            contradict each other, or the item checks nothing at all.
    """
    if not _is_options_shape(raw):
        legacy = raw if isinstance(raw, list) else [raw]
        if not all(isinstance(c, dict) for c in legacy):
            raise ValueError(
                f"expected_output: a candidate list holds dicts with a 'maql' key, got {raw!r}; "
                "plain MAQL strings go under 'candidates'"
            )
        for candidate in legacy:
            misspelt = _misspelt_option_key(candidate)
            if misspelt is not None:
                raise ValueError(f"expected_output: unknown key {misspelt[0]!r}; did you mean {misspelt[1]!r}?")
        return MetricExpectation(candidates=list(legacy))

    unknown = sorted(set(raw) - OPTION_KEYS)
    if unknown:
        raise ValueError(f"expected_output: unknown key(s) {unknown}; allowed: {sorted(OPTION_KEYS)}")

    candidates = _candidates(raw["candidates"], "candidates") if "candidates" in raw else []
    replies = _strings(raw["user_replies"], "user_replies") if "user_replies" in raw else ()
    run_all = _flag(raw, "run_all_replies")
    no_create = _flag(raw, "expect_no_create")
    mentions = _strings(raw["expected_mentions"], "expected_mentions") if "expected_mentions" in raw else ()

    if "confirmation_turn" in raw and "expect_confirmation_stop" in raw:
        raise ValueError("give confirmation_turn or expect_confirmation_stop, not both")
    confirmation_turn: int | None = None
    if "confirmation_turn" in raw:
        confirmation_turn = raw["confirmation_turn"]
        if isinstance(confirmation_turn, bool) or not isinstance(confirmation_turn, int) or confirmation_turn < 2:
            raise ValueError(f"confirmation_turn must be an integer of at least 2, got {confirmation_turn!r}")
    elif _flag(raw, "expect_confirmation_stop"):
        confirmation_turn = 2

    rubric = raw.get("rubric")
    if "rubric" in raw and (not isinstance(rubric, str) or not rubric.strip()):
        raise ValueError(f"rubric must be a non-empty string, got {rubric!r}")

    fields = _field_spec(raw["expected_fields"], "expected_fields", _FIELD_KEYS) if "expected_fields" in raw else None

    update: UpdateSpec | None = None
    if "expected_update" in raw:
        upd = raw["expected_update"]
        if not isinstance(upd, dict) or not isinstance(upd.get("metric_id"), str) or not upd["metric_id"].strip():
            raise ValueError(f"expected_update needs a metric_id, got {upd!r}")
        maql = _strings(upd["maql"], "expected_update.maql") if "maql" in upd else ()
        rest = {k: v for k, v in upd.items() if k not in ("metric_id", "maql")}
        unknown_upd = sorted(set(rest) - set(_UPDATE_KEYS))
        if unknown_upd:
            raise ValueError(f"expected_update: unknown key(s) {unknown_upd}; allowed: {['metric_id', *_UPDATE_KEYS]}")
        if not rest and not maql:
            raise ValueError("expected_update must list at least one field that changes")
        update = UpdateSpec(
            metric_id=upd["metric_id"],
            fields=_field_spec(rest, "expected_update", _FIELD_KEYS) if rest else FieldSpec(),
            maql=maql,
        )

    metrics: tuple[tuple[str, ...], ...] = ()
    if "expected_metrics" in raw:
        entries = raw["expected_metrics"]
        if not isinstance(entries, list) or len(entries) < 2:
            raise ValueError(f"expected_metrics must list at least two metrics, got {entries!r}")
        parsed: list[tuple[str, ...]] = []
        for i, entry in enumerate(entries):
            source = entry.get("candidates", entry.get("maql")) if isinstance(entry, dict) else entry
            parsed.append(tuple(c["maql"] for c in _candidates(source, f"expected_metrics[{i}]")))
            for ref in _PLACEHOLDER_RE.findall(" ".join(parsed[-1])):
                if int(ref) >= i:
                    raise ValueError(
                        f"expected_metrics[{i}] refers to {{metric/@{ref}}}, which is not an earlier entry"
                    )
        metrics = tuple(parsed)

    no_deletion = _strings(raw["expect_no_deletion"], "expect_no_deletion") if "expect_no_deletion" in raw else ()
    executes = _flag(raw, "expect_executes")
    suggestions = _flag(raw, "expect_suggestions")
    no_overwrite = _flag(raw, "expect_no_overwrite")
    if no_create and (candidates or metrics or fields or update or executes or suggestions):
        raise ValueError(
            "expect_no_create cannot be combined with candidates, expected_metrics, expected_fields, "
            "expected_update, expect_executes or expect_suggestions: each needs a written metric"
        )
    if (executes or suggestions) and not (candidates or fields):
        raise ValueError("expect_executes and expect_suggestions need candidates or expected_fields: a metric to judge")
    if update and no_overwrite:
        raise ValueError("expected_update writes over an existing metric, which expect_no_overwrite forbids")
    if mentions and not no_create:
        raise ValueError("expected_mentions needs expect_no_create")
    if run_all and not replies:
        raise ValueError("run_all_replies needs user_replies")
    if metrics and (candidates or not replies):
        raise ValueError("expected_metrics needs user_replies and replaces candidates")
    if update and candidates:
        raise ValueError("expected_update carries its own maql; drop candidates")

    spec = MetricExpectation(
        candidates=candidates,
        legacy=False,
        user_replies=replies,
        run_all_replies=run_all,
        expect_no_create=no_create,
        expected_mentions=mentions,
        expect_no_overwrite=no_overwrite,
        expect_clarification=_flag(raw, "expect_clarification"),
        confirmation_turn=confirmation_turn,
        rubric=rubric,
        expected_fields=fields,
        expected_update=update,
        expected_metrics=metrics,
        expect_no_deletion=no_deletion,
        expect_executes=executes,
        score_first_proposal=_flag(raw, "score_first_proposal"),
        expect_suggestions=suggestions,
    )
    if spec.score_first_proposal and not candidates:
        raise ValueError("score_first_proposal needs candidates")
    # Checks of what the agent must do. expect_no_create counts: a completed answer without a write is its point.
    # expect_no_overwrite, confirmation_turn and expect_no_deletion only forbid, so alone they pass an agent that
    # does nothing at all.
    if not (candidates or no_create or metrics or update or fields or spec.expect_clarification or rubric):
        if no_overwrite or confirmation_turn is not None or no_deletion:
            raise ValueError(
                "expect_no_overwrite, confirmation_turn and expect_no_deletion pass an agent that does nothing; "
                "add candidates, expected_fields, expected_update, expected_metrics, expect_no_create, "
                "expect_clarification or a rubric"
            )
        raise ValueError("expected_output checks nothing: give candidates or at least one expect_* key")
    return spec


def format_matches_kind(fmt: str, kind: str) -> bool:
    """Whether a number format string shows the given kind of number. A missing format shows no kind."""
    if not fmt.strip():
        return False
    if kind == "percent":
        return "%" in fmt
    if kind == "currency":
        return any(mark in fmt for mark in _CURRENCY_MARKS)
    if kind == "integer":
        return _DECIMAL_RE.search(fmt) is None
    return _DECIMAL_RE.search(fmt) is not None


def _norm_text(value: Any) -> str:
    return " ".join(str(value or "").split()).casefold()


def _tags(value: Any) -> frozenset[str]:
    return frozenset(_norm_text(t) for t in (value or []))


def stored_fields(attributes: dict) -> dict:
    """The comparable fields of a metric's entity attributes: every writable one, none the server manages."""
    content = attributes.get("content") or {}
    return {
        "title": attributes.get("title") or "",
        "description": attributes.get("description") or "",
        "tags": sorted(attributes.get("tags") or []),
        "format": content.get("format") or "",
        "maql": content.get("maql") or "",
        "isHidden": bool(attributes.get("isHidden")),
        "isHiddenFromKda": bool(attributes.get("isHiddenFromKda")),
        "conditionalFormatting": attributes.get("conditionalFormatting"),
    }


def field_mismatches(spec: FieldSpec, metric_id: str, attributes: dict | None) -> list[str]:
    """How the stored metric differs from the spec; empty when every listed field matches."""
    if attributes is None:
        return [f"metric {metric_id!r} is not stored in the workspace"]
    stored = stored_fields(attributes)
    out: list[str] = []
    if spec.metric_id is not None and spec.metric_id != metric_id:
        out.append(f"metric_id: expected {spec.metric_id!r}, got {metric_id!r}")
    if spec.title is not None and _norm_text(spec.title) != _norm_text(stored["title"]):
        out.append(f"title: expected {spec.title!r}, got {stored['title']!r}")
    if spec.format is not None and spec.format.strip() != stored["format"].strip():
        out.append(f"format: expected {spec.format!r}, got {stored['format']!r}")
    if spec.format_kind is not None and not format_matches_kind(stored["format"], spec.format_kind):
        out.append(f"format: expected a {spec.format_kind} format, got {stored['format']!r}")
    out += [f"format: {s!r} not in {stored['format']!r}" for s in spec.format_contains if s not in stored["format"]]
    if spec.description is not None and spec.description.strip() != stored["description"].strip():
        out.append(f"description: expected {spec.description!r}, got {stored['description']!r}")
    out += [
        f"description: {s!r} not in {stored['description']!r}"
        for s in spec.description_contains
        if _norm_text(s) not in _norm_text(stored["description"])
    ]
    if spec.tags is not None and _tags(spec.tags) != _tags(stored["tags"]):
        out.append(f"tags: expected {sorted(spec.tags)}, got {stored['tags']}")
    missing = _tags(spec.tags_include) - _tags(stored["tags"])
    if missing:
        out.append(f"tags: {sorted(missing)} missing from {stored['tags']}")
    return out


def update_mismatches(spec: UpdateSpec, before: dict | None, after: dict | None) -> list[str]:
    """How an update differs from the spec: a listed field did not change as asked, or another field moved."""
    if before is None:
        return [f"metric {spec.metric_id!r} did not exist before the run"]
    out = field_mismatches(spec.fields, spec.metric_id, after)
    if after is None:
        return out
    old, new = stored_fields(before), stored_fields(after)
    if spec.maql and not any(normalize_maql(m) == normalize_maql(new["maql"]) for m in spec.maql):
        out.append(f"maql: expected one of {list(spec.maql)}, got {new['maql']!r}")
    listed = {
        "title": spec.fields.title is not None,
        "description": spec.fields.description is not None or bool(spec.fields.description_contains),
        "tags": spec.fields.tags is not None or bool(spec.fields.tags_include),
        "format": spec.fields.format is not None
        or spec.fields.format_kind is not None
        or bool(spec.fields.format_contains),
        "maql": bool(spec.maql),
    }
    for key in old:
        same = normalize_maql(old[key]) == normalize_maql(new[key]) if key == "maql" else old[key] == new[key]
        if listed.get(key) and same:
            # The final value matching is not enough: a request already met before the run proves no update.
            out.append(f"{key} did not change although the request asked for it: still {new[key]!r}")
        elif not listed.get(key) and not same:
            out.append(f"{key} changed although the request did not ask for it: {old[key]!r} -> {new[key]!r}")
    return out


def substitute_placeholders(maql: str, created_ids: list[str | None]) -> str:
    """Replace ``{metric/@n}`` with the id of the metric matched for entry n."""

    def _sub(match: re.Match) -> str:
        index = int(match.group(1))
        metric_id = created_ids[index] if index < len(created_ids) else None
        return f"{{metric/{metric_id}}}" if metric_id else match.group(0)

    return _PLACEHOLDER_RE.sub(_sub, maql)


def first_proposed_maql(texts: list[str]) -> str | None:
    """The MAQL of the first formula the agent showed in a code span or a fenced block, if any."""
    for text in texts:
        found = _PROPOSED_MAQL_RE.search(text or "")
        if found:
            return (found.group(1) or found.group(2)).strip()
    return None


def missing_mentions(mentions: tuple[str, ...], texts: list[str]) -> list[str]:
    """The expected mentions no agent reply names, compared case-insensitively."""
    joined = _norm_text(" ".join(texts))
    return [m for m in mentions if _norm_text(m) not in joined]
