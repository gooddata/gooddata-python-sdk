# (C) 2021 GoodData Corporation
from __future__ import annotations

from typing import Optional

from gooddata_pandas.dataframe import DataFrameFactory
from gooddata_pandas.series import SeriesFactory
from gooddata_sdk import create_sdk

_USER_AGENT = "gooddata-pandas/0.1"


class GoodPandas:
    """
    Facade to access factories that create pandas Series and DataFrames using analytics computed by GoodData.CN.
    """

    def __init__(self, host: str, token: str, headers_host: Optional[str] = None) -> None:
        self._sdk = create_sdk(host, token, _USER_AGENT, headers_host)
        self._series_per_ws: dict[str, SeriesFactory] = dict()
        self._frames_per_ws: dict[str, DataFrameFactory] = dict()

    def series(self, workspace_id: str) -> SeriesFactory:
        """
        Creates factory to use for construction of pandas.Series.

        :param workspace_id: workspace to which the factory will be bound
        :return: always one same instance for given workspace
        """
        if workspace_id not in self._series_per_ws:
            self._series_per_ws[workspace_id] = SeriesFactory(sdk=self._sdk, workspace_id=workspace_id)

        return self._series_per_ws[workspace_id]

    def data_frames(self, workspace_id: str) -> DataFrameFactory:
        """
        Creates factory to use for construction of pandas.DataFrame.

        :param workspace_id: workspace to which the factory will be bound
        :return: always one same instance for given workspace
        """
        if workspace_id not in self._frames_per_ws:
            self._frames_per_ws[workspace_id] = DataFrameFactory(sdk=self._sdk, workspace_id=workspace_id)

        return self._frames_per_ws[workspace_id]
