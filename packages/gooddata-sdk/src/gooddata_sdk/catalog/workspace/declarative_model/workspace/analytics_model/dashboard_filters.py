# (C) 2026 GoodData Corporation
from __future__ import annotations

from typing import Any, Literal, Union

import attrs
from cattrs import global_converter, structure
from gooddata_api_client.model.dashboard_compound_comparison_condition import DashboardCompoundComparisonCondition
from gooddata_api_client.model.dashboard_compound_range_condition import DashboardCompoundRangeCondition
from gooddata_api_client.model.dashboard_measure_value_filter import DashboardMeasureValueFilter
from gooddata_api_client.model.dashboard_measure_value_filter_measure_value_filter import (
    DashboardMeasureValueFilterMeasureValueFilter,
)

from gooddata_sdk.catalog.base import Base

ComparisonOperator = Literal[
    "GREATER_THAN",
    "GREATER_THAN_OR_EQUAL_TO",
    "LESS_THAN",
    "LESS_THAN_OR_EQUAL_TO",
    "EQUAL_TO",
    "NOT_EQUAL_TO",
]

RangeOperator = Literal["BETWEEN", "NOT_BETWEEN"]


@attrs.define(kw_only=True)
class CatalogDashboardCompoundComparisonCondition(Base):
    """Comparison condition for a dashboard measure value filter.

    Filters dashboard data where the measure satisfies a comparison
    relation (e.g. greater than, equal to) against a single value.
    """

    operator: str
    value: float

    @staticmethod
    def client_class() -> type[DashboardCompoundComparisonCondition]:
        return DashboardCompoundComparisonCondition

    def to_api(self) -> DashboardCompoundComparisonCondition:
        return DashboardCompoundComparisonCondition(
            operator=self.operator,
            value=self.value,
            _check_type=False,
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDashboardCompoundComparisonCondition:
        return cls(
            operator=entity["operator"],
            value=float(entity["value"]),
        )


@attrs.define(kw_only=True)
class CatalogDashboardCompoundRangeCondition(Base):
    """Range condition for a dashboard measure value filter.

    Filters dashboard data where the measure falls within (or outside)
    a numeric range defined by ``from_value`` and ``to``.
    """

    from_value: float
    operator: str
    to: float

    @staticmethod
    def client_class() -> type[DashboardCompoundRangeCondition]:
        return DashboardCompoundRangeCondition

    def to_api(self) -> DashboardCompoundRangeCondition:
        return DashboardCompoundRangeCondition(
            _from=self.from_value,
            operator=self.operator,
            to=self.to,
            _check_type=False,
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDashboardCompoundRangeCondition:
        # The JSON key is "from"; the API client Python attribute is "_from";
        # after to_dict() it appears as "from" (camelCase=True) or "_from" (camelCase=False).
        from_val = entity.get("from_value") or entity.get("from") or entity.get("_from")
        return cls(
            from_value=float(from_val),
            operator=entity["operator"],
            to=float(entity["to"]),
        )


# Union type alias used as the element type for ``conditions``.
CatalogDashboardCompoundConditionItem = Union[
    CatalogDashboardCompoundComparisonCondition,
    CatalogDashboardCompoundRangeCondition,
]


def _structure_condition_item(v: dict[str, Any], _: Any) -> CatalogDashboardCompoundConditionItem:
    """Discriminate between comparison and range conditions.

    Comparison conditions carry a ``value`` key; range conditions carry
    ``from`` / ``_from`` / ``from_value`` instead.
    """
    if "value" in v:
        return structure(v, CatalogDashboardCompoundComparisonCondition)
    return structure(v, CatalogDashboardCompoundRangeCondition)


global_converter.register_structure_hook(
    CatalogDashboardCompoundConditionItem,  # type: ignore[arg-type]
    _structure_condition_item,
)


@attrs.define(kw_only=True)
class CatalogDashboardMeasureValueFilterBody(Base):
    """Inner body of a :class:`CatalogDashboardMeasureValueFilter`.

    Attributes:
        conditions: One or more compound conditions (comparison or range).
            Multiple conditions are combined with OR logic.
        measure: IdentifierRef dict pointing to the measure to filter on,
            e.g. ``{"identifier": {"id": "metric/revenue", "type": "metric"}}``.
        local_identifier: Optional local identifier for the filter within
            a dashboard layout.
        title: Optional human-readable label for the filter.
    """

    conditions: list[CatalogDashboardCompoundConditionItem]
    measure: dict[str, Any]
    local_identifier: str | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> type[DashboardMeasureValueFilterMeasureValueFilter]:
        return DashboardMeasureValueFilterMeasureValueFilter

    def to_api(self) -> DashboardMeasureValueFilterMeasureValueFilter:
        kwargs: dict[str, Any] = {}
        if self.local_identifier is not None:
            kwargs["local_identifier"] = self.local_identifier
        if self.title is not None:
            kwargs["title"] = self.title
        return DashboardMeasureValueFilterMeasureValueFilter(
            conditions=[c.to_api() for c in self.conditions],
            measure=self.measure,
            _check_type=False,
            **kwargs,
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDashboardMeasureValueFilterBody:
        local_id = entity.get("local_identifier") or entity.get("localIdentifier")
        return cls(
            conditions=[_condition_item_from_dict(c) for c in entity.get("conditions", [])],
            measure=entity["measure"],
            local_identifier=local_id,
            title=entity.get("title"),
        )


def _condition_item_from_dict(v: dict[str, Any]) -> CatalogDashboardCompoundConditionItem:
    """Construct the correct condition subtype from a plain dict."""
    if "value" in v:
        return CatalogDashboardCompoundComparisonCondition(
            operator=v["operator"],
            value=float(v["value"]),
        )
    from_val = v.get("from_value") or v.get("from") or v.get("_from")
    return CatalogDashboardCompoundRangeCondition(
        from_value=float(from_val),
        operator=v["operator"],
        to=float(v["to"]),
    )


@attrs.define(kw_only=True)
class CatalogDashboardMeasureValueFilter(Base):
    """Dashboard filter that restricts visible data by a measure's value.

    This filter type can appear as an element of
    ``DashboardFilter.oneOf`` and may be used in dashboard filter
    contexts or as a filter override in tabular dashboard exports.

    Example::

        from gooddata_sdk import (
            CatalogDashboardCompoundComparisonCondition,
            CatalogDashboardMeasureValueFilter,
            CatalogDashboardMeasureValueFilterBody,
        )

        mvf = CatalogDashboardMeasureValueFilter(
            measure_value_filter=CatalogDashboardMeasureValueFilterBody(
                conditions=[
                    CatalogDashboardCompoundComparisonCondition(
                        operator="GREATER_THAN",
                        value=1000.0,
                    )
                ],
                measure={"identifier": {"id": "metric/revenue", "type": "metric"}},
                title="Revenue > 1 000",
            )
        )
    """

    measure_value_filter: CatalogDashboardMeasureValueFilterBody

    @staticmethod
    def client_class() -> type[DashboardMeasureValueFilter]:
        return DashboardMeasureValueFilter

    def to_api(self) -> DashboardMeasureValueFilter:
        return DashboardMeasureValueFilter(
            measure_value_filter=self.measure_value_filter.to_api(),
            _check_type=False,
        )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDashboardMeasureValueFilter:
        # Accept both camelCase (from live API) and snake_case (from to_dict round-trip).
        raw_body = entity.get("measure_value_filter") or entity.get("measureValueFilter")
        return cls(measure_value_filter=CatalogDashboardMeasureValueFilterBody.from_api(raw_body))
