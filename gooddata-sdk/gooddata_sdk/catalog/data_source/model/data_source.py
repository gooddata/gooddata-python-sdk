# (C) 2022 GoodData Corporation
from __future__ import annotations

import base64
from typing import Any, List, Optional, Tuple, Type

from gooddata_metadata_client.model.json_api_data_source_in import JsonApiDataSourceIn
from gooddata_metadata_client.model.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes
from gooddata_metadata_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_metadata_client.model.json_api_data_source_patch import JsonApiDataSourcePatch
from gooddata_metadata_client.model.json_api_data_source_patch_attributes import JsonApiDataSourcePatchAttributes
from gooddata_metadata_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_sdk.catalog.entity import (
    BasicCredentials,
    CatalogNameEntity,
    Credentials,
    TokenCredentials,
    TokenCredentialsFromFile,
)


class CatalogDataSource(CatalogNameEntity):
    _URL_TMPL: Optional[str] = None
    _URL_VENDOR: Optional[str] = None
    _DATA_SOURCE_TYPE: Optional[str] = None
    _SUPPORTED_CREDENTIALS: list[Type[Credentials]] = [BasicCredentials, TokenCredentials, TokenCredentialsFromFile]

    def __init__(
        self,
        id: str,
        name: str,
        schema: str,
        credentials: Credentials,
        url: Optional[str] = None,
        data_source_type: Optional[str] = None,
        custom_attributes: Optional[BigQueryAttributes | SnowflakeAttributes | PostgresAttributes] = None,
        enable_caching: Optional[bool] = None,
        cache_path: Optional[list[str]] = None,
        url_params: Optional[List[Tuple[str, str]]] = None,
    ):
        super(CatalogDataSource, self).__init__(id, name)
        Credentials.validate_instance(self._SUPPORTED_CREDENTIALS, credentials)
        self.custom_attributes = custom_attributes
        self.schema = schema
        self.credentials = credentials
        self.enable_caching = enable_caching
        self.cache_path = cache_path
        self.url_params = url_params
        self.data_source_type = data_source_type or self._make_data_source_type()
        self.url = url or self._make_url()

    def _make_url(self) -> str:
        if self.custom_attributes and self._URL_TMPL:
            db_vendor = None
            if self._URL_VENDOR:
                db_vendor = self._URL_VENDOR
            elif self._DATA_SOURCE_TYPE:
                db_vendor = self._DATA_SOURCE_TYPE.lower()
            return (
                self._URL_TMPL.format(
                    **self.custom_attributes.attributes,
                    # url contains {db_vendor}, e.g. jdbc:{db_vendor}://....
                    # we inject custom or default (DS_TYPE.lower()) value there
                    db_vendor=db_vendor,
                )
                + self._join_params(";")
            )
        else:
            raise Exception("Neither url(constructor) nor URL_TMPL set, cannot setup final url.")

    def _join_params(self, delimiter: str) -> str:
        if self.url_params:
            return delimiter.join([p[0] + "=" + p[1] for p in self.url_params])
        return ""

    def _make_data_source_type(self) -> str:
        if self._DATA_SOURCE_TYPE:
            return self._DATA_SOURCE_TYPE
        else:
            raise Exception(
                "Neither data_source_type(constructor) nor DATA_SOURCE_TYPE(class var) set, "
                + "cannot setup final data_source_type"
            )

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDataSource:
        ea = entity["attributes"]
        credentials = Credentials.create(cls._SUPPORTED_CREDENTIALS, entity)
        return cls(
            id=entity["id"],
            name=ea["name"],
            data_source_type=ea["type"],
            url=ea["url"],
            schema=ea["schema"],
            credentials=credentials,
            enable_caching=ea.get("enableCaching"),
            cache_path=ea.get("cachePath"),
        )

    def to_api(self) -> JsonApiDataSourceInDocument:
        kwargs = self.credentials.to_api_args()
        if self.enable_caching is not None:
            kwargs["enableCaching"] = self.enable_caching
        if self.cache_path is not None:
            kwargs["cachePath"] = self.cache_path
        return JsonApiDataSourceInDocument(
            data=JsonApiDataSourceIn(
                id=self.id,
                attributes=JsonApiDataSourceInAttributes(
                    name=self.name,
                    type=self.data_source_type,
                    url=self.url,
                    schema=self.schema,
                    **kwargs,
                ),
            )
        )

    @classmethod
    def to_api_patch(cls, data_source_id: str, attributes: dict) -> JsonApiDataSourcePatchDocument:
        return JsonApiDataSourcePatchDocument(
            data=JsonApiDataSourcePatch(id=data_source_id, attributes=JsonApiDataSourcePatchAttributes(**attributes))
        )


class PostgresAttributes:
    def __init__(self, host: str, db_name: str, port: int = 5432):
        self.host = host
        self.port = port
        self.db_name = db_name

    @property
    def attributes(self) -> dict:
        return dict(host=self.host, port=self.port, db_name=self.db_name)


class CatalogDataSourcePostgres(CatalogDataSource):
    _URL_TMPL = "jdbc:{db_vendor}://{host}:{port}/{db_name}"
    _DATA_SOURCE_TYPE = "POSTGRESQL"


class CatalogDataSourceRedshift(CatalogDataSourcePostgres):
    _DATA_SOURCE_TYPE = "REDSHIFT"


class CatalogDataSourceVertica(CatalogDataSourcePostgres):
    _DATA_SOURCE_TYPE = "VERTICA"


class SnowflakeAttributes:
    def __init__(self, account: str, warehouse: str, db_name: str, port: int = 443):
        self.account = account
        self.port = port
        self.warehouse = warehouse
        self.db_name = db_name

    @property
    def attributes(self) -> dict:
        return dict(account=self.account, port=self.port, warehouse=self.warehouse, db_name=self.db_name)


class CatalogDataSourceSnowflake(CatalogDataSource):
    _URL_TMPL = "jdbc:{db_vendor}://{account}.snowflakecomputing.com:{port}?warehouse={warehouse}&db={db_name}"
    _DATA_SOURCE_TYPE = "SNOWFLAKE"


class BigQueryAttributes:
    def __init__(self, project_id: str):
        self.project_id = project_id

    @property
    def attributes(self) -> dict:
        return dict(project_id=self.project_id)


class CatalogDataSourceBigQuery(CatalogDataSource):
    _URL_TMPL = "jdbc:{db_vendor}://https://www.googleapis.com/bigquery/v2:443;ProjectId={project_id};OAuthType=0"
    _DATA_SOURCE_TYPE = "BIGQUERY"


def encode_bigquery_token(file_path: str) -> str:
    with open(file_path, "rb") as fp:
        return base64.b64encode(fp.read()).decode("utf-8")
