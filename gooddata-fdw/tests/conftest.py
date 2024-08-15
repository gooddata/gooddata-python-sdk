# (C) 2021 GoodData Corporation
from collections import OrderedDict
from pathlib import Path

import pytest
import yaml
from gooddata_fdw.environment import ColumnDefinition


def pytest_addoption(parser):
    default_config_path = Path(__file__).parent / "gd_test_config.yaml"
    parser.addoption(
        "--gd-test-config",
        action="store",
        default=str(default_config_path),
        help="Absolut path to test configuration",
    )


@pytest.fixture(scope="session")
def test_config(request):
    config_path = Path(request.config.getoption("--gd-test-config"))
    with open(config_path) as f:
        config = yaml.safe_load(f)

    return config


@pytest.fixture
def fdw_options_for_insight(test_config):
    return dict(
        host=test_config["host"],
        token=test_config["token"],
        workspace=test_config["workspace"],
        insight="revenue_and_quantity_by_product_and_category",
    )


@pytest.fixture
def test_insight_columns():
    columns = OrderedDict()
    # attribute
    columns["products_category"] = ColumnDefinition(
        column_name="products_category",
        type_name="VARCHAR(255)",
        options=dict(local_id="06bc6b3b9949466494e4f594c11f1bff"),
    )
    # attribute
    columns["product_name"] = ColumnDefinition(
        column_name="product_name",
        type_name="VARCHAR(255)",
        options=dict(local_id="192668bfb6a74e9ab7b5d1ce7cb68ea3"),
    )
    # fact
    columns["quantity"] = ColumnDefinition(
        column_name="quantity",
        type_name="DECIMAL(18,2)",
        options=dict(local_id="29486504dd0e4a36a18b0b2f792d3a46"),
    )
    # fact
    columns["price"] = ColumnDefinition(
        column_name="price",
        type_name="DECIMAL(18,2)",
        options=dict(local_id="aa6391acccf1452f8011201aef9af492"),
    )
    # metric
    columns["percent_revenue_in_category"] = ColumnDefinition(
        column_name="percent_revenue_in_category",
        type_name="DECIMAL(18,1)",
        options=dict(local_id="2cd39539d8da46c9883e63caa3ba7cc0"),
    )
    # metric
    columns["revenue"] = ColumnDefinition(
        column_name="revenue",
        type_name="DECIMAL(18,2)",
        options=dict(local_id="9a0f08331c094c7facf2a0b4f418de0a"),
    )

    return columns


@pytest.fixture
def fdw_options_for_compute_table(test_config):
    return dict(
        host=test_config["host"],
        token=test_config["token"],
        workspace=test_config["workspace"],
        compute="value-does-not-matter",
    )


@pytest.fixture
def test_compute_table_columns():
    columns = OrderedDict()
    # attribute
    columns["products_category"] = ColumnDefinition(
        column_name="products_category",
        type_name="VARCHAR(255)",
        options=dict(id="label/products.category"),
    )
    # attribute
    columns["products_product_name"] = ColumnDefinition(
        column_name="products_product_name",
        type_name="VARCHAR(255)",
        options=dict(id="label/product_name"),
    )
    # fact
    columns["quantity"] = ColumnDefinition(
        column_name="quantity",
        type_name="DECIMAL(18,2)",
        options=dict(id="fact/quantity"),
    )
    # fact
    columns["price"] = ColumnDefinition(
        column_name="price",
        type_name="DECIMAL(18,2)",
        options=dict(id="fact/price"),
    )
    # metric
    columns["percent_revenue_in_category"] = ColumnDefinition(
        column_name="percent_revenue_in_category",
        type_name="DECIMAL(18,1)",
        options=dict(id="metric/percent_revenue_in_category"),
    )
    # metric
    columns["revenue"] = ColumnDefinition(
        column_name="revenue",
        type_name="DECIMAL(18,2)",
        options=dict(id="metric/revenue"),
    )

    return columns
