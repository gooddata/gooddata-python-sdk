# (C) 2025 GoodData Corporation

"""Wrapper for interaction with GoodData Cloud."""

from gooddata_sdk.sdk import GoodDataSdk

from gooddata_pipelines.api.gooddata_api import ApiMethods


# TODO: Refactor the GoodDataApi class to use composition instead of inheritance.
class GoodDataApi(ApiMethods):
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
        self._domain: str = self._get_clean_host(host)
        self._token: str = token

        # Initialize the GoodData SDK
        self._sdk = GoodDataSdk.create(self._domain, self._token)

        # Set up utils for direct API interaction
        self.base_url = self._get_base_url(self._domain)
        self.headers: dict = {
            "Authorization": f"Bearer {self._token}",
            "Content-Type": "application/vnd.gooddata.api+json",
        }

    @staticmethod
    def _get_clean_host(host: str) -> str:
        """Returns a clean URL of the GoodData Cloud host.

        Method ensures that the URL starts with "https://" and does not
        end with a trailing slash.
        """

        if host is None:
            raise RuntimeError("Host is not set. Please provide a valid host.")

        if host == "":
            raise ValueError(
                "Host is an empty string. Please provide a valid host."
            )

        # Remove trailing slash if present.
        if host[-1] == "/":
            host = host[:-1]

        if not host.startswith("https://") and not host.startswith("http://"):
            host = f"https://{host}"

        if host.startswith("http://") and not host.startswith("https://"):
            host = host.replace("http://", "https://")

        return host
