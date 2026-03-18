# (C) 2022 GoodData Corporation
from __future__ import annotations

import builtins
from typing import Any, ClassVar, TypeVar

from attrs import Attribute, asdict, define, field
from cattrs import structure
from gooddata_api_client.model.json_api_data_source_in import JsonApiDataSourceIn
from gooddata_api_client.model.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_patch import JsonApiDataSourcePatch
from gooddata_api_client.model.json_api_data_source_patch_attributes import JsonApiDataSourcePatchAttributes
from gooddata_api_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument

from gooddata_sdk.catalog.base import Base, value_in_allowed
from gooddata_sdk.catalog.entity import (
    BasicCredentials,
    ClientSecretCredentials,
    Credentials,
    KeyPairCredentials,
    TokenCredentials,
    TokenCredentialsFromFile,
)

U = TypeVar("U", bound="CatalogDataSourceBase")


def db_attrs_with_template(instance: CatalogDataSource, *args: Any) -> None:
    if instance.db_specific_attributes is not None and instance.url_template is None:
        raise ValueError("_URL_TMPL needs to be set when db_specific_attributes is not None.")


@define(kw_only=True, eq=False)
class CatalogDataSourceBase(Base):
    _SUPPORTED_CREDENTIALS: ClassVar[list[builtins.type[Credentials]]] = [
        BasicCredentials,
        ClientSecretCredentials,
        TokenCredentials,
        TokenCredentialsFromFile,
        KeyPairCredentials,
    ]
    _DELIMITER: ClassVar[str] = "&"
    _ATTRIBUTES: ClassVar[list[str]] = [
        "cache_strategy",
        "url",
        "parameters",
        "name",
        "type",
        "schema",
        "alternative_data_source_id",
    ]

    id: str
    name: str
    type: str = field()
    schema: str
    url: str | None = None
    cache_strategy: str | None = None
    parameters: list[dict[str, str]] | None = None
    decoded_parameters: list[dict[str, str]] | None = None
    credentials: Credentials = field(repr=False)
    alternative_data_source_id: str | None = None

    @type.validator  # type: ignore[attr-defined]
    def _check_allowed_values(self, attribute: Attribute, value: str) -> None:
        value_in_allowed(self.__class__, attribute, value, JsonApiDataSourceInAttributes)

    def to_api(self) -> Any:
        kwargs = self.credentials.to_api_args()
        attributes = asdict(
            self, filter=lambda attribute, value: attribute.name in self._ATTRIBUTES and value is not None
        )
        kwargs = {**kwargs, **attributes}
        return JsonApiDataSourceInDocument(
            data=JsonApiDataSourceIn(
                id=self.id,
                attributes=JsonApiDataSourceInAttributes(
                    **kwargs,
                ),
            )
        )

    @classmethod
    def from_api(cls: builtins.type[U], entity: dict[str, Any]) -> U:
        attributes = entity["attributes"]
        credentials = Credentials.create(cls._SUPPORTED_CREDENTIALS, entity)
        return structure({"id": entity["id"], "credentials": credentials, **attributes}, cls)

    @classmethod
    def to_api_patch(cls, data_source_id: str, attributes: dict) -> JsonApiDataSourcePatchDocument:
        return JsonApiDataSourcePatchDocument(
            data=JsonApiDataSourcePatch(id=data_source_id, attributes=JsonApiDataSourcePatchAttributes(**attributes))
        )

    def __eq__(self, other: Any) -> bool:
        return (
            self.id == other.id
            and self.name == other.name
            and self.type == other.type
            and self.schema == other.schema
            and self.parameters == other.parameters
        )


@define(kw_only=True, eq=False)
class CatalogDataSource(CatalogDataSourceBase):
    _URL_TMPL: ClassVar[str | None] = None
    _DATA_SOURCE_TYPE: ClassVar[str | None] = None

    db_vendor: str | None = field(default=None, init=False)
    db_specific_attributes: DatabaseAttributes | None = field(default=None, validator=db_attrs_with_template)
    url_params: list[tuple[str, str]] | None = None

    def __attrs_post_init__(self) -> None:
        self.db_vendor = self.db_vendor or self.type.lower()
        self.url = self._make_url()

    def _make_url(self) -> str | None:
        parameters = self._join_params()
        if self.url:
            return f"{self.url}?{parameters}" if parameters else self.url
        elif self.db_specific_attributes and self._URL_TMPL:
            base_url = self._URL_TMPL.format(
                **self.db_specific_attributes.str_attributes,
                # url contains {db_vendor}, e.g. jdbc:{db_vendor}://....
                # we inject custom or default (DS_TYPE.lower()) value there
                db_vendor=self.db_vendor,
                schema=self.schema,
            )
            return f"{base_url}?{parameters}" if parameters else base_url
        else:
            return None

    def _join_params(self) -> str | None:
        if self.url_params:
            return self._DELIMITER.join([f"{p[0]}={p[1]}" for p in self.url_params])
        return None

    @property
    def url_template(self) -> str | None:
        return self._URL_TMPL


@define(kw_only=True)
class DatabaseAttributes:
    @property
    def str_attributes(self) -> dict[str, str]:
        return asdict(self)


@define(kw_only=True)
class PostgresAttributes(DatabaseAttributes):
    host: str
    db_name: str
    port: str = "5432"


