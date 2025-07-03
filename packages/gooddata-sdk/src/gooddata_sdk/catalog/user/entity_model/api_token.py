# (C) 2024 GoodData Corporation
from typing import Optional

from attrs import define

from gooddata_sdk.catalog.base import Base


@define(auto_attribs=True, kw_only=True)
class CatalogApiToken(Base):
    id: str
    bearer_token: Optional[str] = None
