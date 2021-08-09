# (C) 2021 GoodData Corporation
from __future__ import annotations
import gooddata_metadata_client as metadata_client
import gooddata_afm_client as afm_client

USER_AGENT = "gooddata-python-sdk/0.1"


class GoodDataApiClient:
    def __init__(self, host, token, extra_user_agent=None):
        self._hostname = host
        self._token = token

        user_agent = (
            f"{USER_AGENT} {extra_user_agent}"
            if extra_user_agent is not None
            else USER_AGENT
        )

        self._metadata_config = metadata_client.Configuration(host=host)
        self._metadata_client = metadata_client.ApiClient(
            configuration=self._metadata_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._metadata_client.default_headers["X-Requested-With"] = "XMLHttpRequest"
        self._metadata_client.user_agent = user_agent

        self._afm_config = afm_client.Configuration(host=host)
        self._afm_client = afm_client.ApiClient(
            configuration=self._afm_config,
            header_name="Authorization",
            header_value=f"Bearer {token}",
        )
        self._afm_client.default_headers["X-Requested-With"] = "XMLHttpRequest"
        self._afm_client.user_agent = user_agent

    @property
    def afm_client(self):
        return self._afm_client

    @property
    def metadata_client(self):
        return self._metadata_client
