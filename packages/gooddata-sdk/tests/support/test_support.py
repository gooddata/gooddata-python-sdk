# (C) 2022 GoodData Corporation
from __future__ import annotations

import time
from pathlib import Path

import pytest
from gooddata_sdk import GoodDataSdk
from tests_support.vcrpy_utils import get_vcr

gd_vcr = get_vcr()

_current_dir = Path(__file__).parent.absolute()
_fixtures_dir = _current_dir / "fixtures"


@gd_vcr.use_cassette(str(_fixtures_dir / "is_available.yaml"))
def test_is_available(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    assert sdk.support.is_available


def test_is_not_available(test_config):
    sdk = GoodDataSdk.create(host_="http://nonsense:1234", token_="1234")
    assert not sdk.support.is_available


@gd_vcr.use_cassette(str(_fixtures_dir / "is_available_no_access.yaml"))
def test_is_available_no_access(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_="1234")
    with pytest.raises(Exception):
        assert sdk.support.is_available


@gd_vcr.use_cassette(str(_fixtures_dir / "wait_till_available_no_wait.yaml"))
def test_wait_till_available_no_wait(test_config):
    sdk = GoodDataSdk.create(host_=test_config["host"], token_=test_config["token"])
    start_time = time.time()
    sdk.support.wait_till_available(3)
    assert (time.time() - start_time) < 1000


def test_wait_till_available_timeout(test_config):
    sdk = GoodDataSdk.create(host_="http://nonsense:1234", token_="1234")
    start_time = time.time()
    with pytest.raises(TimeoutError):
        sdk.support.wait_till_available(3)
    assert 4 > (time.time() - start_time) > 3
