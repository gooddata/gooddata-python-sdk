# (C) 2026 GoodData Corporation
import sys

from gooddata_dbt.args import parse_arguments


def test_parse_arguments_deploy_ldm_second_granularities(monkeypatch):
    monkeypatch.setattr(sys, "argv", ["gooddata-dbt", "deploy_ldm"])
    assert parse_arguments("test").gooddata_enable_second_granularities is False

    monkeypatch.setattr(sys, "argv", ["gooddata-dbt", "deploy_ldm", "--gooddata-enable-second-granularities"])
    assert parse_arguments("test").gooddata_enable_second_granularities is True
