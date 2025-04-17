# (C) 2022 GoodData Corporation
from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Union

import pytest
import yaml
from gooddata_sdk import GoodDataSdk

_current_dir = Path(__file__).parent.absolute()
PROFILES_PATH = _current_dir / "profiles" / "profiles.yaml"
AAC_PROFILES_PATH = _current_dir / "profiles" / "gooddata.yaml"
CORRUPTED_PROFILES = _current_dir / "profiles" / "corrupted.yaml"


def load_profiles_content(path: Union[str, Path]) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def are_same_check(profile_data: dict[str, Any], sdk: GoodDataSdk):
    assert profile_data["host"] == sdk.client._hostname
    assert profile_data["token"] == sdk.client._token
    if "custom_headers" in profile_data:
        assert profile_data["custom_headers"] == sdk.client._custom_headers
    if "extra_user_agent" in profile_data:
        assert profile_data["extra_user_agent"] in sdk.client._api_client.user_agent


@pytest.mark.parametrize(
    "profile",
    [
        "custom",
        "default",
        "correct_1",
        "correct_2",
        "correct_3",
        "correct_4",
    ],
)
def test_legacy_config(profile):
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content(PROFILES_PATH)
    are_same_check(data[profile], sdk)


def test_legacy_wrong_profile():
    profile = "wrong"
    with pytest.raises(ValueError):
        GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)


def test_new_config_default(setenvvar):
    sdk = GoodDataSdk.create_from_profile(profiles_path=AAC_PROFILES_PATH)
    data = load_profiles_content(AAC_PROFILES_PATH)
    profile = data["default_profile"]
    profile_data = data["profiles"][profile]
    assert profile_data["host"] == sdk.client._hostname
    assert os.environ[profile_data["token"][1:]] == sdk.client._token


def test_new_config_selected(setenvvar):
    profile = "xyz"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=AAC_PROFILES_PATH)
    data = load_profiles_content(AAC_PROFILES_PATH)
    profile_data = data["profiles"][profile]
    assert profile_data["host"] == sdk.client._hostname
    assert os.environ[profile_data["token"][1:]] == sdk.client._token


def test_non_existing_token(setenvvar):
    profile = "def"
    with pytest.raises(ValueError):
        GoodDataSdk.create_from_profile(profile=profile, profiles_path=AAC_PROFILES_PATH)


def test_corrupted_config():
    with pytest.raises(ValueError):
        GoodDataSdk.create_from_profile(profiles_path=CORRUPTED_PROFILES)


def test_new_options(setenvvar):
    sdk1 = GoodDataSdk.create("host", "token", "agent_foo", header1="header1", header2="header2")
    assert sdk1._client._hostname == "host"
    assert sdk1._client._token == "token"
    assert sdk1._client._api_client.user_agent[-9:] == "agent_foo"
    assert sdk1._client._custom_headers == {"header1": "header1", "header2": "header2"}
    assert not sdk1._client.executions_cancellable

    sdk2 = GoodDataSdk.create(
        "host", "token", "agent_foo", header1="header1", executions_cancellable=True, header2="header2"
    )
    assert sdk1._client._hostname == sdk2._client._hostname
    assert sdk1._client._token == sdk2._client._token
    assert sdk1._client._api_client.user_agent == sdk2._client._api_client.user_agent
    assert sdk1._client._custom_headers == sdk2._client._custom_headers
    assert sdk2._client.executions_cancellable

    sdk3 = GoodDataSdk.create(
        "host", "token", "agent_foo", executions_cancellable=True, header1="header1", header2="header2"
    )
    assert sdk1._client._api_client.user_agent == sdk3._client._api_client.user_agent
    assert sdk1._client._custom_headers == sdk3._client._custom_headers
    assert sdk3._client.executions_cancellable

    sdk4 = GoodDataSdk.create(
        "host", "token", "agent_foo", header1="header1", header2="header2", executions_cancellable=True
    )
    assert sdk1._client._api_client.user_agent == sdk4._client._api_client.user_agent
    assert sdk1._client._custom_headers == sdk4._client._custom_headers
    assert sdk4._client.executions_cancellable
