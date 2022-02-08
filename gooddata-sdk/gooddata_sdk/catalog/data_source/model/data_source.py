# (C) 2022 GoodData Corporation
from __future__ import annotations

import base64
from typing import Any, List, Optional, Tuple

from gooddata_metadata_client.model.json_api_data_source_in import JsonApiDataSourceIn
from gooddata_metadata_client.model.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes
from gooddata_metadata_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_metadata_client.model.json_api_data_source_patch import JsonApiDataSourcePatch
from gooddata_metadata_client.model.json_api_data_source_patch_attributes import JsonApiDataSourcePatchAttributes
from gooddata_metadata_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_sdk.catalog.entity import CatalogNameEntity


class CatalogDataSource(CatalogNameEntity):
    def __init__(
        self,
        id: str,
        name: str,
        data_source_type: str,
        url: str,
        schema: str,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        url_params: Optional[List[Tuple[str, str]]] = None,
    ):
        super(CatalogDataSource, self).__init__(id, name)
        self.data_source_type = data_source_type
        self.url = url
        self.schema = schema
        self.username = username
        self.password = password
        self.token = token
        self.url_params = url_params

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> CatalogDataSource:
        ea = entity["attributes"]
        return cls(
            id=entity["id"],
            name=ea["name"],
            data_source_type=ea["type"],
            url=ea["url"],
            schema=ea["schema"],
            username=ea["username"],
            # Password/token are not returned from API (security)
            # You have to fill it to keep it or update it
            password="",
            token="",
        )

    def to_api(self) -> JsonApiDataSourceInDocument:
        credentials = dict()
        if self.username:
            credentials["username"] = self.username
        if self.password:
            credentials["password"] = self.password
        if self.token:
            credentials["token"] = self.token
        return JsonApiDataSourceInDocument(
            data=JsonApiDataSourceIn(
                id=self.id,
                attributes=JsonApiDataSourceInAttributes(
                    name=self.name,
                    type=self.data_source_type,
                    url=self.url,
                    schema=self.schema,
                    **credentials,
                ),
            )
        )

    @classmethod
    def to_api_patch(cls, data_source_id: str, attributes: dict) -> JsonApiDataSourcePatchDocument:
        return JsonApiDataSourcePatchDocument(
            data=JsonApiDataSourcePatch(id=data_source_id, attributes=JsonApiDataSourcePatchAttributes(**attributes))
        )


class CatalogDataSourceUserPwd(CatalogNameEntity):
    def __init__(
        self,
        id: str,
        name: str,
        schema: str,
        username: str,
        password: str,
        url_params: Optional[List[Tuple[str, str]]] = None,
    ):
        super(CatalogDataSourceUserPwd, self).__init__(id, name)
        self.schema = schema
        self.username = username
        self.password = password
        self.url_params = url_params


class CatalogDataSourceToken(CatalogNameEntity):
    def __init__(
        self, id: str, name: str, schema: str, token_path: str, url_params: Optional[List[Tuple[str, str]]] = None
    ):
        super(CatalogDataSourceToken, self).__init__(id, name)
        self.schema = schema
        self.token_path = token_path
        self.url_params = url_params


def _join_params(url_params: Optional[List[Tuple[str, str]]], delimiter: str) -> str:
    if url_params:
        return delimiter.join([p[0] + "=" + p[1] for p in url_params])
    return ""


def make_standard_url(
    db_engine: str,
    host: str,
    port: int,
    db_name: str,
    params: List[Tuple[str, str]] = None,
) -> str:
    tmpl = "jdbc:{db_engine}://{host}:{port}/{db_name}"
    url = tmpl.format(db_engine=db_engine, host=host, port=port, db_name=db_name)
    url = url + _join_params(params, "&")
    return url


def make_snowflake_url(
    account: str,
    warehouse: str,
    db_name: str,
    port: int = 443,
    params: List[Tuple[str, str]] = None,
) -> str:
    tmpl = "jdbc:snowflake://{account}.snowflakecomputing.com:{port}?warehouse={warehouse}&db={db_name}"
    url = tmpl.format(account=account, port=port, warehouse=warehouse, db_name=db_name)
    url = url + _join_params(params, "&")
    return url


def make_bigquery_url(project_id: str, params: List[Tuple[str, str]] = None) -> str:
    tmpl = "jdbc:bigquery://https://www.googleapis.com/bigquery/v2:443;ProjectId={project_id};OAuthType=0"
    url = tmpl.format(project_id=project_id)
    url = url + _join_params(params, ";")
    return url


def encode_bigquery_token(file_path: str) -> str:
    with open(file_path, "rb") as fp:
        return base64.b64encode(fp.read()).decode("utf-8")
