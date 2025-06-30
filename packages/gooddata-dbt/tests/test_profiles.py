# (C) 2023 GoodData Corporation
import argparse
from pathlib import Path

from gooddata_dbt.dbt.profiles import DbtProfiles

_CURR_DIR = Path(__file__).parent


def test_profiles():
    dbt_profiles = DbtProfiles(argparse.Namespace(profiles_dir=_CURR_DIR / "resources/dbt_profiles"))
    profiles = dbt_profiles.profiles
    assert len(profiles) == 1
    default_profile = profiles[0]
    assert default_profile.name == "default"
    assert len(default_profile.outputs) == 6
