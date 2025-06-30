# (C) 2023 GoodData Corporation
import argparse
import os
import re
from typing import Optional, Union
from urllib.parse import quote_plus

import attrs
import yaml
from gooddata_sdk import (
    BasicCredentials,
    CatalogDataSourceMotherDuck,
    CatalogDataSourcePostgres,
    CatalogDataSourceRedshift,
    CatalogDataSourceSnowflake,
    CatalogDataSourceVertica,
    MotherDuckAttributes,
    PostgresAttributes,
    RedshiftAttributes,
    SnowflakeAttributes,
    TokenCredentialsFromEnvVar,
    VerticaAttributes,
)

from gooddata_dbt.dbt.base import Base


@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputPostgreSQL(Base):
    name: str
    title: str
    host: str
    port: str
    user: str
    password: str = attrs.field(repr=lambda value: "***")
    dbname: str
    database: str = attrs.field(default=attrs.Factory(lambda self: self.dbname, takes_self=True))
    schema: str

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourcePostgres:
        return CatalogDataSourcePostgres(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=PostgresAttributes(
                host=self.host,
                port=self.port,
                # TODO - adopt this in Python SDK
                db_name=quote_plus(self.dbname),
            ),
            # Schema name is collected from dbt manifest from relevant tables
            schema=schema_name,
            credentials=BasicCredentials(
                username=self.user,
                password=self.password,
            ),
        )


@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputRedshift(Base):
    name: str
    title: str
    host: str
    port: str
    user: str
    password: str = attrs.field(repr=lambda value: "***")
    dbname: str
    database: str = attrs.field(default=attrs.Factory(lambda self: self.dbname, takes_self=True))
    schema: str

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourceRedshift:
        return CatalogDataSourceRedshift(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=RedshiftAttributes(
                host=self.host,
                port=self.port,
                # TODO - adopt this in Python SDK
                db_name=quote_plus(self.dbname),
            ),
            # Schema name is collected from dbt manifest from relevant tables
            schema=schema_name,
            credentials=BasicCredentials(
                username=self.user,
                password=self.password,
            ),
        )


@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputSnowflake(Base):
    name: str
    title: str
    account: str
    user: str
    password: str = attrs.field(repr=lambda value: "***")
    database: str
    warehouse: str
    schema: str
    query_tag: Optional[str] = None

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourceSnowflake:
        return CatalogDataSourceSnowflake(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=SnowflakeAttributes(
                # TODO - adopt this in Python SDK
                db_name=quote_plus(self.database),
                account=self.account,
                warehouse=self.warehouse,
            ),
            # Schema name is collected from dbt manifest from relevant tables
            schema=schema_name,
            credentials=BasicCredentials(
                username=self.user,
                password=self.password,
            ),
        )


@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputVertica(Base):
    name: str
    title: str
    host: str
    port: str
    username: str
    password: str = attrs.field(repr=lambda value: "***")
    database: str
    schema: str

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourceVertica:
        return CatalogDataSourceVertica(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=VerticaAttributes(
                host=self.host,
                port=self.port,
                # TODO - adopt this in Python SDK
                db_name=quote_plus(self.database),
            ),
            # Schema name is collected from dbt manifest from relevant tables
            schema=schema_name,
            credentials=BasicCredentials(
                username=self.username,
                password=self.password,
            ),
        )


@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputMotherDuck(Base):
    name: str
    title: str
    path: str
    schema: str
    database: str = ""

    def __attrs_post_init__(self) -> None:
        self.database = self.validate_connection_props()

    def validate_connection_props(self) -> str:
        if not self.path.startswith("md:"):
            raise ValueError(f"Path {self.path} is not a valid MotherDuck path.")
        _, db_name = self.path.split(":", 1)
        if db_name:
            return db_name
        elif self.database:
            return self.database
        else:
            raise ValueError(f"Database name is neither specified in {self.path=} nor in {self.database=}")

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourceMotherDuck:
        return CatalogDataSourceMotherDuck(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=MotherDuckAttributes(
                db_name=quote_plus(self.database),
            ),
            # Schema name is collected from dbt manifest from relevant tables
            schema=schema_name,
            credentials=TokenCredentialsFromEnvVar(
                env_var_name="MOTHERDUCK_TOKEN",
            ),
        )


DbtOutput = Union[DbtOutputPostgreSQL, DbtOutputRedshift, DbtOutputSnowflake, DbtOutputVertica, DbtOutputMotherDuck]


@attrs.define(auto_attribs=True, kw_only=True)
class DbtProfile(Base):
    name: str
    outputs: list[DbtOutput]


class DbtProfiles:
    """
    TODO:
        * from class methods from_cloud, from_local/core
        * How to read password for dbt Cloud?
    """

    def __init__(self, args: argparse.Namespace) -> None:
        self.args = args
        with open(os.path.expanduser(f"{args.profiles_dir}/profiles.yml")) as fp:
            self.dbt_profiles = yaml.safe_load(fp)

    @staticmethod
    def inject_env_vars(output_def: dict) -> None:
        env_re = re.compile(r"\{\{ env_var\('([^']+)'(,\s*'([^']+)')?\) \}\}")
        for output_key, output_value in output_def.items():
            if (env_match := env_re.search(str(output_value))) is not None:
                default_value = None
                if len(env_match.groups()) == 3:
                    default_value = env_match.group(3)
                final_value = os.getenv(env_match.group(1)) or default_value
                if final_value is None:
                    output_def[output_key] = ""
                else:
                    output_def[output_key] = env_re.sub(final_value, str(output_value))
            # else do nothing, real value seems to be stored in dbt profile

    @staticmethod
    def to_data_class(output: str, output_def: dict) -> Optional[DbtOutput]:
        db_type = output_def["type"]
        if db_type == "postgres":
            return DbtOutputPostgreSQL.from_dict({"name": output, **output_def})
        elif db_type == "redshift":
            return DbtOutputRedshift.from_dict({"name": output, **output_def})
        elif db_type == "snowflake":
            return DbtOutputSnowflake.from_dict({"name": output, **output_def})
        elif db_type == "vertica":
            return DbtOutputVertica.from_dict({"name": output, **output_def})
        elif db_type == "duckdb" and output_def["path"].startswith("md:"):
            return DbtOutputMotherDuck.from_dict({"name": output, **output_def})
        elif db_type == "duckdb":
            # No logging available here. Pass because GoodData cannot connect to DuckDB file.
            return None
        else:
            raise Exception(f"Unsupported database type {output=} {db_type=}")

    @property
    def profiles(self) -> list[DbtProfile]:
        profiles = []
        for profile, profile_def in self.dbt_profiles.items():
            outputs = []
            for output, output_def in profile_def["outputs"].items():
                self.inject_env_vars(output_def)
                dbt_output = self.to_data_class(output, output_def)
                if dbt_output:
                    outputs.append(dbt_output)
            profiles.append(DbtProfile(name=profile, outputs=outputs))
        return profiles

    @property
    def profile(self) -> DbtProfile:
        for profile in self.profiles:
            if profile.name == self.args.profile:
                return profile
        raise ValueError(f"Profile {self.args.profile} not found in {self.profiles}.")

    @property
    def target(self) -> DbtOutput:
        for output in self.profile.outputs:
            if output.name == self.args.target:
                if self.args.gooddata_upper_case:
                    output.schema = output.schema.upper()
                    output.database = output.database.upper()
                return output
        raise ValueError(f"Target {self.args.target} not found in {self.profile.outputs}.")

    @property
    def data_source_id(self) -> str:
        return f"{self.args.profile}-{self.target.name}"
