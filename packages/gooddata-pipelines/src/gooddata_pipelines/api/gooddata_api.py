# (C) 2025 GoodData Corporation

"""Interaction with GoodData Cloud via the direct API calls."""

import json
from typing import Any

import requests

TIMEOUT = 60
REQUEST_PAGE_SIZE = 250
API_VERSION = "v1"


class ApiMethods:
    headers: dict[str, str]
    base_url: str

    @staticmethod
    def _get_base_url(domain: str) -> str:
        """Returns the root endpoint for the GoodData Cloud API.

        Method ensures that the URL starts with "https://" and does not
        end with a trailing slash.

        Args:
            domain (str): The domain of the GoodData Cloud instance.
        Returns:
            str: The base URL for the GoodData Cloud API.
        """
        # Remove trailing slash if present.
        if domain[-1] == "/":
            domain = domain[:-1]

        if not domain.startswith("https://") and not domain.startswith(
            "http://"
        ):
            domain = f"https://{domain}"

        if domain.startswith("http://") and not domain.startswith("https://"):
            domain = domain.replace("http://", "https://")

        return f"{domain}/api/{API_VERSION}"

    def _get_url(self, endpoint: str) -> str:
        """Returns the full URL for a given API endpoint.

        Args:
            endpoint (str): The API endpoint to be appended to the base URL.
        Returns:
            str: The full URL for the API endpoint.
        """
        return f"{self.base_url}{endpoint}"

    def get_all_workspace_data_filters(
        self, workspace_id: str
    ) -> requests.Response:
        """Gets all workspace data filters for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace.
        Returns:
            requests.Response: The response from the server containing all
                workspace data filters.
        """
        url = f"/entities/workspaces/{workspace_id}/workspaceDataFilters"
        return self._get(url)

    def get_workspace_data_filter_settings(
        self, workspace_id: str
    ) -> requests.Response:
        """Gets all workspace data filter settings for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace.
        Returns:
            requests.Response: The response from the server containing all
                workspace data filter settings.
        """
        url = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings?include=workspaceDataFilters"
        return self._get(url)

    def get_workspace_data_filter_setting(
        self, workspace_id: str, wdf_id: str
    ) -> requests.Response:
        """Gets a specific workspace data filter setting.

        Args:
            workspace_id (str): The ID of the workspace.
            wdf_id (str): The ID of the workspace data filter setting.
        Returns:
            requests.Response: The response from the server containing the
                workspace data filter setting.
        """
        url = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_id}"
        return self._get(url)

    def put_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting: dict[str, Any],
    ) -> requests.Response:
        """Updates a workspace data filter setting.

        Args:
            workspace_id (str): The ID of the workspace.
            wdf_setting (dict[str, Any]): The workspace data filter setting to
                update.
        Returns:
            requests.Response: The response from the server containing the
                updated workspace data filter setting.
        """
        wdf_setting_id = wdf_setting["data"]["id"]
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_setting_id}"
        return self._put(
            endpoint,
            wdf_setting,
            self.headers,
        )

    def post_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting: dict[str, Any],
    ) -> requests.Response:
        """Creates a workspace data filter setting for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace.
            wdf_setting (dict[str, Any]): The workspace data filter setting to
                create.
        Returns:
            requests.Response: The response from the server containing the
                created workspace data filter setting.
        """
        endpoint = (
            f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/"
        )
        return self._post(
            endpoint,
            wdf_setting,
            self.headers,
        )

    def delete_workspace_data_filter_setting(
        self,
        workspace_id: str,
        wdf_setting_id: str,
    ) -> requests.Response:
        """Deletes a workspace data filter setting.

        Args:
            workspace_id (str): The ID of the workspace.
            wdf_setting_id (str): The ID of the workspace data filter setting
                to delete.
        Returns:
            requests.Response: The response from the server confirming the
                deletion of the workspace data filter setting.
        """
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilterSettings/{wdf_setting_id}"
        return self._delete(
            endpoint,
        )

    def get_user_data_filters(self, workspace_id: str) -> requests.Response:
        """Gets the user data filters for a given workspace."""
        endpoint = f"/layout/workspaces/{workspace_id}/userDataFilters"
        return self._get(endpoint)

    def put_user_data_filters(
        self, workspace_id: str, user_data_filters: dict[str, Any]
    ) -> requests.Response:
        """Puts the user data filters into GoodData workspace."""
        headers = {**self.headers, "Content-Type": "application/json"}
        return self._put(
            f"/layout/workspaces/{workspace_id}/userDataFilters",
            user_data_filters,
            headers,
        )

    def get_automations(self, workspace_id: str) -> requests.Response:
        """Gets the automations for a given workspace."""
        endpoint = (
            f"/entities/workspaces/{workspace_id}/automations?include=ALL"
        )
        return self._get(endpoint)

    def post_automation(
        self, workspace_id: str, automation: dict[str, Any]
    ) -> requests.Response:
        """Posts an automation for a given workspace."""
        endpoint = f"/entities/workspaces/{workspace_id}/automations"
        return self._post(endpoint, automation)

    def delete_automation(
        self, workspace_id: str, automation_id: str
    ) -> requests.Response:
        """Deletes an automation for a given workspace."""
        endpoint = (
            f"/entities/workspaces/{workspace_id}/automations/{automation_id}"
        )
        return self._delete(endpoint)

    def get_all_metrics(self, workspace_id: str) -> requests.Response:
        """Get all metrics from the specified workspace.

        Args:
            workspace_id (str): The ID of the workspace to retrieve metrics from.
        Returns:
            requests.Response: The response containing the metrics.
        """
        endpoint = f"/entities/workspaces/{workspace_id}/metrics"
        headers = {**self.headers, "X-GDC-VALIDATE-RELATIONS": "true"}
        return self._get(endpoint, headers=headers)

    def get_all_visualization_objects(
        self, workspace_id: str
    ) -> requests.Response:
        """Get all visualizations from the specified workspace.

        Args:
            workspace_id (str): The ID of the workspace to retrieve visualizations from.
        Returns:
            requests.Response: The response containing the visualizations.
        """
        endpoint = f"/entities/workspaces/{workspace_id}/visualizationObjects"
        headers = {**self.headers, "X-GDC-VALIDATE-RELATIONS": "true"}
        return self._get(endpoint, headers=headers)

    def get_all_dashboards(self, workspace_id: str) -> requests.Response:
        """Get all dashboards from the specified workspace.

        Args:
            workspace_id (str): The ID of the workspace to retrieve dashboards from.
        Returns:
            requests.Response: The response containing the dashboards.
        """
        endpoint = f"/entities/workspaces/{workspace_id}/analyticalDashboards"
        headers = {**self.headers, "X-GDC-VALIDATE-RELATIONS": "true"}
        return self._get(endpoint, headers=headers)

    def get_profile(self) -> requests.Response:
        """Returns organization and current user information."""
        endpoint = "/profile"
        return self._get(endpoint)

    def _get(
        self, endpoint: str, headers: dict[str, str] | None = None
    ) -> requests.Response:
        """Sends a GET request to the server.

        Args:
            endpoint (str): The API endpoint to send the GET request to.
            headers (dict[str, str] | None): Headers to include in the request.
                If no headers are provided, the default headers will be used.
        Returns:
            requests.Response: The response from the server.
        """
        url = self._get_url(endpoint)
        request_headers = headers if headers else self.headers

        return requests.get(url, headers=request_headers, timeout=TIMEOUT)

    def _post(
        self,
        endpoint: str,
        data: Any,
        headers: dict | None = None,
    ) -> requests.Response:
        """Sends a POST request to the server with a given JSON object.

        Args:
            endpoint (str): The API endpoint to send the POST request to.
            data (Any): The JSON data to send in the request body.
            headers (dict | None): Headers to include in the request.
                If no headers are provided, the default headers will be used.
        Returns:
            requests.Response: The response from the server.
        """
        url = self._get_url(endpoint)
        request_headers = headers if headers else self.headers
        data_json = json.dumps(data)

        return requests.post(
            url, data=data_json, headers=request_headers, timeout=TIMEOUT
        )

    def _put(
        self,
        endpoint: str,
        data: Any,
        headers: dict | None = None,
    ) -> requests.Response:
        """Sends a PUT request to the server with a given JSON object.

        Args:
            endpoint (str): The API endpoint to send the PUT request to.
            data (Any): The JSON data to send in the request body.
            headers (dict | None): Headers to include in the request.
                If no headers are provided, the default headers will be used.
        Returns:
            requests.Response: The response from the server.
        """
        url = self._get_url(endpoint)
        request_headers = headers if headers else self.headers
        data_json = json.dumps(data)

        return requests.put(
            url, data=data_json, headers=request_headers, timeout=TIMEOUT
        )

    def _delete(
        self,
        endpoint: str,
    ) -> requests.Response:
        """Sends a DELETE request to the server.

        Args:
            endpoint (str): The API endpoint to send the DELETE request to.
        Returns:
            requests.Response: The response from the server.
        """
        url = self._get_url(endpoint)

        return requests.delete(url, headers=self.headers, timeout=TIMEOUT)

    @staticmethod
    def raise_if_response_not_ok(*responses: requests.Response) -> None:
        """Check if responses from API calls are OK.

        Raises ValueError if any response is not OK (status code not 2xx).
        """
        for response in responses:
            if not response.ok:
                raise ValueError(
                    f"Request to {response.url} failed with status code {response.status_code}: {response.text}"
                )
