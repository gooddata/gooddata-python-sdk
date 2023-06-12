# (C) 2023 GoodData Corporation
from typing import Any, Dict, Optional, Type

import attr

from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from gooddata_sdk.catalog.base import Base


@attr.s(auto_attribs=True, kw_only=True)
class ExportRequest(Base):
    """
    ExportRequest class is used to create an export request in the desired format, filename, and settings.

    Attributes:
        format (str): The format of the output file (CSV, XLSX).
        execution_result (str): Execution result id from backend.
        file_name (str): The name of the output file.
        settings (Optional[Dict[str, bool]]): Optional dictionary containing settings for the export request.
        custom_override (Optional[Dict[str, Any]]): Optional dictionary containing custom settings.
    """

    format: str
    execution_result: str
    file_name: str
    settings: Optional[Dict[str, bool]] = None
    custom_override: Optional[Dict[str, Any]] = None

    def __attrs_post_init__(self) -> None:
        """
        Validates that the provided format is supported and raises ValueError if not.
        """
        supported_formats = ["CSV", "XLSX"]
        if self.format not in supported_formats:
            raise ValueError(
                f"format '{self.format}' is not presented " f"in supported formats {','.join(supported_formats)}"
            )

    @staticmethod
    def client_class() -> Type[TabularExportRequest]:
        """
        Returns the appropriate client class for the tabular export request.

        Returns:
            Type[TabularExportRequest]: TabularExportRequest class
        """
        return TabularExportRequest

    @property
    def file(self) -> str:
        """
        Generates the full filename with the format extension.

        Returns:
            str: Full filename with the format extension.
        """
        return f"{self.file_name}.{self.format.lower()}"
