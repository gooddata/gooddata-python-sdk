# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Any

from gooddata_metadata_client.model.generate_ldm_request import GenerateLdmRequest


class CatalogGenerateLdmRequest:
    def __init__(
        self,
        separator: str,
        generate_long_ids: bool = None,
        table_prefix: str = None,
        view_prefix: str = None,
        primary_label_prefix: str = None,
        secondary_label_prefix: str = None,
        fact_prefix: str = None,
        date_granularities: str = None,
        grain_prefix: str = None,
        reference_prefix: str = None,
        grain_reference_prefix: str = None,
        denorm_prefix: str = None,
        wdf_prefix: str = None,
    ):
        self.separator = separator
        self.generate_long_ids = generate_long_ids
        self.table_prefix = table_prefix
        self.view_prefix = view_prefix
        self.primary_label_prefix = primary_label_prefix
        self.secondary_label_prefix = secondary_label_prefix
        self.fact_prefix = fact_prefix
        self.date_granularities = date_granularities
        self.grain_prefix = grain_prefix
        self.reference_prefix = reference_prefix
        self.grain_reference_prefix = grain_reference_prefix
        self.denorm_prefix = denorm_prefix
        self.wdf_prefix = wdf_prefix

    def to_api(self) -> GenerateLdmRequest:
        kwargs: dict[str, Any] = dict()
        if self.generate_long_ids:
            kwargs["generate_long_ids"] = self.generate_long_ids
        if self.table_prefix:
            kwargs["table_prefix"] = self.table_prefix
        if self.view_prefix:
            kwargs["view_prefix"] = self.view_prefix
        if self.primary_label_prefix:
            kwargs["primary_label_prefix"] = self.primary_label_prefix
        if self.secondary_label_prefix:
            kwargs["secondary_label_prefix"] = self.secondary_label_prefix
        if self.fact_prefix:
            kwargs["fact_prefix"] = self.fact_prefix
        if self.date_granularities:
            kwargs["date_granularities"] = self.date_granularities
        if self.grain_prefix:
            kwargs["grain_prefix"] = self.grain_prefix
        if self.reference_prefix:
            kwargs["reference_prefix"] = self.reference_prefix
        if self.grain_reference_prefix:
            kwargs["grain_reference_prefix"] = self.grain_reference_prefix
        if self.denorm_prefix:
            kwargs["denorm_prefix"] = self.denorm_prefix
        if self.wdf_prefix:
            kwargs["wdf_prefix"] = self.wdf_prefix
        return GenerateLdmRequest(self.separator, **kwargs)
