# (C) 2023 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from gooddata_pandas import GoodPandas

_current_dir = Path(__file__).parent.absolute()
PROFILES_PATH = _current_dir / "profiles" / "profiles.yaml"


def load_profiles_content() -> dict:
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def are_same_check(profile_data: dict[str, Any], good_pandas: GoodPandas):
    assert profile_data["host"] == good_pandas.sdk.client._hostname
    assert profile_data["token"] == good_pandas.sdk.client._token
    if "custom_headers" in profile_data:
        assert profile_data["custom_headers"] == good_pandas.sdk.client._custom_headers


def test_default_profile():
    profile = "default"
    good_pandas = GoodPandas.create_from_profile(profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], good_pandas)


def test_other_profile():
    profile = "custom"
    good_pandas = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], good_pandas)


def test_wrong_profile():
    profile = "wrong"
    try:
        GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    except ValueError:
        assert True
    else:
        assert False, "The ValueError was expected to be raised."


def test_correct_1_profile():
    profile = "correct_1"
    sdk = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_2_profile():
    profile = "correct_2"
    sdk = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_3_profile():
    profile = "correct_3"
    sdk = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)


def test_correct_4_profile():
    profile = "correct_4"
    sdk = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    are_same_check(data[profile], sdk)
