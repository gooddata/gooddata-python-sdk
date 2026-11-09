# (C) 2023 GoodData Corporation

import attr
import attrs

from gooddata_dbt.dbt.base import Base


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigEnvironment(Base):
    id: str
    name: str
    # Overrides GoodDataConfigProduct.early_access_values for this environment, if set
    early_access_values: list[str] | None = None


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
    model_ids: list[str] = attr.field(factory=list)
    localization: GoodDataConfigLocalization | None = None
    skip_tests: list[str] | None = None
    # Early access feature flags enabled on the workspaces of this data product in all environments
    early_access_values: list[str] | None = None

    def get_early_access_values(self, environment: GoodDataConfigEnvironment) -> list[str] | None:
        """Resolve early access values for the workspace of this data product in the given environment.

        The environment value wins over the data product value.
        None means "not configured" - the existing workspace value is kept.
        An empty list means "disable all early access features".
        """
        if environment.early_access_values is not None:
            return environment.early_access_values
        return self.early_access_values


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataConfigOrganization(Base):
    gooddata_profile: str
    data_product_ids: list[str] = attr.field(factory=list)


@attrs.define(auto_attribs=True, kw_only=True)
class GoodDataGlobalConfig(Base):
    test_visualizations_parallelism: int | None = 1


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
