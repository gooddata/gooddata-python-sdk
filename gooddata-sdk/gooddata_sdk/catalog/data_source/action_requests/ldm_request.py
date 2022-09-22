# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional, Type

import attr

from gooddata_api_client.model.generate_ldm_request import GenerateLdmRequest
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGenerateLdmRequest(Base):
    separator: str = "__"
    generate_long_ids: Optional[bool] = None
    table_prefix: Optional[str] = None
    view_prefix: Optional[str] = None
    primary_label_prefix: Optional[str] = None
    secondary_label_prefix: Optional[str] = None
    fact_prefix: Optional[str] = None
    date_granularities: Optional[str] = None
    grain_prefix: Optional[str] = None
    reference_prefix: Optional[str] = None
    grain_reference_prefix: Optional[str] = None
    denorm_prefix: Optional[str] = None
    wdf_prefix: Optional[str] = None

    @staticmethod
    def client_class() -> Type[GenerateLdmRequest]:
        return GenerateLdmRequest
