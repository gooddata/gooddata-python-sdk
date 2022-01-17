# (C) 2021 GoodData Corporation
from pathlib import Path

import pytest
import yaml


def pytest_addoption(parser):
    default_config_path = Path(__file__).parent / "gd_test_config.yaml"
    parser.addoption(
        "--gd-test-config",
        action="store",
        default=str(default_config_path),
        help="Absolut path to an application charts",
    )


@pytest.fixture(scope="session")
def test_config(request):
    config_path = Path(request.config.getoption("--gd-test-config"))
    with open(config_path, "rt") as f:
        config = yaml.safe_load(f)

    return config
