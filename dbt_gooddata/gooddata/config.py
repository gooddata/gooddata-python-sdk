from typing import Optional

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
class GoodDataConfigLocalizationTo(Base):
    locale: str
    language: str


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigLocalization(Base):
    from_language: str
    to: list[GoodDataConfigLocalizationTo]


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigProduct(Base):
    id: str
    name: str
    environment_setup_id: str
    model_ids: Optional[list[str]] = []
    localization: Optional[GoodDataConfigLocalization] = None


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfig(Base):
    environment_setups: list[GoodDataConfigEnvironmentSetup]
    data_products: list[GoodDataConfigProduct]

    @property
    def all_model_ids(self) -> list[str]:
        result = []
        for product in self.data_products:
            result.extend(product.model_ids)
        return result

    def get_environment_workspaces(self, environment_setup_id: str) -> list[GoodDataConfigEnvironment]:
        for env_setup in self.environment_setups:
            if env_setup.id == environment_setup_id:
                return env_setup.environments
        return []
