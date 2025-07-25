# (C) 2025 GoodData Corporation

"""Interaction with GoodData Cloud via the direct API calls."""

import json
from typing import Any

import requests

# TODO: Limit the use of "typing.Any". Improve readability by using either models
#  or typed dicts.

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

    def get_custom_application_setting(
        self, workspace_id: str, setting_id: str
    ) -> requests.Response:
        """Gets a custom application setting.

        Args:
            workspace_id (str): The ID of the workspace.
            setting_id (str): The ID of the custom application setting.
        Returns:
            requests.Response: The response from the server containing the
                custom application setting.
        """
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/{setting_id}"
        return self._get(url)

    def put_custom_application_setting(
        self, workspace_id: str, setting_id: str, data: dict[str, Any]
    ) -> requests.Response:
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/{setting_id}"
        return self._put(url, data, self.headers)

    def post_custom_application_setting(
        self, workspace_id: str, data: dict[str, Any]
    ) -> requests.Response:
        """Creates a custom application setting for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace.
            data (dict[str, Any]): The data for the custom application setting.
        Returns:
            requests.Response: The response from the server containing the
                created custom application setting.
        """
        url = f"/entities/workspaces/{workspace_id}/customApplicationSettings/"
        return self._post(url, data, self.headers)

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

    def post_workspace_data_filter(
        self, workspace_id: str, data: dict[str, Any]
    ) -> requests.Response:
        """Creates a workspace data filter for a given workspace.

        Args:
            workspace_id (str): The ID of the workspace.
            data (dict[str, Any]): The data for the workspace data filter.
        Returns:
            requests.Response: The response from the server containing the
                created workspace data filter.
        """
        endpoint = f"/entities/workspaces/{workspace_id}/workspaceDataFilters"
        return self._post(endpoint, data, self.headers)

    def get_user_data_filters(self, workspace_id: str) -> requests.Response:
        """Gets the user data filters for a given workspace."""
        endpoint = f"/layout/workspaces/{workspace_id}/userDataFilters"
        return self._get(endpoint)

    def get_automations(self, workspace_id: str) -> requests.Response:
        """Gets the automations for a given workspace."""
        endpoint = (
            f"/entities/workspaces/{workspace_id}/automations?include=ALL"
        )
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
