# (C) 2021 GoodData Corporation
import pytest
from gooddata_pandas import DataFrameFactory, GoodPandas


@pytest.fixture
def gdf(test_config) -> DataFrameFactory:
    gdpd = GoodPandas(host=test_config["host"], token=test_config["token"])
    return gdpd.data_frames(test_config["workspace"])
