# (C) 2026 GoodData Corporation
"""AAC YAML ↔ declarative round-trip tests for aggregate-aware dataset shapes.

Exercises the SDK wrappers around the WASM convertor (gooddata-code-convertors)
for the three new shapes that aggregate-aware LDMs introduce:

- AUXILIARY datasets (no physical mapping, synthetic identity attributes).
- NORMAL pre-aggregation datasets with `aggregated_facts` (SUM-of-fact and
  APPROXIMATE_COUNT-of-attribute for HLL synopses).
- NORMAL synthesized dim datasets backed by a `sql:` block.

These tests guard the **SDK side** of the AAC convertor pipeline; the
heavy lifting lives in the WASM module bumped to 11.33.0+.
"""

from __future__ import annotations

import yaml
from gooddata_sdk.catalog.workspace.aac import (
    aac_dataset_to_declarative,
    declarative_dataset_to_aac,
)


def _aac_from(declarative: dict) -> dict:
    """Convert declarative dataset → AAC dict via the SDK wrapper."""
    result = declarative_dataset_to_aac(declarative)
    return yaml.safe_load(result["content"])


def _entities_for(aac: dict) -> list[dict]:
    """Build a one-element entities list (most round-trips need it)."""
    return [{"id": aac["id"], "type": aac["type"], "path": f"{aac['id']}.yaml", "data": aac}]


def test_auxiliary_dataset_round_trips_through_aac() -> None:
    declarative_in = {
        "id": "orders",
        "title": "Orders",
        "type": "AUXILIARY",
        "attributes": [
            {"id": "orders.unique_customer", "title": "Unique Customer", "labels": []},
        ],
        "facts": [],
        "grain": [],
        "references": [],
        "aggregatedFacts": [],
    }
    aac = _aac_from(declarative_in)
    # AUX is encoded with `dataset_type: auxiliary` on the AAC side.
    assert aac["dataset_type"] == "auxiliary"
    assert "orders.unique_customer" in aac["fields"]
    assert aac["fields"]["orders.unique_customer"]["type"] == "attribute"
    # AUX attributes must NOT carry source_column on the YAML side either.
    assert "source_column" not in aac["fields"]["orders.unique_customer"]

    declarative_out = aac_dataset_to_declarative(aac, _entities_for(aac))
    assert declarative_out["type"] == "AUXILIARY"
    attrs = declarative_out["attributes"]
    assert any(a["id"] == "orders.unique_customer" for a in attrs)
    # No physical-column mapping was injected on the way back.
    assert all("sourceColumn" not in a for a in attrs)


def test_pre_aggregation_sum_round_trips_through_aac() -> None:
    """The vanilla pre-aggregation path: SUM-of-fact aggregated_facts."""
    declarative_in = {
        "id": "agg_orders_country_daily",
        "title": "Orders by country (daily)",
        "type": "NORMAL",
        "dataSourceTableId": {
            "dataSourceId": "demo-ds",
            "id": "agg_orders_country_daily",
            "type": "dataSource",
            "path": ["agg_orders_country_daily"],
        },
        "precedence": 1,
        "aggregatedFacts": [
            {
                "id": "agg_orders_country_daily.revenue",
                "sourceColumn": "revenue",
                "sourceFactReference": {
                    "operation": "SUM",
                    "reference": {"id": "orders.revenue", "type": "fact"},
                },
            },
        ],
        "attributes": [],
        "facts": [],
        "grain": [],
        "references": [],
    }
    aac = _aac_from(declarative_in)
    assert aac["dataset_type"] == "standard"
    assert aac["precedence"] == 1
    field = aac["fields"]["agg_orders_country_daily.revenue"]
    assert field["type"] == "aggregated_fact"
    assert field["aggregated_as"] == "SUM"
    assert field["assigned_to"] == "orders.revenue"

    declarative_out = aac_dataset_to_declarative(aac, _entities_for(aac), data_source_id="demo-ds")
    assert declarative_out["type"] == "NORMAL"
    assert declarative_out["precedence"] == 1
    out_facts = declarative_out["aggregatedFacts"]
    assert len(out_facts) == 1
    assert out_facts[0]["sourceFactReference"]["operation"] == "SUM"
    assert out_facts[0]["sourceFactReference"]["reference"]["type"] == "fact"


def test_synthesized_dim_with_sql_round_trips_through_aac() -> None:
    declarative_in = {
        "id": "dim_country",
        "title": "Country",
        "type": "NORMAL",
        "sql": {
            "statement": "SELECT DISTINCT country FROM agg_orders_country_daily",
            "dataSourceId": "demo-ds",
        },
        "attributes": [
            {
                "id": "dim_country.country",
                "title": "Country",
                "sourceColumn": "country",
                "sourceColumnDataType": "STRING",
                "labels": [],
            },
        ],
        "facts": [],
        "grain": [{"id": "dim_country.country", "type": "attribute"}],
        "references": [],
        "aggregatedFacts": [],
    }
    aac = _aac_from(declarative_in)
    assert aac["sql"].startswith("SELECT DISTINCT")
    assert aac["data_source"] == "demo-ds"

    declarative_out = aac_dataset_to_declarative(aac, _entities_for(aac), data_source_id="demo-ds")
    assert declarative_out["sql"]["statement"] == declarative_in["sql"]["statement"]
    assert declarative_out["sql"]["dataSourceId"] == "demo-ds"
    out_attrs = declarative_out["attributes"]
    assert out_attrs[0]["sourceColumn"] == "country"


def test_pre_aggregation_approximate_count_attribute_target_round_trips() -> None:
    """HLL APPROXIMATE_COUNT references an attribute, not a fact.

    The platform requires `aggregatedFacts[].sourceFactReference.reference.type
    == "attribute"` for HLL synopses (gdc-nas CQ-2147).
    """
    aac = {
        "type": "dataset",
        "id": "agg_orders_country_daily",
        "title": "Agg",
        "table_path": "agg_orders_country_daily",
        "data_source": "demo-ds",
        "dataset_type": "standard",
        "precedence": 1,
        "fields": {
            "agg_orders_country_daily.unique_customers_hll": {
                "type": "aggregated_fact",
                "source_column": "unique_customers_hll",
                "data_type": "HLL",
                "aggregated_as": "APPROXIMATE_COUNT",
                "assigned_to": "attribute/orders.unique_customer",
            },
        },
    }
    aux = {
        "type": "dataset",
        "id": "orders",
        "title": "Orders",
        "dataset_type": "auxiliary",
        "fields": {"unique_customer": {"type": "attribute", "title": "Unique Customer"}},
    }
    entities = [
        {"id": "orders", "type": "dataset", "path": "orders.yaml", "data": aux},
        {"id": aac["id"], "type": aac["type"], "path": f"{aac['id']}.yaml", "data": aac},
    ]
    declarative = aac_dataset_to_declarative(aac, entities, data_source_id="demo-ds")
    af = declarative["aggregatedFacts"][0]
    assert af["sourceFactReference"]["operation"] == "APPROXIMATE_COUNT"
    assert af["sourceColumnDataType"] == "HLL"
    assert af["sourceFactReference"]["reference"]["type"] == "attribute"
