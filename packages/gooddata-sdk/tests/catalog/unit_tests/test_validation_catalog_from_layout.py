# (C) 2026 GoodData Corporation
"""Rebuilding the catalog from a layout, so references resolve without a server.

Two rules carry this, and both are invisible in the LDM as written: an attribute has a
label sharing its id even when it declares none, and a date instance's granularities become
addressable ids. Miss either and thousands of healthy references look dangling.
"""

from __future__ import annotations

from typing import Any

from gooddata_sdk import CatalogDeclarativeAnalytics
from gooddata_sdk.catalog.validation.catalog_from_layout import catalog_ids_from_layout, catalog_ids_from_ldm
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.ldm import CatalogDeclarativeModel


def _ldm(datasets: list[dict[str, Any]], date_instances: list[dict[str, Any]] | None = None) -> CatalogDeclarativeModel:
    return CatalogDeclarativeModel.from_dict(
        {"ldm": {"datasets": datasets, "dateInstances": date_instances or []}}, camel_case=True
    )


def _dataset(
    dataset_id: str,
    *,
    attributes: dict[str, tuple[str, ...]] | None = None,
    facts: tuple[str, ...] = (),
) -> dict[str, Any]:
    return {
        "id": dataset_id,
        "title": dataset_id,
        "grain": [],
        "references": [],
        "attributes": [
            {
                "id": attribute,
                "title": attribute,
                "labels": [{"id": label, "title": label} for label in labels],
            }
            for attribute, labels in (attributes or {}).items()
        ],
        "facts": [{"id": fact, "title": fact} for fact in facts],
    }


def _date(instance_id: str, *granularities: str) -> dict[str, Any]:
    return {
        "id": instance_id,
        "title": instance_id,
        "granularities": list(granularities),
        "granularitiesFormatting": {"titleBase": "", "titlePattern": "%titleBase"},
    }


def _analytics(*metric_ids: str) -> CatalogDeclarativeAnalytics:
    return CatalogDeclarativeAnalytics.from_dict(
        {"analytics": {"metrics": [{"id": m, "title": m, "content": {"maql": "SELECT 1"}} for m in metric_ids]}},
        camel_case=True,
    )


class TestFromLdm:
    def test_datasets_facts_attributes_and_labels_are_all_addressable(self):
        ids = catalog_ids_from_ldm(_ldm([_dataset("d", attributes={"a": ("a.name",)}, facts=("f",))]))
        assert {"dataset/d", "fact/f", "attribute/a", "label/a.name"} <= ids

    def test_an_attribute_has_a_label_sharing_its_id(self):
        """The implicit primary label. Content refers to it by the attribute's id like any
        other label, and it appears nowhere in the LDM -- leaving it out reported 4654 of
        17543 healthy references as dangling on the workspace this was built against."""
        ids = catalog_ids_from_ldm(_ldm([_dataset("d", attributes={"status": ()})]))
        assert "label/status" in ids

    def test_the_implicit_label_exists_even_when_labels_are_declared(self):
        ids = catalog_ids_from_ldm(_ldm([_dataset("d", attributes={"status": ("status.name",)})]))
        assert {"label/status", "label/status.name"} <= ids

    def test_date_granularities_become_addressable_ids(self):
        """A date instance declares granularities, not attributes; content addresses
        `<instance>.<granularity>` in lower case."""
        ids = catalog_ids_from_ldm(_ldm([], [_date("process_date", "YEAR", "MONTH")]))
        assert {"dataset/process_date", "label/process_date.year", "attribute/process_date.month"} <= ids

    def test_an_empty_model_yields_nothing(self):
        assert catalog_ids_from_ldm(CatalogDeclarativeModel(ldm=None)) == set()


class TestFromLayout:
    def test_metrics_come_from_the_analytics_model(self):
        """A metric referring to another metric resolves against what the layout defines."""
        ids = catalog_ids_from_layout(_analytics("revenue"), _ldm([_dataset("d")]))
        assert "metric/revenue" in ids
        assert "dataset/d" in ids

    def test_a_layout_without_a_logical_model_offers_only_its_metrics(self):
        ids = catalog_ids_from_layout(_analytics("revenue"), None)
        assert ids == {"metric/revenue"}

    def test_an_empty_layout_offers_nothing(self):
        assert catalog_ids_from_layout(CatalogDeclarativeAnalytics(analytics=None), None) == set()
