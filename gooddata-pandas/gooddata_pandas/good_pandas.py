# (C) 2021 GoodData Corporation
from __future__ import annotations
import os
import json
from gooddata_sdk import GoodDataSdk, client as sdk_client
from gooddata_pandas.series import SeriesFactory
from gooddata_pandas.dataframe import DataFrameFactory


_USER_AGENT = "gooddata-pandas/0.1"


class GoodPandas:
    """
    Facade to access factories that create pandas Series and DataFrames using analytics computed by GoodData.CN.
    """

    def __init__(self, host, token):
        self._sdk = _create_sdk(host, token)
        self._series_per_ws = dict()
        self._frames_per_ws = dict()

    def series(self, workspace_id):
        """
        Creates factory to use for construction of pandas.Series.

        :param workspace_id: workspace to which the factory will be bound
        :return: always one same instance for given workspace
        :rtype: SeriesFactory
        """
        if workspace_id not in self._series_per_ws:
            self._series_per_ws[workspace_id] = SeriesFactory(
                sdk=self._sdk, workspace_id=workspace_id
            )

        return self._series_per_ws[workspace_id]

    def data_frames(self, workspace_id):
        """
        Creates factory to use for construction of pandas.DataFrame.

        :param workspace_id: workspace to which the factory will be bound
        :return: always one same instance for given workspace
        :rtype: DataFrameFactory
        """
        if workspace_id not in self._frames_per_ws:
            self._frames_per_ws[workspace_id] = DataFrameFactory(
                sdk=self._sdk, workspace_id=workspace_id
            )

        return self._frames_per_ws[workspace_id]


def _create_sdk(host, token):
    """Return GoodDataSdk instance."""
    headers = os.environ.get("GOODDATA_SDK_HTTP_HEADERS", None)
    if headers:
        try:
            headers = json.loads(headers)
            assert isinstance(headers, dict), "Not a dictionary"
        except (AssertionError, json.JSONDecodeError) as e:
            text = (
                "environment variable GOODDATA_SDK_HTTP_HEADERS contains data in bad format. "
                "Json object expected."
            )
            raise ValueError(text) from e
    client = sdk_client.GoodDataApiClient(
        host, token, custom_headers=headers, extra_user_agent=_USER_AGENT
    )
    return GoodDataSdk(client)
