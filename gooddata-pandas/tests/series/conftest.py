# (C) 2021 GoodData Corporation
import pytest

from gooddata_pandas import GoodPandas, SeriesFactory
from tests import TEST_HOST, TEST_WORKSPACE, get_test_token


@pytest.fixture
def gds() -> SeriesFactory:
    gdpd = GoodPandas(host=TEST_HOST, token=get_test_token())
    return gdpd.series(TEST_WORKSPACE)
