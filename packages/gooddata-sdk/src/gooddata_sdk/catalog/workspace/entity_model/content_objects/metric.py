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

    @property
    def is_hidden(self) -> Optional[bool]:
        return safeget(self.json_api_attributes, ["isHidden"])

    @property
    def metric_type(self) -> Optional[str]:
        """
        Returns the metric type classification.

        Possible values:
        - "UNSPECIFIED" - Default type for metrics without semantic classification
        - "CURRENCY" - Metric represents a currency value
        - None - Not set

        Returns:
            Optional[str]: The metric type or None if not set.
        """
        return safeget(self.json_api_attributes, ["content", "metricType"])

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=self.obj_id)
