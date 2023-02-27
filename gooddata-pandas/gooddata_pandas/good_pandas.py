# (C) 2021 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Optional

from gooddata_pandas import __version__
from gooddata_pandas.dataframe import DataFrameFactory
from gooddata_pandas.series import SeriesFactory
from gooddata_sdk import GoodDataSdk
from gooddata_sdk.utils import PROFILES_FILE_PATH, good_pandas_profile_content

USER_AGENT = f"gooddata-pandas/{__version__}"
"""Extra segment of the User-Agent header that will be appended to standard gooddata-sdk user agent."""


class GoodPandas:
    """
    Facade to access factories that create pandas Series and DataFrames using analytics computed by GoodData.CN.
    """

    def __init__(
        self,
        host: str,
        token: str,
        headers_host: Optional[str] = None,
        **custom_headers_: Optional[str],
    ) -> None:
        if headers_host is not None:
            custom_headers_["Host"] = headers_host
        self._sdk = GoodDataSdk.create(host, token, USER_AGENT, **custom_headers_)
        self._series_per_ws: dict[str, SeriesFactory] = dict()
        self._frames_per_ws: dict[str, DataFrameFactory] = dict()

    @classmethod
    def create_from_profile(cls, profile: str = "default", profiles_path: Path = PROFILES_FILE_PATH) -> GoodPandas:
        content, custom_headers = good_pandas_profile_content(profile, profiles_path)
        return cls(**content, **custom_headers)

    @property
    def sdk(self) -> GoodDataSdk:
        return self._sdk

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
