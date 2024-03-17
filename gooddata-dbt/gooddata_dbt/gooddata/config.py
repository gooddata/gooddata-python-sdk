# (C) 2023 GoodData Corporation
from typing import List, Optional

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
    environments: List[GoodDataConfigEnvironment]


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigLocalizationTo(Base):
    locale: str
    language: str


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigLocalization(Base):
    from_language: str
    to: List[GoodDataConfigLocalizationTo]


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigProduct(Base):
    id: str
    name: str
    environment_setup_id: str
    model_ids: List[str] = attr.field(default=list)
    localization: Optional[GoodDataConfigLocalization] = None
    skip_tests: Optional[List[str]] = None


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigOrganization(Base):
    gooddata_profile: str
    data_product_ids: List[str] = attr.field(default=list)


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataGlobalConfig(Base):
    test_visualizations_parallelism: Optional[int] = 1


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfig(Base):
    environment_setups: List[GoodDataConfigEnvironmentSetup]
    data_products: List[GoodDataConfigProduct]
    organizations: List[GoodDataConfigOrganization]
    global_properties: GoodDataGlobalConfig

    @property
    def all_model_ids(self) -> List[str]:
        result: List[str] = []
        for product in self.data_products:
            result.extend(product.model_ids)
        return result

    def get_environment_workspaces(self, environment_setup_id: str) -> List[GoodDataConfigEnvironment]:
        for env_setup in self.environment_setups:
            if env_setup.id == environment_setup_id:
                return env_setup.environments
        return []
