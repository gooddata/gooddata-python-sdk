# (C) 2022 GoodData Corporation
import os
from pathlib import Path
from unittest import mock

import pytest
import yaml


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


@pytest.fixture()
def setenvvar(monkeypatch):
    with mock.patch.dict(os.environ, clear=True):
        envvars = {"OK_TOKEN": "secret_password", "ENV_VAR": "secret"}
        for k, v in envvars.items():
            monkeypatch.setenv(k, v)
        yield