@define(kw_only=True)
class RedshiftAttributes(PostgresAttributes):
    port: str = "5439"


@define(kw_only=True)
class VerticaAttributes(PostgresAttributes):
    port: str = "5433"


@define(kw_only=True)
class GreenplumAttributes(PostgresAttributes):
    pass


@define(kw_only=True)
class MySqlAttributes(DatabaseAttributes):
    host: str
    port: str = "3306"


@define(kw_only=True)
class MariaDbAttributes(MySqlAttributes):
    pass


@define(kw_only=True)
class CatalogDataSourcePostgres(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = "jdbc:{db_vendor}://{host}:{port}/{db_name}"
    type: str = "POSTGRESQL"


@define(kw_only=True)
class CatalogDataSourceRedshift(CatalogDataSourcePostgres):
    type: str = "REDSHIFT"


@define(kw_only=True)
class CatalogDataSourceVertica(CatalogDataSourcePostgres):
    type: str = "VERTICA"


@define(kw_only=True)
class SnowflakeAttributes(DatabaseAttributes):
    account: str
    warehouse: str
    db_name: str
    port: str = "443"


@define(kw_only=True)
class CatalogDataSourceSnowflake(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = (
        "jdbc:{db_vendor}://{account}.snowflakecomputing.com:{port}?warehouse={warehouse}&db={db_name}"
    )
    type: str = "SNOWFLAKE"
    db_specific_attributes: DatabaseAttributes

    def _make_url(self) -> str:
        parameters = self._join_params()
        base_url = self._URL_TMPL.format(
            **self.db_specific_attributes.str_attributes,
            # url contains {db_vendor}, e.g. jdbc:{db_vendor}://....
            # we inject custom or default (DS_TYPE.lower()) value there
            db_vendor=self.db_vendor,
        )
        return f"{base_url}{self._DELIMITER}{parameters}" if parameters else base_url


@define(kw_only=True)
class CatalogDataSourceBigQuery(CatalogDataSource):
    type: str = "BIGQUERY"


@define(kw_only=True)
class CatalogDataSourceGreenplum(CatalogDataSourcePostgres):
    type: str = "GREENPLUM"
    db_vendor: str = "postgresql"


@define(kw_only=True)
class MsSqlAttributes(DatabaseAttributes):
    host: str
    db_name: str
    port: str = "1433"


@define(kw_only=True)
class CatalogDataSourceMsSql(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = "jdbc:{db_vendor}://{host}:{port};databaseName={db_name}"
    type: str = "MSSQL"
    db_vendor: str = "sqlserver"
    db_specific_attributes: MsSqlAttributes


@define(kw_only=True)
class DatabricksAttributes(DatabaseAttributes):
    host: str
    http_path: str
    port: str = "443"


@define(kw_only=True)
class CatalogDataSourceDatabricks(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = "jdbc:{db_vendor}://{host}:{port}/default;httpPath={http_path}"
    type: str = "DATABRICKS"
    parameters: list[dict[str, str]]
    db_specific_attributes: DatabricksAttributes

    def __attrs_post_init__(self) -> None:
        mandatory_parameter = [parameter.get("name") == "catalog" for parameter in self.parameters]
        if not any(mandatory_parameter):
            raise ValueError(f"'catalog' is mandatory parameter for data source type {self.type}")

        self.db_vendor = self.type.lower()
        self.url = self._make_url()


@define(kw_only=True)
class CatalogDataSourceMySql(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = "jdbc:{db_vendor}://{host}:{port}/{schema}"
    type: str = "MYSQL"
    db_vendor: str = "mysql"


@define(kw_only=True)
class CatalogDataSourceMariaDb(CatalogDataSourceMySql):
    type: str = "MARIADB"
    db_vendor: str = "mariadb"


@define(kw_only=True)
class MotherDuckAttributes(DatabaseAttributes):
    db_name: str


@define(kw_only=True)
class CatalogDataSourceMotherDuck(CatalogDataSource):
    _URL_TMPL: ClassVar[str] = "jdbc:duckdb:md:{db_name}"
    type: str = "MOTHERDUCK"


class _NoCredentials(Credentials):
    """Placeholder credentials for data sources that do not require authentication."""

    def to_api_args(self) -> dict[str, Any]:
        return {}

    @classmethod
    def is_part_of_api(cls, entity: dict[str, Any]) -> bool:
        return True

    @classmethod
    def from_api(cls, entity: dict[str, Any]) -> _NoCredentials:
        return cls()


@define(kw_only=True, eq=False)
class CatalogDataSourceGdStorage(CatalogDataSource):
    type: str = "GDSTORAGE"
    schema: str = ""
    credentials: Credentials = field(factory=_NoCredentials, repr=False)


@define(kw_only=True, eq=False)
class CatalogDataSourceAiLakehouse(CatalogDataSource):
    """AI Lakehouse data source.

    Note: The backend does not expose connection details (url, token, schema, parameters)
    for AI Lakehouse data sources — these fields are stripped on the server side.
    Only id, name, type, cache_strategy, and permissions are preserved.
    """

    type: str = "AILAKEHOUSE"
    schema: str = ""
    credentials: Credentials = field(factory=_NoCredentials, repr=False)
