import os
from typing import Optional
import attrs
import re
import yaml
from urllib.parse import quote_plus

from dbt_gooddata.dbt.base import Base
from gooddata_sdk import (
    BasicCredentials, CatalogDataSourcePostgres, PostgresAttributes,
    CatalogDataSourceSnowflake, SnowflakeAttributes,
)

@attrs.define(auto_attribs=True, kw_only=True)
class DbtOutputPostgreSQL(Base):
    name: str
    title: str
    host: str
    port: str
    user: str
    password: str = attrs.field(repr=lambda value: "***")
    dbname: str
    schema: str

    def to_gooddata(self, data_source_id: str, schema_name: str) -> CatalogDataSourcePostgres:
        return CatalogDataSourcePostgres(
            id=data_source_id,
            name=self.title,
            db_specific_attributes=PostgresAttributes(
                host=self.host,
                # TODO - adopt this in Python SDK
                db_name=quote_plus(self.dbname)
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


DbtOutput = DbtOutputPostgreSQL | DbtOutputSnowflake


@attrs.define(auto_attribs=True, kw_only=True)
class DbtProfile(Base):
    name: str
    outputs: list[DbtOutputPostgreSQL | DbtOutputSnowflake]


class DbtProfiles:
    def __init__(self, args):
        self.args = args
        with open(os.path.expanduser(f"{args.profile_dir}/profiles.yml")) as fp:
            self.dbt_profiles = yaml.safe_load(fp)

    @staticmethod
    def inject_env_vars(output_def: dict) -> None:
        env_re = re.compile(r"env_var\('([^']+)'(,\s*'([^']+)')?\)")
        for output_key, output_value in output_def.items():
            if (env_match := env_re.search(str(output_value))) is not None:
                default_value = None
                if len(env_match.groups()) == 3:
                    default_value = env_match.group(3)
                final_value = os.getenv(env_match.group(1)) or default_value
                output_def[output_key] = final_value
            # else do nothing, real value seems to be stored in dbt profile

    @staticmethod
    def to_data_class(output: str, output_def: dict) -> DbtOutput:
        db_type = output_def["type"]
        if db_type == "postgres":
            data_class = DbtOutputPostgreSQL.from_dict({"name": output} | output_def)
        elif db_type == "snowflake":
            data_class = DbtOutputSnowflake.from_dict({"name": output} | output_def)
        else:
            raise Exception(f"Unsupported database type {output=} {db_type=}")
        return data_class

    @property
    def profiles(self) -> list[DbtProfile]:
        profiles = []
        for profile, profile_def in self.dbt_profiles.items():
            outputs = []
            for output, output_def in profile_def["outputs"].items():
                self.inject_env_vars(output_def)
                dbt_output = self.to_data_class(output, output_def)
                outputs.append(dbt_output)
            profiles.append(
                DbtProfile(name=profile, outputs=outputs)
            )
        return profiles

    @property
    def profile(self) -> Optional[DbtProfile]:
        for profile in self.profiles:
            if profile.name == self.args.profile:
                return profile

    @property
    def target(self) -> Optional[DbtOutput]:
        for output in self.profile.outputs:
            if output.name == self.args.target:
                return output
