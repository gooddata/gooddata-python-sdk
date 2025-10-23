# (C) 2023 GoodData Corporation
from typing import Optional

import attr
import attrs

from gooddata_dbt.dbt.base import Base


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigEnvironment(Base):
    id: str
    name: str


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
    model_ids: list[str] = attr.field(default=list)
    localization: Optional[GoodDataConfigLocalization] = None
    skip_tests: Optional[list[str]] = None


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigOrganization(Base):
    gooddata_profile: str
    data_product_ids: list[str] = attr.field(default=list)


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataGlobalConfig(Base):
    test_visualizations_parallelism: Optional[int] = 1


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfig(Base):
    environment_setups: list[GoodDataConfigEnvironmentSetup]
    data_products: list[GoodDataConfigProduct]
    organizations: list[GoodDataConfigOrganization]
    global_properties: GoodDataGlobalConfig

    @property
    def all_model_ids(self) -> list[str]:
        result: list[str] = []
        for product in self.data_products:
            result.extend(product.model_ids)
        return result

    def get_environment_workspaces(self, environment_setup_id: str) -> list[GoodDataConfigEnvironment]:
        for env_setup in self.environment_setups:
            if env_setup.id == environment_setup_id:
                return env_setup.environments
        return []
