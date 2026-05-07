# (C) 2026 GoodData Corporation
"""Round-trip tests for aggregate-aware declarative LDM shapes.

Covers the three dataset shapes that the SDK must preserve byte-for-byte
through `from_dict` / `to_dict` for the catalog content service to write
them back to the platform unchanged:

- AUXILIARY datasets (synthetic identity attribute, no physical mapping).
- NORMAL pre-aggregation datasets (`precedence > 0`, `aggregatedFacts`,
  empty `grain`/`attributes`/`facts`, `dataSourceTableId`).
- NORMAL synthesized dim datasets that carry a `sql:` block instead of a
  `dataSourceTableId` (typically `SELECT DISTINCT … UNION …`).

Also asserts that the polymorphic `aggregatedFacts[].sourceFactReference`
round-trips both `fact` and `attribute` targets — the latter is the
HLL APPROXIMATE_COUNT path enabled by gdc-nas CQ-2147.
"""

from __future__ import annotations

import json
from pathlib import Path

from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
)

_FIXTURE = Path(__file__).parent / "agg_aware_ldm" / "layout.json"


def _load_raw() -> dict:
    return json.loads(_FIXTURE.read_text())


def _dataset(layout: dict, dataset_id: str) -> dict:
    return next(ds for ds in layout["datasets"] if ds["id"] == dataset_id)


def test_auxiliary_dataset_round_trips() -> None:
    raw = _load_raw()
    aux_in = _dataset(raw, "orders")
    assert aux_in["type"] == "AUXILIARY"

    ldm = CatalogDeclarativeLdm.from_dict(raw)
    aux_parsed = next(ds for ds in ldm.datasets if ds.id == "orders")
    assert aux_parsed.type == "AUXILIARY"
    # AUXILIARY datasets must NOT carry pre-aggregation fields.
    assert aux_parsed.precedence is None
    assert aux_parsed.sql is None
    assert aux_parsed.aggregated_facts is None or aux_parsed.aggregated_facts == []
    # The synthetic identity attribute and the references-to-dims must survive.
    assert any(a.id == "orders.unique_customer" for a in aux_parsed.attributes)
    assert aux_parsed.references and aux_parsed.references[0].identifier.id == "dim_country"

    aux_out = _dataset(ldm.to_dict(camel_case=True), "orders")
    assert aux_out == aux_in


def test_pre_aggregation_dataset_round_trips() -> None:
    raw = _load_raw()
    agg_in = _dataset(raw, "agg_orders_country_daily")
    assert agg_in["type"] == "NORMAL"
    assert agg_in["precedence"] == 1
    assert len(agg_in["aggregatedFacts"]) == 2

    ldm = CatalogDeclarativeLdm.from_dict(raw)
    agg = next(ds for ds in ldm.datasets if ds.id == "agg_orders_country_daily")
    assert agg.precedence == 1
    assert agg.grain == []
    assert agg.attributes == []
    assert agg.facts == []
    assert agg.data_source_table_id is not None
    assert agg.aggregated_facts is not None
    assert len(agg.aggregated_facts) == 2

    # SUM-of-fact and APPROXIMATE_COUNT-of-attribute targets must both survive.
    by_id = {af.id: af for af in agg.aggregated_facts}
    revenue = by_id["agg_orders_country_daily.revenue"]
    hll = by_id["agg_orders_country_daily.unique_customers_hll"]
    assert revenue.source_fact_reference is not None
    assert revenue.source_fact_reference.operation == "SUM"
    assert revenue.source_fact_reference.reference.type == "fact"
    assert hll.source_fact_reference is not None
    assert hll.source_fact_reference.operation == "APPROXIMATE_COUNT"
    assert hll.source_fact_reference.reference.type == "attribute"
    assert hll.source_column_data_type == "HLL"

    agg_out = _dataset(ldm.to_dict(camel_case=True), "agg_orders_country_daily")
    assert agg_out == agg_in


def test_synthesized_dim_with_sql_round_trips() -> None:
    raw = _load_raw()
    dim_in = _dataset(raw, "dim_country")
    assert dim_in["type"] == "NORMAL"
    assert "sql" in dim_in
    assert "dataSourceTableId" not in dim_in

    ldm = CatalogDeclarativeLdm.from_dict(raw)
    dim = next(ds for ds in ldm.datasets if ds.id == "dim_country")
    assert dim.sql is not None
    assert "UNION" in dim.sql.statement.upper() or "SELECT DISTINCT" in dim.sql.statement.upper()
    assert dim.data_source_table_id is None
    assert dim.precedence is None

    dim_out = _dataset(ldm.to_dict(camel_case=True), "dim_country")
    assert dim_out == dim_in


def test_full_layout_round_trips() -> None:
    """End-to-end safety net — the full LDM dict should be byte-equal after a round-trip."""
    raw = _load_raw()
    ldm = CatalogDeclarativeLdm.from_dict(raw)
    assert ldm.to_dict(camel_case=True) == raw
