# (C) 2021 GoodData Corporation
from collections import OrderedDict

import pytest

from gooddata_fdw.environment import ColumnDefinition
from tests import TEST_HOST, get_test_token, TEST_WORKSPACE


@pytest.fixture
def import_srv_options():
    return dict(host=TEST_HOST, token=get_test_token())


@pytest.fixture
def fdw_options_for_insight():
    return dict(
        host=TEST_HOST,
        token=get_test_token(),
        workspace=TEST_WORKSPACE,
        insight="f7fef745-7269-454e-982e-e1d7d3eed81f",
    )


@pytest.fixture
def test_insight_columns():
    columns = OrderedDict()
    columns["car_car_make"] = ColumnDefinition(
        column_name="car_car_make",
        type_name="VARCHAR(256)",
        options=dict(local_id="bb6895568384411a909514dd5b95011f"),
    )
    columns["customer_customer_age_group"] = ColumnDefinition(
        column_name="customer_customer_age_group",
        type_name="VARCHAR(256)",
        options=dict(local_id="b08cd137253d405f803601bf12fa89cb"),
    )
    columns["premium_revenue"] = ColumnDefinition(
        column_name="premium_revenue",
        type_name="DECIMAL(15,5)",
        options=dict(local_id="0b3a3a4a6e2547259725e18e64033620"),
    )

    return columns


@pytest.fixture
def fdw_options_for_compute_table():
    return dict(
        host=TEST_HOST,
        token=get_test_token(),
        workspace=TEST_WORKSPACE,
        compute="value-does-not-matter",
    )


@pytest.fixture
def test_compute_table_columns():
    columns = OrderedDict()
    columns["coverage_lifetime"] = ColumnDefinition(
        column_name="coverage_lifetime",
        type_name="DECIMAL(15,5)",
        options=dict(id="fact/coverage.coverage_lifetime"),
    )
    columns["claim_amount"] = ColumnDefinition(
        column_name="claim_amount",
        type_name="DECIMAL(15,5)",
        options=dict(id="metric/claim-amount"),
    )
    columns["car_make"] = ColumnDefinition(
        column_name="car_make",
        type_name="VARCHAR(256)",
        options=dict(id="label/car.car_make"),
    )
    columns["car_model"] = ColumnDefinition(
        column_name="car_model",
        type_name="VARCHAR(256)",
        options=dict(id="label/car.car_model"),
    )

    return columns
