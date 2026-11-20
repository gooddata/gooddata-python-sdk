# (C) 2026 GoodData Corporation. All rights reserved.
"""The search-tool item: the expected ``search_objects`` arguments plus the checks an item opts into.

An item that carries only ``tool_call``, or reaches the runner as the bare arguments, is scored on
``tool_selection`` (gating) and ``tool_correctness`` (informing). Each other key adds one check, and a
key the module does not know is rejected, so a misspelt check cannot read as a pass.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any

from gooddata_eval.core.models import ChatResult, ToolCallEvent

SEARCH_TOOL = "search_objects"

# The keys of an item's expected output beside ``tool_call``. Public so a caller holding a raw item can
# tell the options shape from bare arguments.
SEARCH_OPTION_KEYS = frozenset(
    {
        "expected_objects",
        "expect_widget",
        "required_tools",
        "forbidden_tools",
        "search_required",
        "answer_rubric",
        "expected_limit",
        "no_raw_ids",
        "setup_turns",
        "report_only",
    }
)
_KNOWN_KEYS = SEARCH_OPTION_KEYS | {"tool_call"}
# The search_objects parameters, and emit_widget, the old name of user_requested_search. An expected output with
# any other key is read as an item, so a misspelt check key fails it instead of passing as an argument.
SEARCH_ARGUMENT_KEYS = frozenset(
    {"keywords", "object_types", "limit", "compatible_with_afm", "kda_eligible", "user_requested_search", "emit_widget"}
)

_OBJECT_TYPES = frozenset(
    {
        "metric",
        "fact",
        "attribute",
        "label",
        "date_attribute",
        "computed_attribute",
        "dataset",
        "date",
        "parameter",
        "visualization",
        "dashboard",
        "document",
        "report",
    }
)
# The agent's tools take an attribute by either of its ids, and search returns a date attribute with
# ``type`` attribute and ``final_type`` date_attribute, so these spellings name one object.
_ATTRIBUTE_TYPES = frozenset({"attribute", "label", "date_attribute"})

# A ``{type/id}`` chip is the UI's own syntax for a named object and renders as its title, also inside
# inline code. An id outside a chip reaches the user as raw text.
_CHIP = re.compile(r"\{[a-z_]+/[^{}\s]+\}")
_UUID = re.compile(r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.IGNORECASE)
_TYPED_ID = re.compile(rf"\b(?:{'|'.join(sorted(_OBJECT_TYPES))})/([A-Za-z0-9_](?:[A-Za-z0-9_.-]*[A-Za-z0-9_])?)")
# Prose pairs type words with a slash ("date/time", "label/value pairs"). Only an id with an underscore,
# a dot or a digit, as the workspace ids have, counts. A one-word id such as metric/revenue is not caught.
_ID_MARK = re.compile(r"[_.0-9]")


@dataclass(frozen=True)
class SearchExpectation:
    """What one item expects. Every field but ``tool_args`` is an opt-in check.

    ``setup_turns`` should only read the workspace (search, describe, an unsaved chart). The CLI runs an item with
    setup turns in its serial phase, so a write cannot race another item, but nothing removes what it writes.
    """

    tool_args: dict[str, Any] = field(default_factory=dict)
    expected_objects: tuple[str, ...] = ()
    expect_widget: bool | None = None
    required_tools: tuple[str, ...] = ()
    forbidden_tools: tuple[str, ...] = ()
    search_required: bool = True
    answer_rubric: tuple[str, ...] = ()
    expected_limit: int | None = None
    no_raw_ids: bool = False
    setup_turns: tuple[str, ...] = ()
    report_only: bool = False

    @property
    def has_turn_checks(self) -> bool:
        """Whether the item opts into a check of the scored turn. Each one is published as a score of its own."""
        return bool(
            self.expected_objects
            or self.expect_widget is not None
            or self.required_tools
            or self.forbidden_tools
            or self.answer_rubric
            or self.expected_limit is not None
            or self.no_raw_ids
        )

    @property
    def has_checks(self) -> bool:
        """Whether the item opts into anything beyond ``tool_selection`` and ``tool_correctness``."""
        return self.has_turn_checks or bool(self.setup_turns) or not self.search_required


def _string_list(key: str, value: Any) -> tuple[str, ...]:
    # isinstance, not str(entry): an unquoted YAML `no` loads as False and would turn into the text "False".
    if not isinstance(value, list) or not value:
        raise ValueError(f"{key} must be a non-empty list of strings, got {value!r}")
    if any(not isinstance(entry, str) or not entry.strip() for entry in value):
        raise ValueError(f"{key} must hold non-empty strings only, got {value!r}")
    return tuple(value)


def _flag(key: str, value: Any) -> bool:
    if not isinstance(value, bool):
        raise ValueError(f"{key} must be true or false, got {value!r}")
    return value


def _object_ref(ref: str) -> tuple[str, str]:
    object_type, sep, object_id = ref.partition("/")
    if not sep or object_type not in _OBJECT_TYPES or not object_id or object_id != object_id.strip():
        raise ValueError(f"expected_objects entry must be '<type>/<id>' with a known type, got {ref!r}")
    return object_type, object_id


def _tool_args(tool_call: Any) -> dict[str, Any]:
    if not isinstance(tool_call, dict):
        raise ValueError(f"tool_call must be an object, got {tool_call!r}")
    name = tool_call.get("function_name")
    if name is not None and name != SEARCH_TOOL:
        raise ValueError(f"tool_call.function_name must be {SEARCH_TOOL!r}, got {name!r}")
    return check_arguments(tool_call.get("function_arguments", {}))


def check_arguments(args: Any) -> dict[str, Any]:
    """The expected ``search_objects`` arguments, whichever way the item gives them.

    Raises:
        ValueError: The arguments are not an object, or ``compatible_with_afm`` is not lists of objects.
    """
    if not isinstance(args, dict):
        raise ValueError(f"tool_call.function_arguments must be an object, got {args!r}")
    afm = args.get("compatible_with_afm")
    if afm is not None and (
        not isinstance(afm, dict)
        or not set(afm) <= {"measures", "attributes"}
        or any(value is not None and not isinstance(value, list) for value in afm.values())
        or any(not isinstance(item, dict) for value in afm.values() for item in value or [])
    ):
        raise ValueError(f"compatible_with_afm must hold lists of measure and attribute objects, got {afm!r}")
    return dict(args)


def parse_expectation(expected_output: Any) -> SearchExpectation:
    """Read an item's whole expected output.

    Raises:
        ValueError: The expected output is not an object, names an unknown key, or holds a value the
            run could not score. Raised before any request is sent.
    """
    if not isinstance(expected_output, dict):
        raise ValueError(f"expected_output must be an object, got {expected_output!r}")
    unknown = sorted(set(expected_output) - _KNOWN_KEYS)
    if unknown:
        raise ValueError(f"expected_output has unknown keys {unknown}; known keys are {sorted(_KNOWN_KEYS)}")
    raw = expected_output
    tool_args = _tool_args(raw["tool_call"]) if "tool_call" in raw else {}

    expected_objects: tuple[str, ...] = ()
    if "expected_objects" in raw:
        expected_objects = _string_list("expected_objects", raw["expected_objects"])
        for ref in expected_objects:
            _object_ref(ref)
    required = _string_list("required_tools", raw["required_tools"]) if "required_tools" in raw else ()
    forbidden = _string_list("forbidden_tools", raw["forbidden_tools"]) if "forbidden_tools" in raw else ()
    both = sorted(set(required) & set(forbidden))
    if both:
        raise ValueError(f"tools {both} are both required and forbidden")
    limit = raw.get("expected_limit")
    if "expected_limit" in raw and (not isinstance(limit, int) or isinstance(limit, bool) or limit < 1):
        raise ValueError(f"expected_limit must be a positive integer, got {limit!r}")

    spec = SearchExpectation(
        tool_args=tool_args,
        expected_objects=expected_objects,
        expect_widget=_flag("expect_widget", raw["expect_widget"]) if "expect_widget" in raw else None,
        required_tools=required,
        forbidden_tools=forbidden,
        search_required=_flag("search_required", raw["search_required"]) if "search_required" in raw else True,
        answer_rubric=_string_list("answer_rubric", raw["answer_rubric"]) if "answer_rubric" in raw else (),
        expected_limit=limit,
        no_raw_ids=_flag("no_raw_ids", raw["no_raw_ids"]) if "no_raw_ids" in raw else False,
        setup_turns=_string_list("setup_turns", raw["setup_turns"]) if "setup_turns" in raw else (),
        report_only=_flag("report_only", raw["report_only"]) if "report_only" in raw else False,
    )
    if "tool_call" not in raw and not spec.has_checks:
        raise ValueError("expected_output asserts nothing: give tool_call or at least one check")
    # tool_correctness only informs, so without tool_selection's gate a check of the turn is all that can fail a run.
    if not spec.search_required and not spec.has_turn_checks:
        raise ValueError(
            "search_required: false needs a check of the scored turn (such as expect_widget or forbidden_tools), "
            "or the item passes whatever the agent does"
        )
    if spec.report_only and not spec.has_turn_checks:
        raise ValueError("report_only has no check to report")
    return spec


def _ref_key(object_type: str, object_id: str) -> tuple[str, str]:
    return ("attribute" if object_type in _ATTRIBUTE_TYPES else object_type, object_id)


def call_args(tc: ToolCallEvent) -> dict[str, Any]:
    """The call's arguments, or {} when they are missing or not a JSON object."""
    args = tc.parsed_arguments()
    return args if isinstance(args, dict) else {}


