# (C) 2025 GoodData Corporation

import attrs
import requests

from gooddata_pipelines.api import GoodDataApi
from gooddata_pipelines.api.gooddata_api import API_VERSION
from gooddata_pipelines.backup_and_restore.csv_reader import CSVReader
from gooddata_pipelines.backup_and_restore.models.input_type import InputType
from gooddata_pipelines.backup_and_restore.models.workspace_response import (
    Workspace,
    WorkspaceResponse,
)
from gooddata_pipelines.logger import LogObserver


class BackupInputProcessor:
    """Class to handle the input CSV and prepare the actual input for the backup.

    Based on the InputType value, this class will determine which approach to take
    in getting the IDs of workspaces to backup. It will then call appropriate
    GoodData Cloud endpoints to get the IDs and return them as a list.
    """

    _api: GoodDataApi
    base_workspace_endpoint: str
    hierarchy_endpoint: str
    all_workspaces_endpoint: str

    def __init__(self, api: GoodDataApi, page_size: int) -> None:
        self._api = api
        self.page_size = page_size
        self.logger = LogObserver()
        self.csv_reader = CSVReader()

        self.set_endpoints()

    def set_endpoints(self) -> None:
        """Sets the hierarchy endpoint for the API client."""
        self.base_workspace_endpoint = "/api/v1/entities/workspaces"
        self.hierarchy_endpoint = (
            f"{self.base_workspace_endpoint}?"
            + "filter=parent.id=={parent_id}"
            + f"&include=parent&page=0&size={self.page_size}&sort=name,asc&metaInclude=page,hierarchy"
        )
        self.all_workspaces_endpoint = f"{self.base_workspace_endpoint}?page=0&size={self.page_size}&sort=name,asc&metaInclude=page"

    @attrs.define
    class _ProcessDataOutput:
        workspace_ids: list[str]
        sub_parents: list[str] | None = None

    def fetch_page(self, url: str) -> WorkspaceResponse:
        """Fetch a page of workspaces."""

        # Separate the API path from the URL so that it can be fed to the api class
        endpoint: str = url.split(f"api/{API_VERSION}")[1]
        response: requests.Response = self._api._get(endpoint)
        if response.ok:
            return WorkspaceResponse(**response.json())
        else:
            raise RuntimeError(
                f"Failed to fetch data from the API. URL: {endpoint}"
            )

    @staticmethod
    def process_data(data: list[Workspace]) -> _ProcessDataOutput:
        """Extract children and sub-parents from workspace data."""
        children: list[str] = []
        sub_parents: list[str] = []

        for workspace in data:
            # append child workspace IDs
            children.append(workspace.id)

            # if hierarchy is present and has children, append child workspace ID to sub_parents
            if workspace.meta and workspace.meta.hierarchy:
                if workspace.meta.hierarchy.children_count > 0:
                    sub_parents.append(workspace.id)
        return BackupInputProcessor._ProcessDataOutput(children, sub_parents)

    def log_paging_progress(self, response: WorkspaceResponse) -> None:
        """Log the progress of paging through API responses if paginatino data is present"""
        current_page: int | None
        total_pages: int | None

        if response.meta.page:
            current_page = response.meta.page.number + 1
            total_pages = response.meta.page.total_pages
        else:
            current_page = None
            total_pages = None

        if current_page and total_pages:
            self.logger.info(f"Fetched page: {current_page} of {total_pages}")

    def _paginate(
        self, url: str | None
    ) -> list["BackupInputProcessor._ProcessDataOutput"]:
        """Paginates through the API responses and returns a list of workspace IDs."""
        result: list[BackupInputProcessor._ProcessDataOutput] = []
        while url:
            response: WorkspaceResponse = self.fetch_page(url)
            self.log_paging_progress(response)
            result.append(self.process_data(response.data))
            url = response.links.next

        return result

    def get_hierarchy(self, parent_id: str) -> list[str]:
        """Returns a list of workspace IDs in the hierarchy."""
        self.logger.info(f"Fetching children of {parent_id}")
        url = self.hierarchy_endpoint.format(parent_id=parent_id)

        all_children, sub_parents = [], []

        results: list[BackupInputProcessor._ProcessDataOutput] = self._paginate(
            url
        )

        for result in results:
            all_children.extend(result.workspace_ids)
            if result.sub_parents:
                sub_parents.extend(result.sub_parents)

        for subparent in sub_parents:
            all_children += self.get_hierarchy(subparent)

        if not all_children:
            self.logger.warning(
                f"No child workspaces found for parent workspace ID: {parent_id}"
            )

        return all_children

    def get_all_workspaces(self) -> list[str]:
        """Returns a list of all workspace IDs in the organization."""
        # TODO: can be optimized - requests can be sent asynchronously.
        # Use the total number of pages to calculate the number of requests
        # to be sent. Use semaphore or otherwise limit the number of concurrent
        # requests to avoid putting too much load on the server.
        self.logger.info("Fetching all workspaces")
        url = self.all_workspaces_endpoint

        all_workspaces: list[str] = []

        results: list[BackupInputProcessor._ProcessDataOutput] = self._paginate(
            url
        )

        for result in results:
            all_workspaces.extend(result.workspace_ids)

        if not all_workspaces:
            self.logger.warning("No workspaces found in the organization.")

        return all_workspaces

    def get_ids_to_backup(
        self,
        input_type: InputType,
        path_to_csv: str | None = None,
        workspace_ids: list[str] | None = None,
    ) -> list[str]:
        """Returns the list of workspace IDs to back up based on the input type."""

        if input_type in (InputType.LIST_OF_WORKSPACES, InputType.HIERARCHY):
            if (path_to_csv is None) == (workspace_ids is None):
                raise ValueError(
                    f"Path to CSV and list of workspace IDs must be specified exclusively for this input type: {input_type.value}"
                )

            # If we're backing up based on the list, simply read it from the CSV
            list_of_parents = []
            if path_to_csv is not None:
                list_of_parents = self.csv_reader.read_backup_csv(path_to_csv)
            if workspace_ids is not None:
                list_of_parents = workspace_ids

            if input_type == InputType.LIST_OF_WORKSPACES:
                return list_of_parents
            else:
                # For hierarchy backup, we read the CSV and treat it as a list of
                # parent workspace IDs. Then we retrieve the children of each parent,
                # including their children, and so on. The parent workspaces are
                # also included in the backup.
                list_of_children: list[str] = []

                for parent in list_of_parents:
                    list_of_children.extend(self.get_hierarchy(parent))

                return list_of_parents + list_of_children

        # If we're backing up the entire organization, we simply get all workspaces
        elif input_type == InputType.ORGANIZATION:
            list_of_workspaces = self.get_all_workspaces()
            return list_of_workspaces

        else:
            # This path should be unreachable as long as the conditions above
            # exhaustively check all values of InputType Enum.
            raise ValueError(f"Unsupported input type: {input_type.value}")
