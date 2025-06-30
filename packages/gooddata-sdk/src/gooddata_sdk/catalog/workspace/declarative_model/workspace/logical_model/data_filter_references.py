# (C) 2023 GoodData Corporation
import attr
from gooddata_api_client.model.declarative_workspace_data_filter_references import (
    DeclarativeWorkspaceDataFilterReferences,
)

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.identifier import CatalogDatasetWorkspaceDataFilterIdentifier


@attr.s(auto_attribs=True, kw_only=True)
class CatalogDeclarativeWorkspaceDataFilterReferences(Base):
    filter_id: CatalogDatasetWorkspaceDataFilterIdentifier
    filter_column: str
    filter_column_data_type: str

    @staticmethod
    def client_class() -> type[DeclarativeWorkspaceDataFilterReferences]:
        return DeclarativeWorkspaceDataFilterReferences