def search_calls(events: list[ToolCallEvent]) -> list[ToolCallEvent]:
    """The turn's ``search_objects`` calls, in order."""
    return [tc for tc in events if tc.function_name == SEARCH_TOOL]


def _objects(container: Any) -> list[dict]:
    """The object entries of a search result or widget part; none when its shape is not the expected one."""
    objects = container.get("objects") if isinstance(container, dict) else None
    return [obj for obj in objects if isinstance(obj, dict)] if isinstance(objects, list) else []


def returned_refs(result: ChatResult) -> list[str]:
    """Every object the turn's searches returned, as ``type/id``, first sighting first.

    Read from the ``search_objects`` results and from the ``searchResults`` widget parts: a search
    the agent runs for itself shows no widget, so its result is the only place its objects appear.
    """
    refs: dict[tuple[str, str], str] = {}

    def _add(object_type: Any, object_id: Any) -> None:
        if isinstance(object_type, str) and isinstance(object_id, str) and object_type and object_id:
            refs.setdefault(_ref_key(object_type, object_id), f"{object_type}/{object_id}")

    for tc in search_calls(result.tool_call_events or []):
        for obj in _objects(tc.parsed_result()):
            _add(obj.get("final_type") or obj.get("type"), obj.get("id"))
    for part in result.search_results:
        for obj in _objects(part):
            _add(obj.get("type"), obj.get("id"))
    return list(refs.values())


