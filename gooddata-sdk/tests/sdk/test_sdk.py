# (C) 2022 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from gooddata_sdk import GoodDataSdk

_current_dir = Path(__file__).parent.absolute()
PROFILES_PATH = _current_dir / "profiles" / "profiles.yaml"


def load_profiles_content() -> dict:
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def are_same_check(profile_data: dict[str, Any], sdk: GoodDataSdk):
    assert profile_data["host"] == sdk.client._hostname
    assert profile_data["token"] == sdk.client._token
    if "custom_headers" in profile_data:
        assert profile_data["custom_headers"] == sdk.client._custom_headers
    if "extra_user_agent" in profile_data:
        assert profile_data["extra_user_agent"] in sdk.client._api_client.user_agent


def test_default_profile():
    profile = "default"
    sdk = GoodDataSdk.create_from_profile(profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_other_profile():
    profile = "custom"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_wrong_profile():
    profile = "wrong"
    try:
        GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    except ValueError:
        assert True
    else:
        assert False, "The ValueError was expected to be raised."


def test_correct_1_profile():
    profile = "correct_1"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_2_profile():
    profile = "correct_2"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_3_profile():
    profile = "correct_3"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_4_profile():
    profile = "correct_4"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)
