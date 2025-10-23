# (C) 2023 GoodData Corporation

import attrs
from cattrs import structure


@attrs.define
class DbtCloudEnvironmentProjectConnectionDetails:
    account: str
    # database: str # TODO - dbt CLoud provides wrong value here, we must take it from Credentials, see below
    warehouse: str


@attrs.define
class DbtCloudEnvironmentProjectConnection:
    name: str
    type: str
    details: DbtCloudEnvironmentProjectConnectionDetails


@attrs.define
class DbtCloudEnvironmentProject:
    connection: DbtCloudEnvironmentProjectConnection


@attrs.define
class DbtCloudEnvironmentCredentials:
    user: str
    database: str


@attrs.define
class DbtCloudEnvironment:
    name: str
    project: DbtCloudEnvironmentProject
    credentials: DbtCloudEnvironmentCredentials

    @classmethod
    def from_dict(cls, data: dict) -> "DbtCloudEnvironment":
        return structure(data, cls)

    def to_profile(self, password: str, schema_name: str) -> dict:
        # TODO: add support for other DB types, now it is hardcoded to Snowflake
        return {
            "title": f"{self.project.connection.name} ({self.name} dbtCloud)",
            "type": self.project.connection.type,
            "account": self.project.connection.details.account,
            "user": self.credentials.user,
            "password": password,
            "database": self.credentials.database,
            "warehouse": self.project.connection.details.warehouse,
            "schema": schema_name,
        }
