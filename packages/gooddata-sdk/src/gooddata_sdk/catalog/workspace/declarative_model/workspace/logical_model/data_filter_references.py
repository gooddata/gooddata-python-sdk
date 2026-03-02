# (C) 2023 GoodData Corporation
from attrs import define
from gooddata_api_client.model.declarative_workspace_data_filter_references import (
    DeclarativeWorkspaceDataFilterReferences,
)

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogDatasetWorkspaceDataFilterIdentifier


@define(kw_only=True)
class CatalogDeclarativeWorkspaceDataFilterReferences(Base):
    filter_id: CatalogDatasetWorkspaceDataFilterIdentifier
    filter_column: str
    filter_column_data_type: str

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilterReferences]:
        return DeclarativeWorkspaceDataFilterReferences
