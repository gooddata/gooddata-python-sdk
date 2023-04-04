# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any, Optional

import attr

from gooddata_api_client.model.json_api_metric_out_list import JsonApiMetricOutList
from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.compute.model.base import ObjId
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric


@attr.s(auto_attribs=True, kw_only=True)
class CatalogMetric(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiMetricOutList

    @property
    def format(self) -> Optional[str]:
        # TODO: fix me
        if self.attributes:
            return self.attributes["content"]["format"]
        return None

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=ObjId(self.id, "metric"))
