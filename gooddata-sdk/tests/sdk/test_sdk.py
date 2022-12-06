# (C) 2022 GoodData Corporation
from pathlib import Path

import yaml

from gooddata_sdk import GoodDataSdk

_current_dir = Path(__file__).parent.absolute()
PROFILES_PATH = _current_dir / "profiles" / "profiles.yaml"


def load_profiles_content() -> dict:
    with open(PROFILES_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def test_default_profile():
    profile = "default"
    sdk = GoodDataSdk.create_from_profile(profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    assert data[profile]["host"] == sdk.client._hostname
    assert data[profile]["token"] == sdk.client._token
    assert data[profile]["custom_headers"] == sdk.client._custom_headers
    assert data[profile]["extra_user_agent"] in sdk.client._api_client.user_agent


def test_other_profile():
    profile = "custom"
    sdk = GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content()

    assert data[profile]["host"] == sdk.client._hostname
    assert data[profile]["token"] == sdk.client._token
    assert data[profile]["custom_headers"] == sdk.client._custom_headers
    assert data[profile]["extra_user_agent"] in sdk.client._api_client.user_agent


def test_wrong_profile():
    profile = "wrong"
    try:
        GoodDataSdk.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    except ValueError:
        assert True
    else:
        assert False, "The ValueError was expected to be raised."
