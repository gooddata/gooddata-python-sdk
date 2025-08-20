# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

import attr
from gooddata_api_client.model.json_api_metric_out import JsonApiMetricOut

from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric
from gooddata_sdk.utils import safeget


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMetric(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiMetricOut

    @property
    def format(self) -> Optional[str]:
        return safeget(self.json_api_attributes, ["content", "format"])

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=self.obj_id)
