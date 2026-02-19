# (C) 2022 GoodData Corporation
from __future__ import annotations

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
    sqls: list[CatalogPdmSql] | None = None
    tables: list[CatalogDeclarativeTable] | None = None

    @staticmethod
    def client_class() -> type[PdmLdmRequest]:
        return PdmLdmRequest


@attr.s(auto_attribs=True, kw_only=True)
class CatalogGenerateLdmRequest(Base):
    separator: str = "__"
    generate_long_ids: bool | None = None
    table_prefix: str | None = None
    view_prefix: str | None = None
    primary_label_prefix: str | None = None
    secondary_label_prefix: str | None = None
    fact_prefix: str | None = None
    date_granularities: str | None = None
    grain_prefix: str | None = None
    reference_prefix: str | None = None
    grain_reference_prefix: str | None = None
    denorm_prefix: str | None = None
    wdf_prefix: str | None = None
    pdm: CatalogPdmLdmRequest | None = None
    workspace_id: str | None = None
    translation_prefix: str | None = None

    @staticmethod
    def client_class() -> type[GenerateLdmRequest]:
        return GenerateLdmRequest
