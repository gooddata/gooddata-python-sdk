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

from pathlib import Path

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)

_PARAMETER = {
    "id": "discount-rate",
    "title": "Discount Rate",
    "content": {"type": "NUMBER", "defaultValue": 0.5},
}
_LAYOUT = {"analytics": {"parameters": [_PARAMETER]}}


def test_declarative_analytics_parameters_survive_round_trip() -> None:
    analytics = CatalogDeclarativeAnalytics.from_dict(_LAYOUT)

    # The typed wrapper must actually capture the parameter as a declarative
    # parameter (id/title/content), not the data-source name/value shape.
    params = analytics.analytics.parameters
    assert len(params) == 1
    assert params[0].id == "discount-rate"
    assert params[0].title == "Discount Rate"
    assert params[0].content["type"] == "NUMBER"

    # The api round-trip must preserve it verbatim - neither dropped nor mangled.
    round_tripped = analytics.to_api().to_dict(camel_case=True)
    assert round_tripped["analytics"]["parameters"] == [_PARAMETER]


def test_declarative_analytics_parameters_survive_disk_round_trip(tmp_path: Path) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({"parameters": [_PARAMETER]})

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert [p.id for p in reloaded.parameters] == ["discount-rate"]
    assert reloaded.parameters[0].content["type"] == "NUMBER"
