# (C) 2026 GoodData Corporation. All rights reserved.
"""The KDA item's field checks: what ``create_key_driver_analysis`` and its execution must match.

An item opts in with ``check_fields: true``. Its expected output then names the measure, the date
attribute, both periods, the non-date filters and the summary the execution must return. Without
the key, nothing here runs and the item is scored on completion only.

``any_of`` lists complete alternatives. Each option replaces some fields of the item, and a run
passes when one option matches every field. The summary goes with the date attribute, so an
option that changes one usually states both.
"""

from __future__ import annotations

import json
import math
import re
from collections.abc import Mapping
from dataclasses import dataclass
from decimal import Decimal
from typing import Any

# The fields in the order they are checked and published. Score ``kda_<field>_correct`` each.
KDA_FIELDS = ("measure", "date_attribute", "analyzed_period", "reference_period", "filters", "summary")
KDA_FIELD_SCORES = tuple(f"kda_{name}_correct" for name in KDA_FIELDS)

_FIELD_KEYS = {
    "measure": "Measure",
    "date_attribute": "Date Attribute",
    "analyzed_period": "Analyzed Period",
    "reference_period": "Reference Period",
    "filters": "Filters",
    "summary": "Summary",
}
_OPTION_KEYS = frozenset(_FIELD_KEYS.values())
_ITEM_KEYS = _OPTION_KEYS | {"check_fields", "any_of"}
_SUMMARY_VALUES = ("analyzed_value", "reference_value", "change")
_SUMMARY_KEYS = frozenset({*_SUMMARY_VALUES, "absolute_tolerance"})
_DEFAULT_TOLERANCE = 0.01
_MEASURE_KEYS = frozenset({"id", "type", "aggregation"})
# The values create_key_driver_analysis accepts. It upper-cases the aggregation itself.
_MEASURE_TYPES = ("metric", "fact", "attribute")
_AGGREGATIONS = ("SUM", "AVG", "MIN", "MAX", "MEDIAN", "COUNT")
_FILTER_STATES = ("include", "exclude")
# Spelled like the item's other keys, these would leave the checks off without a word.
_OPT_IN_KEYS = ("check_fields", "any_of")
_DATE_FILTER = "date_filter"
# The agent's tools take an attribute by its label or its attribute id. Both ids are equal in the
# eval workspaces, so a filter is matched on the id alone.
_TYPE_PREFIXES = ("label/", "attribute/")


@dataclass(frozen=True)
class KdaFieldOption:
    """One complete set of expected fields."""

    measures: tuple[dict[str, Any], ...]
    date_attribute: str
    analyzed_period: str
    reference_period: str
    filters: tuple[Any, ...]
    filter_entries: tuple[dict[str, Any], ...]
    summary: dict[str, float]
    tolerance: float


@dataclass(frozen=True)
class KdaExpectation:
    """The item's field checks. ``options`` is empty when the item does not opt in."""

    options: tuple[KdaFieldOption, ...] = ()

    @property
    def check_fields(self) -> bool:
        return bool(self.options)


@dataclass(frozen=True)
class KdaFieldResult:
    """The fields of one run, checked against the option that matched most of them."""

    checks: dict[str, bool]
    option_index: int
    expected: dict[str, Any]
    actual: dict[str, Any]

    @property
    def passed(self) -> bool:
        return all(self.checks.values())


def _to_float(value: Any) -> float | None:
    """A finite number from an int, float or numeric string, else None. A bool is not a number."""
    if isinstance(value, bool) or value is None:
        return None
    try:
        number = float(str(value))
    except ValueError:
        return None
    return number if math.isfinite(number) else None


