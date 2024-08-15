# (C) 2023 GoodData Corporation
from __future__ import annotations

from pathlib import Path
from typing import Any, Union

import pytest
import yaml
from gooddata_pandas import GoodPandas

_current_dir = Path(__file__).parent.absolute()
PROFILES_PATH = _current_dir / "profiles" / "profiles.yaml"


def load_profiles_content(path: Union[str, Path]) -> dict:
    with open(path, encoding="utf-8") as f:
        return yaml.safe_load(f)


def are_same_check(profile_data: dict[str, Any], good_pandas: GoodPandas):
    assert profile_data["host"] == good_pandas.sdk.client._hostname
    assert profile_data["token"] == good_pandas.sdk.client._token
    if "custom_headers" in profile_data:
        assert profile_data["custom_headers"] == good_pandas.sdk.client._custom_headers


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
    good_pandas = GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
    data = load_profiles_content(PROFILES_PATH)
    are_same_check(data[profile], good_pandas)


def test_wrong_profile():
    profile = "wrong"
    with pytest.raises(ValueError):
        GoodPandas.create_from_profile(profile=profile, profiles_path=PROFILES_PATH)
