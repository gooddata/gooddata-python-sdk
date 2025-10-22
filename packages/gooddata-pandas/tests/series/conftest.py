# (C) 2021 GoodData Corporation
import pytest
from gooddata_pandas import GoodPandas, SeriesFactory


@pytest.fixture
def gds(test_config) -> SeriesFactory:
    gdpd = GoodPandas(host=test_config["host"], token=test_config["token"])
    return gdpd.series(test_config["workspace"])
