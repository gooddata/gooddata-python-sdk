import attrs

from dbt_gooddata.dbt.base import Base

@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigEnvironment(Base):
    id: str
    name: str
    elt_environment: str

@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigEnvironmentSetup(Base):
    id: str
    environments: list[GoodDataConfigEnvironment]

@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigProduct(Base):
    id: str
    name: str
    environment_setup_id: str
    model_id: str

@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfig(Base):
    environment_setups: list[GoodDataConfigEnvironmentSetup]
    data_products: list[GoodDataConfigProduct]

    def get_environment_workspaces(self, environment_setup_id: str) -> list[GoodDataConfigEnvironment]:
        for env_setup in self.environment_setups:
            if env_setup.id == environment_setup_id:
                return env_setup.environments
