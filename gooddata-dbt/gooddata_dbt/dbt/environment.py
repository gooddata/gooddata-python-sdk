# (C) 2023 GoodData Corporation
import os
from typing import Dict

import attrs
from cattrs import structure


@attrs.define
class Environment:
    name: str
    environment_name: str
    profile: str = attrs.field(init=False, default=os.environ.get("ELT_ENVIRONMENT", ""))
    target: str = attrs.field(init=False, default=os.environ.get("DBT_TARGET", ""))
    title: str = attrs.field(init=False, default="")
    type: str
    account: str
    database: str
    warehouse: str
    schema: str

    user_key: str
    password_key: str

    user: str = attrs.field(init=False, default=attrs.Factory(lambda self: os.environ[self.user_key], takes_self=True))
    password: str = attrs.field(
        init=False, default=attrs.Factory(lambda self: os.environ[self.password_key], takes_self=True)
    )

    def __attrs_post_init__(self) -> None:
        if "DBT_ENVIRONMENT_TITLE" in os.environ:
            self.title = os.environ["DBT_ENVIRONMENT_TITLE"]
        else:
            self.title = f"{self.name} dbt Cloud {self.environment_name}"

    @classmethod
    def from_dict(cls, data: Dict) -> "Environment":
        return structure(data, cls)

    def to_dict(self) -> Dict:
        return attrs.asdict(self)

    def to_profile(self) -> Dict:
        required = ["title", "type", "account", "user", "password", "database", "warehouse", "schema"]
        environment_dict = self.to_dict()
        return {r: environment_dict[r] for r in required}