def _key_of(ref: str) -> tuple[str, str]:
    object_type, _, object_id = ref.partition("/")
    return _ref_key(object_type, object_id)


def missing_objects(expected: tuple[str, ...], returned: list[str]) -> list[str]:
    """The expected refs no search returned. Every one must be found, not any one."""
    found = {_key_of(ref) for ref in returned}
    return [ref for ref in expected if _key_of(ref) not in found]


def raw_ids(text: str) -> list[str]:
    """The UUIDs and ``type/id`` spellings in ``text`` that sit outside a ``{type/id}`` chip."""
    outside = _CHIP.sub(" ", text)
    typed = [m.group(0) for m in _TYPED_ID.finditer(outside) if _ID_MARK.search(m.group(1))]
    return _UUID.findall(outside) + typed


def deterministic_checks(spec: SearchExpectation, result: ChatResult) -> tuple[dict[str, bool], dict[str, Any]]:
    """The checks of one scored turn that need no judge, with the evidence of each failure."""
    checks: dict[str, bool] = {}
    details: dict[str, Any] = {}

    def _check(name: str, ok: bool, why: Any) -> None:
        checks[name] = ok
        if not ok:
            details[name] = why

    events = result.tool_call_events or []
    if spec.expected_objects:
        returned = returned_refs(result)
        missing = missing_objects(spec.expected_objects, returned)
        _check("search_expected_objects", not missing, {"missing": missing, "returned": returned[:30]})
    if spec.expect_widget is not None:
        parts = len(result.search_results)
        _check("search_widget", (parts > 0) == spec.expect_widget, {"expected": spec.expect_widget, "parts": parts})
    if spec.required_tools or spec.forbidden_tools:
        called = [tc.function_name for tc in events]
        not_called = [name for name in spec.required_tools if name not in called]
        forbidden = [name for name in spec.forbidden_tools if name in called]
        _check(
            "search_routing",
            not not_called and not forbidden,
            {"not_called": not_called, "forbidden_called": forbidden, "called": called},
        )
    if spec.expected_limit is not None:
        limits = [call_args(tc).get("limit") for tc in search_calls(events)]
        _check("search_limit", spec.expected_limit in limits, {"expected": spec.expected_limit, "limits": limits})
    if spec.no_raw_ids:
        found = raw_ids(result.text_response or "")
        _check("search_no_raw_ids", not found, {"raw_ids": found})
    return checks, details
