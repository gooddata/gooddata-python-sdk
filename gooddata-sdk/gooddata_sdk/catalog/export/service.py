# (C) 2023 GoodData Corporation
import time
from pathlib import Path
from typing import Callable, Optional, Union

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.pdf_export_request import PdfExportRequest
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from gooddata_sdk import (
    ExportCustomLabel,
    ExportCustomMetric,
    ExportCustomOverride,
    ExportRequest,
    ExportSettings,
    GoodDataApiClient,
    SimpleMetric,
)
from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.insight import InsightService
from gooddata_sdk.table import ExecutionTable, TableService


class ExportService(CatalogServiceBase):
    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(ExportService, self).__init__(api_client)

    @staticmethod
    def _get_exported_content(
        workspace_id: str,
        export_id: str,
        get_func: Callable,
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> bytes:
        assert (
            timeout > 0 and retry > 0 and max_retry > 0
        ), f"Timeout value '{timeout}' or retry value '{retry}' or max retry value '{max_retry}' is negative."
        assert timeout > retry, f"Retry value {retry} cannot be higher than timeout value {timeout}"
        assert retry <= max_retry, f"Retry value {retry} must be smaller or the same as max retry value {max_retry}"
        response = get_func(workspace_id=workspace_id, export_id=export_id, _preload_content=False)
        if response.status == 202:
            counter = 0
            while counter * retry <= timeout:
                time.sleep(retry)
                retry = min(retry * 2, max_retry)
                counter += 1
                response = get_func(workspace_id=workspace_id, export_id=export_id, _preload_content=False)
                if response.status != 202:
                    break
        if response.status != 200:
            raise ValueError(
                f"Server was not able to return response. " f"The last response status is '{response.status}'."
            )
        return response.data

    @staticmethod
    def _create_export(
        workspace_id: str, request: Union[PdfExportRequest, TabularExportRequest], create_func: Callable
    ) -> str:
        response = create_func(workspace_id, request)
        return response["export_result"]

    def _dashboard_id_exists(self, workspace_id: str, dashboard_id: str) -> bool:
        """
        Check is dashboard id exists.

        Note:
            This is needed due to the fact that exporters do not check existence of dashboard id.
        """
        try:
            self._entities_api.get_entity_analytical_dashboards(workspace_id=workspace_id, object_id=dashboard_id)
        except NotFoundException:
            return False
        return True

    def _export_common(
        self,
        workspace_id: str,
        request: Union[PdfExportRequest, TabularExportRequest],
        file_path: Path,
        create_func: Callable,
        get_func: Callable,
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        export_id = self._create_export(workspace_id, request, create_func)
        content = self._get_exported_content(workspace_id, export_id, get_func, timeout, retry, max_retry)
        with open(file_path, "wb") as f:
            f.write(content)

    def export_pdf(
        self,
        workspace_id: str,
        dashboard_id: str,
        file_name: str,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        if not self._dashboard_id_exists(workspace_id, dashboard_id):
            raise ValueError(f"Dashboard id '{dashboard_id}' does not exist for workspace '{workspace_id}'.")
        store_path = store_path if isinstance(store_path, Path) else Path(store_path)
        request = PdfExportRequest(dashboard_id=dashboard_id, file_name=file_name)
        file_path = store_path / f"{file_name}.pdf"
        create_func = self._actions_api.create_pdf_export
        get_func = self._actions_api.get_exported_file
        self._export_common(workspace_id, request, file_path, create_func, get_func, timeout, retry, max_retry)

    def export_tabular(
        self,
        workspace_id: str,
        export_request: ExportRequest,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        store_path = store_path if isinstance(store_path, Path) else Path(store_path)
        file_path = store_path / export_request.file
        create_func = self._actions_api.create_tabular_export
        get_func = self._actions_api.get_tabular_export
        self._export_common(
            workspace_id, export_request.to_api(), file_path, create_func, get_func, timeout, retry, max_retry
        )

    @staticmethod
    def _custom_overrides_labels(exec_table: ExecutionTable, metrics_format: str = "#,##0") -> ExportCustomOverride:
        """
        Insights by default use generated hash as local_id therefore we might want to use dummy logic to replace it.
        For attributes by label.id
        For metrics by item.id
        """
        labels = {
            attribute.local_id: ExportCustomLabel(title=attribute.label.id) for attribute in exec_table.attributes
        }
        metrics = {
            metric.local_id: ExportCustomMetric(
                title=metric.item.id if isinstance(metric, SimpleMetric) else metric.local_id, format=metrics_format
            )
            for metric in exec_table.metrics
        }
        return ExportCustomOverride(labels=labels, metrics=metrics)

    def export_tabular_by_insight_id(
        self,
        workspace_id: str,
        insight_id: str,
        file_format: str,
        use_labels: bool = True,
        file_name: Optional[str] = None,
        settings: Optional[ExportSettings] = None,
        custom_override: Optional[ExportCustomOverride] = None,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        try:
            insight = InsightService(self._client).get_insight(workspace_id=workspace_id, insight_id=insight_id)
            exec_table = TableService(self._client).for_insight(workspace_id=workspace_id, insight=insight)
            custom_override = self._custom_overrides_labels(exec_table) if use_labels else custom_override
            file_name = file_name if file_name is not None else insight.title
            export_request = ExportRequest(
                format=file_format,
                execution_result=exec_table.result_id,
                file_name=file_name,
                settings=settings,
                custom_override=custom_override,
            )
            self.export_tabular(
                workspace_id=workspace_id,
                export_request=export_request,
                store_path=store_path,
                timeout=timeout,
                retry=retry,
                max_retry=max_retry,
            )
        except NotFoundException:
            print(
                f"Either workspace workspace_id='{workspace_id}' or insight insight_id='{insight_id}' does not exist."
            )
