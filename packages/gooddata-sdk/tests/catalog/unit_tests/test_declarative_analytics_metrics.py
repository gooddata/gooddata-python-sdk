# (C) 2026 GoodData Corporation
"""Unit test: a metric's ``isHiddenFromKda`` survives the declarative round trip."""

from __future__ import annotations

from pathlib import Path

import pytest
from gooddata_sdk.catalog.workspace.declarative_model.workspace.analytics_model.analytics_model import (
    CatalogDeclarativeAnalyticsLayer,
)

_METRIC = {"id": "bmk_w_fraud_charged_back", "title": "BMK", "content": {"format": "#,##0", "maql": "SELECT 1"}}


@pytest.mark.parametrize(
    ("extra", "expected"),
    [
        ({"isHiddenFromKda": True}, True),
        ({"isHiddenFromKda": False}, False),
        ({}, None),
    ],
    ids=["hidden", "explicit-visible", "absent"],
)
def test_declarative_metric_is_hidden_from_kda_survives_round_trip(
    tmp_path: Path, extra: dict, expected: bool | None
) -> None:
    layer = CatalogDeclarativeAnalyticsLayer.from_dict({"metrics": [{**_METRIC, **extra}]})

    layer.store_to_disk(tmp_path)
    reloaded = CatalogDeclarativeAnalyticsLayer.load_from_disk(tmp_path)

    assert reloaded.metrics[0].is_hidden_from_kda is expected
    assert reloaded.to_api().to_dict(camel_case=True)["metrics"][0] == {**_METRIC, **extra}
