# (C) 2026 GoodData Corporation
"""Unit test: analytics-layer ``parameters`` survive the declarative round-trip.

Regression test. The ``parameters`` field on ``CatalogDeclarativeAnalyticsLayer``
was bound to the data-source ``CatalogParameter`` ({name, value}) instead of a
declarative parameter wrapper ({id, title, content}). That dropped the field
silently on older SDKs and raised ``ClassValidationError`` once the generated
model gained ``parameters``. This pins the correct behaviour: a parameter that
goes in must come back out unchanged.
"""

from __future__ import annotations

import json
from pathlib import Path
from types import SimpleNamespace

import pytest
from gooddata_api_client.api_client import ApiClient
from gooddata_api_client.model.declarative_automation import DeclarativeAutomation
from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)

_NUMBER_PARAMETER = {
    "id": "discount-rate",
    "title": "Discount Rate",
    "content": {"type": "NUMBER", "defaultValue": 0.5},
}
_DATE_RANGE_PARAMETER = {
    "id": "fiscal-year",
    "title": "Fiscal Year",
    "content": {"type": "DATE_RANGE", "defaultValue": {"granularity": "MONTH", "from": "2025-08", "to": "2026-07"}},
}
_PARAMETERS = pytest.mark.parametrize(
    "parameter", [_NUMBER_PARAMETER, _DATE_RANGE_PARAMETER], ids=["number", "date-range"]
)


@_PARAMETERS
def test_declarative_analytics_parameters_survive_round_trip(parameter: dict) -> None:
    analytics = CatalogDeclarativeAnalytics.from_dict({"analytics": {"parameters": [parameter]}})

    # The typed wrapper must actually capture the parameter as a declarative
    # parameter (id/title/content), not the data-source name/value shape.
    params = analytics.analytics.parameters
    assert len(params) == 1
    assert params[0].id == parameter["id"]
    assert params[0].title == parameter["title"]
    assert params[0].content["type"] == parameter["content"]["type"]

    # The api round-trip must preserve it verbatim - neither dropped nor mangled.
    round_tripped = analytics.to_api().to_dict(camel_case=True)
    assert round_tripped["analytics"]["parameters"] == [parameter]


@_PARAMETERS
def test_declarative_analytics_parameters_survive_disk_round_trip(parameter: dict, tmp_path: Path) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({"parameters": [parameter]})

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert [p.to_dict(camel_case=True) for p in reloaded.parameters] == [parameter]


def test_declarative_automation_with_a_parameterized_dashboard_filter_reads_from_the_api() -> None:
    dashboard_filter = {
        "dashboardParameterizedDateFilter": {
            "parameter": {"identifier": {"id": "fiscal-year", "type": "parameter"}},
            "localIdentifier": "fiscal-year-filter",
        }
    }
    body = {
        "id": "monthly-export",
        "dashboardTabularExports": [
            {
                "requestPayload": {
                    "dashboardId": "sales",
                    "fileName": "sales",
                    "format": "XLSX",
                    "dashboardFiltersOverride": [dashboard_filter],
                }
            }
        ],
    }

    api_client = ApiClient()
    automation = api_client.deserialize(SimpleNamespace(data=json.dumps(body)), (DeclarativeAutomation,), True)

    assert api_client.sanitize_for_serialization(automation) == body
