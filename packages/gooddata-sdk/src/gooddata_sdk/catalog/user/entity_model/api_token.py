# (C) 2024 GoodData Corporation

from attrs import define

from gooddata_sdk.catalog.base import Base


@define(kw_only=True)
class CatalogApiToken(Base):
    id: str
    bearer_token: str | None = None
