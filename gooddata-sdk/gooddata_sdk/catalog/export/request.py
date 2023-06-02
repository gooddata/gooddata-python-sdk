# (C) 2023 GoodData Corporation
from typing import Dict, Optional, Type

import attr

from gooddata_api_client.model.custom_label import CustomLabel as ApiCustomLabel
from gooddata_api_client.model.custom_metric import CustomMetric as ApiCustomMetric
from gooddata_api_client.model.custom_override import CustomOverride as ApiCustomOverride
from gooddata_api_client.model.settings import Settings as ApiSettings
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class ExportCustomLabel(Base):
    title: str

    @staticmethod
    def client_class() -> Type[ApiCustomLabel]:
        return ApiCustomLabel


@attr.s(auto_attribs=True, kw_only=True)
class ExportCustomMetric(Base):
    title: str
    format: str

    @staticmethod
    def client_class() -> Type[ApiCustomMetric]:
        return ApiCustomMetric


@attr.s(auto_attribs=True, kw_only=True)
class ExportCustomOverride(Base):
    labels: Optional[Dict[str, ExportCustomLabel]] = None
    metrics: Optional[Dict[str, ExportCustomMetric]] = None

    @staticmethod
    def client_class() -> Type[ApiCustomOverride]:
        return ApiCustomOverride


@attr.s(auto_attribs=True, kw_only=True)
class ExportSettings(Base):
    merge_headers: bool
    show_filters: bool

    @staticmethod
    def client_class() -> Type[ApiSettings]:
        return ApiSettings


@attr.s(auto_attribs=True, kw_only=True)
class ExportRequest(Base):
    format: str
    # execution result id from backend
    execution_result: str
    file_name: str
    settings: Optional[ExportSettings] = None
    custom_override: Optional[ExportCustomOverride] = None

    def __attrs_post_init__(self) -> None:
        supported_formats = ["CSV", "XLSX"]
        if self.format not in supported_formats:
            raise ValueError(
                f"format '{self.format}' is not presented " f"in supported formats {','.join(supported_formats)}"
            )

    @staticmethod
    def client_class() -> Type[TabularExportRequest]:
        return TabularExportRequest

    @property
    def file(self) -> str:
        return f"{self.file_name}.{self.format.lower()}"
