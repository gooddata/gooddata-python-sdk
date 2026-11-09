# (C) 2026 GoodData Corporation
from gooddata_dbt.gooddata.config import GoodDataConfig

_CONFIG = {
    "environment_setups": [
        {
            "id": "default",
            "environments": [
                {"id": "dev", "name": "Dev", "early_access_values": ["flag_dev"]},
                {"id": "prod", "name": "Prod"},
            ],
        }
    ],
    "data_products": [
        {"id": "sales", "name": "Sales", "environment_setup_id": "default"},
        {"id": "mkt", "name": "Marketing", "environment_setup_id": "default", "early_access_values": ["flag_a"]},
        {"id": "ops", "name": "Ops", "environment_setup_id": "default", "early_access_values": []},
    ],
    "organizations": [{"gooddata_profile": "local", "data_product_ids": ["sales", "mkt", "ops"]}],
    "global_properties": {},
}


def test_early_access_values_resolution():
    config = GoodDataConfig.from_dict(_CONFIG)
    sales, mkt, ops = config.data_products
    dev, prod = config.get_environment_workspaces("default")

    # not configured anywhere -> None, the existing workspace value is kept
    assert sales.get_early_access_values(prod) is None
    # data product level is used in environments without an override
    assert mkt.get_early_access_values(prod) == ["flag_a"]
    # an empty list is kept as is (disables all features), not treated as "not configured"
    assert ops.get_early_access_values(prod) == []
    # environment level overrides data product level
    assert mkt.get_early_access_values(dev) == ["flag_dev"]
    assert sales.get_early_access_values(dev) == ["flag_dev"]
