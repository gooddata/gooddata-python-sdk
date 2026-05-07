# (C) 2026 GoodData Corporation
"""Smoke tests for `APPROXIMATE_COUNT` aggregation in compute-model `SimpleMetric`.

`APPROXIMATE_COUNT` was added to `SIMPLE_METRIC_AGGREGATION` to support HLL
APPROXIMATE_COUNT — the AFM-side counterpart of the agg-aware LDM work.
The aggregation targets an attribute on an AUXILIARY dataset (the synthetic
identity attribute that the HLL synopsis points at), not a fact.

These smoke tests pin down that:

- `SimpleMetric` accepts `APPROXIMATE_COUNT` (case-insensitive, like every
  other aggregation in the enum).
- The resulting api-model carries `aggregation: "APPROXIMATE_COUNT"` and an
  attribute target — that's the wire shape calcique routes to
  `HLL_CARDINALITY()` over the HLL column.
"""

from __future__ import annotations

import pytest
from gooddata_sdk import ObjId, SimpleMetric
from gooddata_sdk.compute.model.metric import SIMPLE_METRIC_AGGREGATION


def test_approximate_count_is_in_allowed_aggregations() -> None:
    """The enum is the source of truth — make the membership explicit."""
    assert "APPROXIMATE_COUNT" in SIMPLE_METRIC_AGGREGATION


@pytest.mark.parametrize("aggregation", ["APPROXIMATE_COUNT", "approximate_count"])
def test_approximate_count_accepts_case_insensitive(aggregation: str) -> None:
    metric = SimpleMetric(
        local_id="unique_users",
        item=ObjId(type="attribute", id="orders.unique_customer"),
        aggregation=aggregation,
    )
    assert metric.aggregation == "APPROXIMATE_COUNT"


def test_approximate_count_api_model_targets_attribute() -> None:
    """The wire shape calcique sees: APPROXIMATE_COUNT over an attribute target."""
    metric = SimpleMetric(
        local_id="unique_users",
        item=ObjId(type="attribute", id="orders.unique_customer"),
        aggregation="APPROXIMATE_COUNT",
    )
    api_dict = metric.as_api_model().to_dict()
    measure = api_dict["definition"]["measure"]
    assert measure["aggregation"] == "APPROXIMATE_COUNT"
    assert measure["item"] == {"identifier": {"id": "orders.unique_customer", "type": "attribute"}}