def _measures(value: Any) -> tuple[dict[str, Any], ...]:
    candidates = value if isinstance(value, list) else [value]
    if not candidates:
        raise ValueError("Measure must name at least one candidate")
    for candidate in candidates:
        if not isinstance(candidate, dict) or not isinstance(candidate.get("id"), str) or not candidate["id"]:
            raise ValueError(f"Measure candidate needs a non-empty string id, got {candidate!r}")
        if candidate.get("type") not in _MEASURE_TYPES:
            raise ValueError(f"Measure candidate type must be one of {', '.join(_MEASURE_TYPES)}, got {candidate!r}")
        aggregation = candidate.get("aggregation")
        if aggregation is not None and str(aggregation).upper() not in _AGGREGATIONS:
            raise ValueError(f"Measure aggregation must be one of {', '.join(_AGGREGATIONS)}, got {candidate!r}")
        if unknown := set(candidate) - _MEASURE_KEYS:
            raise ValueError(f"Measure candidate has unknown keys {sorted(unknown)}, got {candidate!r}")
    return tuple(candidates)


def _text(key: str, value: Any, *, allow_int: bool = False) -> str:
    # A year period may be an int ("Analyzed Period": 2024); a date attribute id never is, and a bool is neither.
    allowed = (str, int) if allow_int else str
    if isinstance(value, bool) or not isinstance(value, allowed) or not str(value).strip():
        raise ValueError(f"{key} must be a non-empty string, got {value!r}")
    return str(value).strip()


def _period_key(value: Any) -> tuple[int | str, ...]:
    """A period by its parts, numbers as numbers: the tool reads ``2024-1`` and ``2024-01`` as one month."""
    return tuple(int(part) if part.isdigit() else part for part in re.split(r"[-\s:]+", str(value).strip()))


def _check_attribute_filter(entry: dict[str, Any]) -> None:
    using, state = entry.get("using"), entry.get("state")
    if not isinstance(using, str) or not using.strip():
        raise ValueError(f"attribute_filter needs a non-empty using, got {entry!r}")
    if not isinstance(state, dict) or len(state) != 1 or next(iter(state)) not in _FILTER_STATES:
        raise ValueError(f"attribute_filter state needs exactly one of include, exclude, got {entry!r}")
    values = next(iter(state.values()))
    if not isinstance(values, list) or not values or not all(isinstance(v, str) for v in values):
        raise ValueError(f"attribute_filter {next(iter(state))} must be a non-empty list of strings, got {entry!r}")


def _filters(value: Any) -> tuple[Any, ...]:
    if not isinstance(value, list):
        raise ValueError(f"Filters must be a list, [] for none, got {value!r}")
    for entry in value:
        if not isinstance(entry, dict):
            raise ValueError(f"Filters must hold objects, got {entry!r}")
        if entry.get("type") == _DATE_FILTER:
            raise ValueError("Filters must not hold a date_filter: date filters are not checked, the periods are")
        if entry.get("type") == "attribute_filter":
            _check_attribute_filter(entry)
    return tuple(_filter_key(entry) for entry in value)


def _summary(value: Any) -> tuple[dict[str, float], float]:
    if not isinstance(value, dict):
        raise ValueError(f"Summary must be an object, got {value!r}")
    if unknown := set(value) - _SUMMARY_KEYS:
        raise ValueError(f"Summary has unknown keys {sorted(unknown)}")
    numbers: dict[str, float] = {}
    for key in _SUMMARY_VALUES:
        if key in value:
            number = _to_float(value[key])
            if number is None:
                raise ValueError(f"Summary {key} must be a number, got {value[key]!r}")
            numbers[key] = number
    if not numbers:
        raise ValueError(f"Summary must state at least one of {', '.join(_SUMMARY_VALUES)}")
    tolerance = _to_float(value.get("absolute_tolerance", _DEFAULT_TOLERANCE))
    if tolerance is None or tolerance < 0:
        raise ValueError(f"Summary absolute_tolerance must be a number >= 0, got {value.get('absolute_tolerance')!r}")
    return numbers, tolerance


