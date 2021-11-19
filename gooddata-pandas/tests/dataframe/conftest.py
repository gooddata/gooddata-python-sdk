# (C) 2021 GoodData Corporation
import pytest

from gooddata_pandas import DataFrameFactory, GoodPandas
from tests import TEST_HOST, TEST_WORKSPACE, get_test_token


@pytest.fixture
def gdf() -> DataFrameFactory:
    gdpd = GoodPandas(host=TEST_HOST, token=get_test_token())
    return gdpd.data_frames(TEST_WORKSPACE)
