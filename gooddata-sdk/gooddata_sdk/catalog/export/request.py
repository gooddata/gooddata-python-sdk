# (C) 2023 GoodData Corporation
from typing import Any, Dict, Optional, Type

import attr

from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class ExportRequest(Base):
    format: str
    # execution result id from backend
    execution_result: str
    file_name: str
    settings: Optional[Dict[str, bool]] = None
    custom_override: Optional[Dict[str, Any]] = None

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
