# (C) 2023 GoodData Corporation
import time
from pathlib import Path
from typing import Callable, Optional, Tuple, Union

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
    """
    ExportService provides the ability to export PDF and Tabular data from GoodData Dashboards.
    Attributes:
        _entities_api:
            A reference to the entities_api of GoodDataApiClient instance.
        _actions_api:
            A reference to the actions_api of GoodDataApiClient instance.
    Methods:
        _get_exported_content:
            A static method that gets the exported content using the provided `get_func`.
        _create_export:
            A static method that creates an export and returns its ID.
        _dashboard_id_exists:
            Checks if the given dashboard_id exists in the workspace.
        _export_common:
            Common export method for handling the exports of PDF and Tabular.
        export_pdf:
            Export a PDF of a GoodData Dashboard.
        export_tabular:
            Export Tabular data from a GoodData Dashboard.
        export_tabular_by_insight_id:
            Exports the tabular data of a particular insight id.
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super(ExportService, self).__init__(api_client)
        """
        Initializes the ExportService with the GoodDataApiClient instance.
        Args:
            api_client (GoodDataApiClient): An instance of the GoodData API Client.
        """

    @staticmethod
    def _get_exported_content(
        workspace_id: str,
        export_id: str,
        get_func: Callable,
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> bytes:
        """
        Get the exported content from a server as bytes.
        Args:
            workspace_id (str):
                The workspace ID for which content is to be exported.
            export_id (str):
                The export ID for the content to be exported.
            get_func (Callable):
                The function to call to get the export data.
            timeout (float, optional):
                The total time in seconds to wait for a successful response. Defaults to 60.0.
            retry (float, optional):
                Initial time in seconds to wait between retries. Defaults to 0.2.
            max_retry (float, optional):
                Maximum time in seconds to wait between retries. Defaults to 5.0.
        Returns:
            bytes: The exported content as bytes.
        Raises:
            ValueError: If the server is not able to return a response or if the input values are invalid.
        """
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
        """
        Creates an export of the requested type (PDF or Tabular) in the specified Workspace.
        Args:
            workspace_id (str): The ID of the target Workspace.
            request (Union[PdfExportRequest, TabularExportRequest]):
                A request object specifying the type of export (PDF or Tabular) to be created.
            create_func (Callable): The function used to create the export.
        Returns:
            str: The export result from the response object.
        """
        response = create_func(workspace_id, request)
        return response["export_result"]

    def _dashboard_id_exists(self, workspace_id: str, dashboard_id: str) -> bool:
        """
        Check if dashboard id exists.

        Args:
            workspace_id (str):
                The ID of the target Workspace.
            dashboard_id (str):
                The ID of the target Dashboard.
        Returns:
            bool: Returns true, if the dashboard exists.

        Note:
            This is needed due to the fact that exporters do not check existence of the dashboard id.
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
        """
        Common method to export content from a workspace.
        Args:
            workspace_id (str):
                The ID of the workspace to export from.
            request (Union[PdfExportRequest, TabularExportRequest]):
                The export request object (Pdf or Tabular).
            file_path (Path):
                The local file path to save the exported content.
            create_func (Callable):
                The function to create an export task.
            get_func (Callable):
                The function to get the exported content.
            timeout (float, optional):
                The maximum time to wait for the export (in seconds). Defaults to 60.0.
            retry (float, optional):
                The time interval to retry checking for exported content (in seconds). Defaults to 0.2.
            max_retry (float, optional):
                The maximum number of retries to check for exported content. Defaults to 5.0.
        Returns:
            None
        """
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
        """
        Export a PDF of the specified GoodData Dashboard and save it to the specified file path.
        Args:
            workspace_id (str):
                The ID of the GoodData Workspace.
            dashboard_id (str):
                The ID of the GoodData Dashboard.
            file_name (str):
                The name of the PDF file (excluding the file extension).
            store_path (Union[str, Path], optional):
                The path to save the exported PDF. Defaults to the current directory.
            timeout (float, optional):
                The maximum amount of time (in seconds) to wait for the server to process the export. Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
            max_retry (float, optional):
                The maximum retry wait time (in seconds). Defaults to 5.0.
        """
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
        """
        Export Tabular (CSV, XLSX) data from the specified GoodData Dashboard report, saved to the specified file path.
        Args:
            workspace_id (str):
                The ID of the GoodData Workspace.
            export_request (ExportRequest):
                An instance of ExportRequest containing the required information for the tabular export.
            store_path (Union[str, Path], optional):
                The path to save the exported tabular data. Defaults to the current directory.
            timeout (float, optional):
                The maximum amount of time (in seconds) to wait for the server to process the export. Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
            max_retry (float, optional):
                The maximum retry wait time (in seconds). Defaults to 5.0.
        """
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

    def _get_insight_exec_table(self, workspace_id: str, insight_id: str) -> Tuple[ExecutionTable, str]:
        try:
            insight = InsightService(self._client).get_insight(workspace_id=workspace_id, insight_id=insight_id)
            return TableService(self._client).for_insight(workspace_id=workspace_id, insight=insight), insight.title
        except NotFoundException:
            raise ValueError(
                f"Either workspace workspace_id='{workspace_id}' or insight insight_id='{insight_id}' does not exist."
            )

    def export_tabular_by_insight_id(
        self,
        workspace_id: str,
        insight_id: str,
        file_format: str,
        file_name: Optional[str] = None,
        settings: Optional[ExportSettings] = None,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        """
        Exports the tabular data of a particular insight id.

        Args:
            workspace_id (str): The workspace id from which the insight is to be exported.
            insight_id (str): The id of the insight to be exported.
            file_format (str): The format of the file to be exported.
            file_name (Optional[str], optional): The name which the exported file should have. Defaults to None.
            settings (Optional[ExportSettings], optional): Any additional settings for the export. Defaults to None.
            store_path (Union[str, Path], optional): The path to store the exported file. Defaults to Path.cwd().
            timeout (float, optional): The maximum time to wait for the export to finish. Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
            max_retry (float, optional): The maximum retry wait time (in seconds). Defaults to 5.0.

        Returns:
            None
        """
        exec_table, insight_tile = self._get_insight_exec_table(workspace_id, insight_id)
        custom_override = self._custom_overrides_labels(exec_table)
        file_name = file_name if file_name is not None else insight_tile
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