def _option(fields: Mapping[str, Any], label: str) -> KdaFieldOption:
    if missing := [key for key in _FIELD_KEYS.values() if key not in fields]:
        raise ValueError(f"{label} lacks {', '.join(missing)}: check_fields needs every field, Filters [] for none")
    summary, tolerance = _summary(fields["Summary"])
    return KdaFieldOption(
        measures=_measures(fields["Measure"]),
        date_attribute=_text("Date Attribute", fields["Date Attribute"]),
        analyzed_period=_text("Analyzed Period", fields["Analyzed Period"], allow_int=True),
        reference_period=_text("Reference Period", fields["Reference Period"], allow_int=True),
        filters=_filters(fields["Filters"]),
        filter_entries=tuple(fields["Filters"]),
        summary=summary,
        tolerance=tolerance,
    )


def _reject_respelt_keys(expected: dict[str, Any]) -> None:
    for key in expected:
        canonical = re.sub(r"[\s-]+", "_", key.strip()).lower() if isinstance(key, str) else key
        if canonical in _OPT_IN_KEYS and key != canonical:
            raise ValueError(f"write {canonical!r}, not {key!r}")


def parse_kda_expectation(expected: Any) -> KdaExpectation:
    """Read the item's field checks, raising ValueError on a malformed one before any request is sent."""
    if isinstance(expected, dict):
        _reject_respelt_keys(expected)
    if not isinstance(expected, dict) or "check_fields" not in expected:
        if isinstance(expected, dict) and "any_of" in expected:
            raise ValueError("any_of is read only with check_fields: true")
        return KdaExpectation()
    flag = expected["check_fields"]
    if not isinstance(flag, bool):
        raise ValueError(f"check_fields must be true or false, got {flag!r}")
    if not flag:
        if "any_of" in expected:
            raise ValueError("any_of is read only with check_fields: true")
        return KdaExpectation()
    if unknown := set(expected) - _ITEM_KEYS:
        raise ValueError(f"expected_output has unknown keys {sorted(unknown)}")
    base = {key: value for key, value in expected.items() if key in _OPTION_KEYS}
    if "any_of" not in expected:
        return KdaExpectation(options=(_option(base, "expected_output"),))
    options = expected["any_of"]
    if not isinstance(options, list) or len(options) < 2 or not all(isinstance(o, dict) and o for o in options):
        raise ValueError(f"any_of must list at least two non-empty objects, got {options!r}")
    parsed: list[KdaFieldOption] = []
    for index, option in enumerate(options):
        if unknown := set(option) - _OPTION_KEYS:
            raise ValueError(
                f"any_of[{index}] has keys {sorted(unknown)}; an option may state only {sorted(_OPTION_KEYS)}"
            )
        parsed.append(_option({**base, **option}, f"any_of[{index}]"))
    return KdaExpectation(options=tuple(parsed))


def _bare_id(using: Any) -> Any:
    if isinstance(using, str):
        for prefix in _TYPE_PREFIXES:
            if using.startswith(prefix):
                return using[len(prefix) :]
    return using


def _filter_key(entry: dict[str, Any]) -> Any:
    """A comparable form of one filter: an attribute filter by its id and values, any other as its JSON."""
    state = entry.get("state")
    if (
        entry.get("type") == "attribute_filter"
        and isinstance(state, dict)
        and set(state) <= set(_FILTER_STATES)
        and all(isinstance(values, list) and all(isinstance(v, str) for v in values) for values in state.values())
    ):
        return (
            "attribute_filter",
            _bare_id(entry.get("using")),
            tuple(sorted(state.get("include") or [])),
            tuple(sorted(state.get("exclude") or [])),
        )
    return json.dumps(entry, sort_keys=True, default=str)


def _measure_matches(candidate: dict[str, Any], actual: Any) -> bool:
    if not isinstance(actual, dict):
        return False
    if candidate["id"] != actual.get("id") or candidate["type"] != actual.get("type"):
        return False
    expected_aggregation = candidate.get("aggregation")
    if expected_aggregation is None:
        return True
    return str(expected_aggregation).upper() == str(actual.get("aggregation") or "").upper()


