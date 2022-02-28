# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.declarative_ldm import DeclarativeLdm
from gooddata_metadata_client.model.declarative_model import DeclarativeModel
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.dataset.dataset import (
    CatalogDeclarativeDataset,
)
from gooddata_sdk.catalog.workspace.declarative_model.workspace.logical_model.date_dataset.date_dataset import (
    CatalogDeclarativeDateDataset,
)


class CatalogDeclarativeModel:
    def __init__(self, ldm: CatalogDeclarativeLdm = None):
        self.ldm = ldm

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeModel:
        ldm = CatalogDeclarativeLdm.from_api(entity["ldm"]) if entity.get("ldm") else None
        return cls(ldm)

    def to_api(self) -> DeclarativeModel:
        kwargs: dict[str, Any] = dict()
        if self.ldm:
            kwargs["ldm"] = self.ldm.to_api()
        return DeclarativeModel(**kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeModel):
            return False
        return self.ldm == other.ldm


class CatalogDeclarativeLdm:
    def __init__(
        self,
        datasets: list[CatalogDeclarativeDataset] = None,
        date_instances: list[CatalogDeclarativeDateDataset] = None,
    ):
        self.datasets = datasets or []
        self.date_instances = date_instances or []

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDeclarativeLdm:
        datasets = [CatalogDeclarativeDataset.from_api(v) for v in entity["datasets"]] if entity.get("datasets") else []
        date_instances = (
            [CatalogDeclarativeDateDataset.from_api(v) for v in entity["date_instances"]]
            if entity.get("date_instances")
            else []
        )
        return cls(datasets, date_instances)

    def to_api(self) -> DeclarativeLdm:
        kwargs: dict[str, Any] = {
            "datasets": [v.to_api() for v in self.datasets],
            "date_instances": [v.to_api() for v in self.date_instances],
        }
        return DeclarativeLdm(**kwargs)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, CatalogDeclarativeLdm):
            return False
        return self.datasets == other.datasets and self.date_instances == other.date_instances
