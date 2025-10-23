# (C) 2022 GoodData Corporation
import attr
from gooddata_api_client.model.data_source_parameter import DataSourceParameter
from gooddata_api_client.model.parameter import Parameter

from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class CatalogParameter(Base):
    name: str
    value: str

    @staticmethod
    def client_class() -> type[Parameter]:
        return Parameter

    def to_data_source_parameter(self) -> DataSourceParameter:
        return DataSourceParameter(name=self.name, value=self.value)
