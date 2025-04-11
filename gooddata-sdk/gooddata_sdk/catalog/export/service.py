# (C) 2023 GoodData Corporation
import time
from pathlib import Path
from typing import Any, Callable, Optional, Union

from gooddata_api_client.exceptions import NotFoundException
from gooddata_api_client.model.slides_export_request import SlidesExportRequest as SlidesExportRequestApi
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from gooddata_api_client.model.visual_export_request import VisualExportRequest

from gooddata_sdk.catalog.catalog_service_base import CatalogServiceBase
from gooddata_sdk.catalog.export.request import (
    ExportRequest,
    ExportSettings,
    SlidesExportRequest,
)
from gooddata_sdk.client import GoodDataApiClient
from gooddata_sdk.visualization import VisualizationService


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
        export_tabular_by_visualization_id:
            Exports the tabular data of a particular visualization id.
    """

    def __init__(self, api_client: GoodDataApiClient) -> None:
        super().__init__(api_client)
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
        assert timeout > 0 and retry > 0 and max_retry > 0, (
            f"Timeout value '{timeout}' or retry value '{retry}' or max retry value '{max_retry}' is negative."
        )
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
                f"Server was not able to return response. The last response status is '{response.status}'."
            )
        return response.data

    @staticmethod
    def _create_export(
        workspace_id: str, request: Union[VisualExportRequest, TabularExportRequest], create_func: Callable
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
        request: Union[VisualExportRequest, TabularExportRequest, SlidesExportRequestApi],
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
        metadata: Optional[dict[str, Any]] = None,
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
                The path to save the exported PDF.
                Defaults to the current directory.
            timeout (float, optional):
                The maximum amount of time (in seconds) to wait for the server to process the export.
                Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content.
                Defaults to 0.2.
            max_retry (float, optional):
                The maximum retry wait time (in seconds).
                Defaults to 5.0.
            metadata (Dict[str, Any]):
                Specify the metadata for the export.
                Specific metadata can override filtering.
        """
        if not self._dashboard_id_exists(workspace_id, dashboard_id):
            raise ValueError(f"Dashboard id '{dashboard_id}' does not exist for workspace '{workspace_id}'.")
        store_path = store_path if isinstance(store_path, Path) else Path(store_path)
        if metadata is None:
            request = VisualExportRequest(dashboard_id=dashboard_id, file_name=file_name)
        else:
            request = VisualExportRequest(dashboard_id=dashboard_id, file_name=file_name, metadata=metadata)
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

    def _get_visualization_title(self, workspace_id: str, visualization_id: str) -> str:
        try:
            visualization = VisualizationService(self._client).get_visualization(
                workspace_id=workspace_id, visualization_id=visualization_id
            )
            return visualization.title
        except NotFoundException:
            raise ValueError(
                f"Either workspace workspace_id='{workspace_id}' "
                f"or visualization visualization_id='{visualization_id}' does not exist."
            )

    def export_tabular_by_visualization_id(
        self,
        workspace_id: str,
        visualization_id: str,
        file_format: str,
        file_name: Optional[str] = None,
        settings: Optional[ExportSettings] = None,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        """
        Exports the tabular data of a particular visualization id.

        Args:
            workspace_id (str): The workspace id from which the visualization is to be exported.
            visualization_id (str): The id of the visualization to be exported.
            file_format (str): The format of the file to be exported.
            file_name (Optional[str], optional): The name which the exported file should have. Defaults to None.
            settings (Optional[ExportSettings], optional): Any additional settings for the export. Defaults to None.
            store_path (Union[str, Path], optional): The path to store the exported file. Default to Path.cwd().
            timeout (float, optional): The maximum time to wait for the export to finish. Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
            max_retry (float, optional): The maximum retry wait time (in seconds). Defaults to 5.0.

        Returns:
            None
        """
        if file_name is None:
            file_name = self._get_visualization_title(workspace_id, visualization_id)
        export_request = ExportRequest(
            format=file_format,
            visualization_object=visualization_id,
            file_name=file_name,
            settings=settings,
        )
        self.export_tabular(
            workspace_id=workspace_id,
            export_request=export_request,
            store_path=store_path,
            timeout=timeout,
            retry=retry,
            max_retry=max_retry,
        )

    def export_slides(
        self,
        workspace_id: str,
        request: SlidesExportRequest,
        store_path: Union[str, Path] = Path.cwd(),
        timeout: float = 60.0,
        retry: float = 0.2,
        max_retry: float = 5.0,
    ) -> None:
        """
        Exports slides based on slide export request.

        Args:
            workspace_id (str): The workspace id from which the visualization is to be exported.
            request (SlidesExportRequest): The request object containing the export parameters.
            store_path (Union[str, Path], optional): The path to store the exported file. Default to Path.cwd().
            timeout (float, optional): The maximum time to wait for the export to finish. Defaults to 60.0.
            retry (float, optional):
                Initial wait time (in seconds) before retrying to get the exported content. Defaults to 0.2.
            max_retry (float, optional): The maximum retry wait time (in seconds). Defaults to 5.0.

        Returns:
            None
        """
        store_path = store_path if isinstance(store_path, Path) else Path(store_path)
        file_path = store_path / f"{request.file_name}.{request.format.lower()}"
        create_func = self._actions_api.create_slides_export
        get_func = self._actions_api.get_slides_export
        self._export_common(workspace_id, request.to_api(), file_path, create_func, get_func, timeout, retry, max_retry)
