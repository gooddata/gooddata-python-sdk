# (C) 2024 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Literal

import attrs
from gooddata_api_client.model.dashboard_arbitrary_attribute_filter_arbitrary_attribute_filter import (
    DashboardArbitraryAttributeFilterArbitraryAttributeFilter,
)
from gooddata_api_client.model.dashboard_match_attribute_filter_match_attribute_filter import (
    DashboardMatchAttributeFilterMatchAttributeFilter,
)

from gooddata_sdk.catalog.base import Base

DashboardMatchOperator = Literal["contains", "startsWith", "endsWith"]


@attrs.define(kw_only=True)
class CatalogDashboardArbitraryAttributeFilter(Base):
    """SDK wrapper for the body of DashboardArbitraryAttributeFilter.

    Represents a free-form attribute filter for dashboard filter overrides.
    The ``display_form`` field should be an ``IdentifierRef`` dict, e.g.::

        {"identifier": {"id": "label.my_label", "type": "label"}}

    To build a dashboard filter override dict, wrap the result of
    :meth:`to_dict` in the outer key::

        {"arbitrary_attribute_filter": filter.to_dict(camel_case=False)}

    Attributes:
        display_form: IdentifierRef dict identifying the display form.
        negative_selection: When ``True``, the filter excludes the listed values.
        values: List of string values to filter on.
        local_identifier: Optional local identifier for the filter.
        title: Optional human-readable title.
    """

    display_form: dict
    negative_selection: bool
    values: list[str] = attrs.field(factory=list)
    local_identifier: str | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DashboardArbitraryAttributeFilterArbitraryAttributeFilter]:
        return DashboardArbitraryAttributeFilterArbitraryAttributeFilter


@attrs.define(kw_only=True)
class CatalogDashboardMatchAttributeFilter(Base):
    """SDK wrapper for the body of DashboardMatchAttributeFilter.

    Represents a string-match attribute filter for dashboard filter overrides.
    The ``display_form`` field should be an ``IdentifierRef`` dict, e.g.::

        {"identifier": {"id": "label.my_label", "type": "label"}}

    To build a dashboard filter override dict, wrap the result of
    :meth:`to_dict` in the outer key::

        {"match_attribute_filter": filter.to_dict(camel_case=False)}

    Attributes:
        display_form: IdentifierRef dict identifying the display form.
        case_sensitive: When ``True``, the string match is case-sensitive.
        literal: The string literal to match against.
        negative_selection: When ``True``, the filter excludes matches.
        operator: Match operator – one of ``"contains"``, ``"startsWith"``, ``"endsWith"``.
        local_identifier: Optional local identifier for the filter.
        title: Optional human-readable title.
    """

    display_form: dict
    case_sensitive: bool
    literal: str
    negative_selection: bool
    operator: DashboardMatchOperator
    local_identifier: str | None = None
    title: str | None = None

    @staticmethod
    def client_class() -> builtins.type[DashboardMatchAttributeFilterMatchAttributeFilter]:
        return DashboardMatchAttributeFilterMatchAttributeFilter
