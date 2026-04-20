# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from attrs import define
from gooddata_api_client.model.json_api_metric_out import JsonApiMetricOut

from gooddata_sdk.catalog.entity import AttrCatalogEntity
from gooddata_sdk.compute.model.metric import Metric, SimpleMetric
from gooddata_sdk.utils import safeget


@define(kw_only=True)
class CatalogMetric(AttrCatalogEntity):
    @staticmethod
    def client_class() -> Any:
        return JsonApiMetricOut

    @property
    def format(self) -> str | None:
        return safeget(self.json_api_attributes, ["content", "format"])

    @property
    def is_hidden(self) -> bool | None:
        return safeget(self.json_api_attributes, ["isHidden"])

    @property
    def certification(self) -> str | None:
        """Certification status of the metric (e.g. 'CERTIFIED'), or None if not certified."""
        return safeget(self.json_api_attributes, ["certification"])

    @property
    def certification_message(self) -> str | None:
        """Optional message associated with the certification."""
        return safeget(self.json_api_attributes, ["certificationMessage"])

    @property
    def certified_at(self) -> str | None:
        """ISO-8601 datetime string of when the certification was set, or None."""
        return safeget(self.json_api_attributes, ["certifiedAt"])

    def as_computable(self) -> Metric:
        return SimpleMetric(local_id=self.id, item=self.obj_id)
