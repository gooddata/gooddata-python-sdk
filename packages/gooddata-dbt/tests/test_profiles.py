# (C) 2023 GoodData Corporation
import argparse
from pathlib import Path

from gooddata_dbt.dbt.profiles import DbtOutputSnowflake, DbtProfiles
from gooddata_sdk import BasicCredentials, KeyPairCredentials

_CURR_DIR = Path(__file__).parent


def test_profiles():
    dbt_profiles = DbtProfiles(argparse.Namespace(profiles_dir=_CURR_DIR / "resources/dbt_profiles"))
    profiles = dbt_profiles.profiles
    assert len(profiles) == 1
    default_profile = profiles[0]
    assert default_profile.name == "default"
    assert len(default_profile.outputs) == 6


def _snowflake_output(**overrides) -> DbtOutputSnowflake:
    defaults = dict(
        name="cicd_dev",
        title="CICD demo (dev)",
        account="gooddata",
        user="cicd",
        database="CICD_DEV",
        warehouse="DEMO_WH",
        schema="cicd_input_stage",
    )
    defaults.update(overrides)
    return DbtOutputSnowflake.from_dict(defaults)


def test_snowflake_password_auth_unchanged():
    output = _snowflake_output(password="xxxxx")
    data_source = output.to_gooddata("snowflake-ds", "cicd_input_stage")
    assert isinstance(data_source.credentials, BasicCredentials)
    assert data_source.credentials.password == "xxxxx"


def test_snowflake_key_pair_auth_from_private_key():
    output = _snowflake_output(private_key="-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----")
    data_source = output.to_gooddata("snowflake-ds", "cicd_input_stage")
    assert isinstance(data_source.credentials, KeyPairCredentials)
    assert data_source.credentials.private_key.startswith("-----BEGIN PRIVATE KEY-----")


def test_snowflake_key_pair_auth_from_private_key_path(tmp_path):
    key_file = tmp_path / "rsa_key.p8"
    key_file.write_text("-----BEGIN PRIVATE KEY-----\nabc\n-----END PRIVATE KEY-----")
    output = _snowflake_output(private_key_path=str(key_file))
    data_source = output.to_gooddata("snowflake-ds", "cicd_input_stage")
    assert isinstance(data_source.credentials, KeyPairCredentials)
    assert data_source.credentials.private_key == key_file.read_text()


def test_inject_env_vars_empty_default_unset(monkeypatch):
    # env_var(..., '') is how profiles.yml opts an optional field like private_key_path out by
    # default - the [^']+ -> [^']* regex fix is what makes this resolve at all instead of leaving
    # the raw "{{ env_var(...) }}" string in place.
    monkeypatch.delenv("SNOWFLAKE_PRIVATE_KEY_PATH", raising=False)
    output_def = {"private_key_path": "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PATH', '') }}"}
    DbtProfiles.inject_env_vars(output_def)
    assert output_def["private_key_path"] == ""


def test_inject_env_vars_empty_default_set(monkeypatch, tmp_path):
    key_file = tmp_path / "rsa_key.p8"
    monkeypatch.setenv("SNOWFLAKE_PRIVATE_KEY_PATH", str(key_file))
    output_def = {"private_key_path": "{{ env_var('SNOWFLAKE_PRIVATE_KEY_PATH', '') }}"}
    DbtProfiles.inject_env_vars(output_def)
    assert output_def["private_key_path"] == str(key_file)


def test_inject_env_vars_non_empty_default_unchanged(monkeypatch):
    monkeypatch.delenv("SNOWFLAKE_PASS", raising=False)
    output_def = {"password": "{{ env_var('SNOWFLAKE_PASS', 'xxxxx') }}"}
    DbtProfiles.inject_env_vars(output_def)
    assert output_def["password"] == "xxxxx"
