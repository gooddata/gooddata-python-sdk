# (C) 2025 GoodData Corporation

"""Wrapper for interaction with GoodData Cloud."""

from gooddata_sdk.sdk import GoodDataSdk

from gooddata_pipelines.api.gooddata_api import ApiMethods
from gooddata_pipelines.api.gooddata_sdk import SdkMethods


class GoodDataApi(SdkMethods, ApiMethods):
    """Wrapper class for the GoodData Cloud API.

    This class combines interactions with the GoodData Python SDK and direct API
    calls.
    """

    def __init__(self, host: str, token: str) -> None:
        """Initialize the GoodDataApi with host and token.

        Args:
            host (str): The GoodData Cloud host URL.
            token (str): The authentication token for the GoodData Cloud API.
        """
        self._domain: str = host
        self._token: str = token

        # Initialize the GoodData SDK
        self._sdk = GoodDataSdk.create(self._domain, self._token)

        # Set up utils for direct API interaction
        self.base_url = self._get_base_url(self._domain)
        self.headers: dict = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/vnd.gooddata.api+json",
        }
