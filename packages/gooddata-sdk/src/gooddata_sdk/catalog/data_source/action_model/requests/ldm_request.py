# (C) 2022 GoodData Corporation
from __future__ import annotations

from typing import Optional

import attr
from gooddata_api_client.model.generate_ldm_request import GenerateLdmRequest
from gooddata_api_client.model.pdm_ldm_request import PdmLdmRequest
from gooddata_api_client.model.pdm_sql import PdmSql

from gooddata_sdk.catalog.base import Base
from gooddata_sdk.catalog.data_source.action_model.sql_column import SqlColumn
from gooddata_sdk.catalog.data_source.declarative_model.physical_model.table import CatalogDeclarativeTable


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPdmSql(Base):
    statement: str
    title: str
    columns: list[SqlColumn]

    @staticmethod
    def client_class() -> type[PdmSql]:
        return PdmSql


@attr.s(auto_attribs=True, kw_only=True)
class CatalogPdmLdmRequest(Base):
    sqls: Optional[list[CatalogPdmSql]] = None
    tables: Optional[list[CatalogDeclarativeTable]] = None

    @staticmethod
    def client_class() -> type[PdmLdmRequest]:
        return PdmLdmRequest


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
    pdm: Optional[CatalogPdmLdmRequest] = None
    workspace_id: Optional[str] = None

    @staticmethod
    def client_class() -> type[GenerateLdmRequest]:
        return GenerateLdmRequest
