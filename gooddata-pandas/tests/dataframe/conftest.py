# (C) 2021 GoodData Corporation
import pytest

from gooddata_pandas import GoodPandas, DataFrameFactory
from tests import TEST_HOST, get_test_token, TEST_WORKSPACE


@pytest.fixture
def gdf() -> DataFrameFactory:
    gdpd = GoodPandas(host=TEST_HOST, token=get_test_token())
    return gdpd.data_frames(TEST_WORKSPACE)