def _actual_summary(execute_result: Any) -> dict | None:
    if not isinstance(execute_result, dict) or execute_result.get("success") is not True:
        return None
    data = execute_result.get("data")
    summary = data.get("summary") if isinstance(data, dict) else None
    return summary if isinstance(summary, dict) else None


def _within(actual: float, expected: float, tolerance: float) -> bool:
    # In decimal, so 100.01 against 100 is a difference of exactly 0.01, not 0.010000000000005116.
    return abs(Decimal(repr(actual)) - Decimal(repr(expected))) <= Decimal(repr(tolerance))


def _summary_matches(option: KdaFieldOption, actual: dict | None) -> bool:
    if actual is None:
        return False
    for key, expected in option.summary.items():
        number = _to_float(actual.get(key))
        if number is None or not _within(number, expected, option.tolerance):
            return False
    return True


def _non_date_filters(filters: Any) -> list[Any]:
    entries = filters if isinstance(filters, list) else []
    return [entry for entry in entries if not (isinstance(entry, dict) and entry.get("type") == _DATE_FILTER)]


def _actual_filters(create_args: dict) -> Any:
    """The non-date filters the agent sent, or the malformed value itself so a failed check shows it."""
    filters = create_args.get("filters", [])
    return _non_date_filters(filters) if isinstance(filters, list) else filters


def _check_option(option: KdaFieldOption, create_args: dict, summary: dict | None) -> dict[str, bool]:
    filters = create_args.get("filters", [])
    # Omitted filters are no filters. Anything but a list, null included, is malformed: the tool takes a list.
    filters_shaped = isinstance(filters, list)
    actual_filters = sorted(
        (_filter_key(f) if isinstance(f, dict) else repr(f) for f in _non_date_filters(filters)),
        key=repr,
    )
    return {
        "measure": any(_measure_matches(c, create_args.get("measure")) for c in option.measures),
        "date_attribute": str(create_args.get("date_attribute_id") or "").strip() == option.date_attribute,
        "analyzed_period": _period_key(create_args.get("analyzed_period") or "") == _period_key(option.analyzed_period),
        "reference_period": _period_key(create_args.get("reference_period") or "")
        == _period_key(option.reference_period),
        "filters": filters_shaped and actual_filters == sorted(option.filters, key=repr),
        "summary": _summary_matches(option, summary),
    }


def _expected_view(option: KdaFieldOption) -> dict[str, Any]:
    return {
        "measure": list(option.measures) if len(option.measures) > 1 else option.measures[0],
        "date_attribute": option.date_attribute,
        "analyzed_period": option.analyzed_period,
        "reference_period": option.reference_period,
        "filters": list(option.filter_entries),
        "summary": {**option.summary, "absolute_tolerance": option.tolerance},
    }


def check_kda_fields(spec: KdaExpectation, create_args: Any, execute_result: Any) -> KdaFieldResult | None:
    """The run's field checks against the option that matched most fields, the first one on a tie.

    None when the item does not opt in or the run never called create: there was nothing to check, and
    the completion checks already fail that run. Arguments that are not an object fail every field.
    """
    if not spec.check_fields or create_args is None:
        return None
    summary = _actual_summary(execute_result)
    if not isinstance(create_args, dict):
        return KdaFieldResult(
            checks=dict.fromkeys(KDA_FIELDS, False),
            option_index=0,
            expected=_expected_view(spec.options[0]),
            actual=dict.fromkeys(KDA_FIELDS) | {"summary": summary},
        )
    results = [_check_option(option, create_args, summary) for option in spec.options]
    best = max(range(len(results)), key=lambda i: sum(results[i].values()))
    actual = {
        "measure": create_args.get("measure"),
        "date_attribute": create_args.get("date_attribute_id"),
        "analyzed_period": create_args.get("analyzed_period"),
        "reference_period": create_args.get("reference_period"),
        "filters": _actual_filters(create_args),
        "summary": summary,
    }
    return KdaFieldResult(
        checks=results[best],
        option_index=best,
        expected=_expected_view(spec.options[best]),
        actual=actual,
    )
