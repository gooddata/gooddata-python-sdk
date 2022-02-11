# (C) 2022 GoodData Corporation
from __future__ import annotations

from gooddata_sdk.catalog.entity import CatalogEntity
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric


class CatalogMetric(CatalogEntity):
    @property
    def format(self) -> str:
        return self._e["content"]["format"]

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=ObjId(self.id, "metric"))
