# (C) 2026 GoodData Corporation
"""Regression-guard for `put_declarative_ldm` over aggregate-aware LDMs.

Task B verified that `CatalogDeclarativeLdm` byte-round-trips an agg-aware
layout. This file checks the next link in the chain: that
`CatalogWorkspaceContentService.put_declarative_ldm` actually hands the
aggregate-aware fields to the LayoutApi unchanged on its way to the
platform. The historical risk is that the SDK's `to_api` step strips a
field because the api-client model didn't carry it, or that an `attrs`
default collapses an explicit `[]` into "missing".
"""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import MagicMock

from gooddata_sdk.catalog.workspace.content_service import CatalogWorkspaceContentService
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import (
    CatalogDeclarativeLdm,
    CatalogDeclarativeModel,
)

# Reuses Task B's fixture so the two tests stay aligned on what an
# agg-aware shape looks like in this codebase.
_FIXTURE = Path(__file__).parent / "agg_aware_ldm" / "layout.json"


def _captured_payload() -> dict:
    """Build the agg-aware LDM, run it through `put_declarative_ldm`, capture the api dict."""
    raw = json.loads(_FIXTURE.read_text())
    ldm = CatalogDeclarativeLdm.from_dict(raw)
    model = CatalogDeclarativeModel(ldm=ldm)

    layout_api = MagicMock(name="LayoutApi")
    svc = CatalogWorkspaceContentService.__new__(CatalogWorkspaceContentService)
    svc._layout_api = layout_api  # type: ignore[attr-defined] # bypass full init
    svc.put_declarative_ldm("ws", model)

    assert layout_api.set_logical_model.call_count == 1
    sent_workspace_id, sent_model = layout_api.set_logical_model.call_args.args
    assert sent_workspace_id == "ws"
    return sent_model.to_dict(camel_case=True)


def _dataset(payload: dict, dataset_id: str) -> dict:
    return next(ds for ds in payload["ldm"]["datasets"] if ds["id"] == dataset_id)


def test_put_preserves_auxiliary_dataset_shape() -> None:
    payload = _captured_payload()
    aux = _dataset(payload, "orders")
    assert aux["type"] == "AUXILIARY"
    # The synthetic identity attribute and the references to dim datasets
    # must reach the wire intact — a regression here breaks AUX hosting.
    assert any(a["id"] == "orders.unique_customer" for a in aux["attributes"])
    assert aux["references"], "AUX-to-dim references must reach the API call"
    assert aux["references"][0]["identifier"]["id"] == "dim_country"
    # AUX must not gain pre-aggregation fields on the way out.
    assert "precedence" not in aux or aux["precedence"] is None
    assert "sql" not in aux or aux["sql"] is None
    assert "dataSourceTableId" not in aux or aux["dataSourceTableId"] is None


def test_put_preserves_pre_aggregation_dataset_shape() -> None:
    payload = _captured_payload()
    agg = _dataset(payload, "agg_orders_country_daily")
    assert agg["type"] == "NORMAL"
    assert agg["precedence"] == 1
    assert agg["dataSourceTableId"]["id"] == "agg_orders_country_daily"
    assert len(agg["aggregatedFacts"]) == 2

    by_id = {af["id"]: af for af in agg["aggregatedFacts"]}
    revenue = by_id["agg_orders_country_daily.revenue"]
    hll = by_id["agg_orders_country_daily.unique_customers_hll"]

    # SUM-of-fact target survives.
    assert revenue["sourceFactReference"]["operation"] == "SUM"
    assert revenue["sourceFactReference"]["reference"]["type"] == "fact"
    # HLL APPROXIMATE_COUNT-of-attribute target survives — this is the load-
    # bearing shape that a regression here would silently corrupt.
    assert hll["sourceFactReference"]["operation"] == "APPROXIMATE_COUNT"
    assert hll["sourceFactReference"]["reference"]["type"] == "attribute"
    assert hll["sourceColumnDataType"] == "HLL"


def test_put_preserves_sql_synthesized_dim_shape() -> None:
    payload = _captured_payload()
    dim = _dataset(payload, "dim_country")
    assert dim["sql"]["statement"].upper().startswith("SELECT DISTINCT")
    assert "dataSourceTableId" not in dim or dim["dataSourceTableId"] is None
    # Attribute on the dim must keep its physical column mapping.
    assert dim["attributes"][0]["sourceColumn"] == "country"
