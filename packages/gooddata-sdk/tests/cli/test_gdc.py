# (C) 2026 GoodData Corporation
from __future__ import annotations

from pathlib import Path

import pytest
import yaml
from gooddata_sdk.cli.constants import DEFAULT_SOURCE_DIR
from gooddata_sdk.cli.deploy import _get_workspace_id
from gooddata_sdk.cli.gdc_core import _get_source_dir

_FIXTURES_DIR = Path(__file__).parent.parent / "catalog" / "fixtures" / "aac"


class TestCliConfig:
    def test_get_source_dir_from_config(self) -> None:
        source_dir = _get_source_dir(_FIXTURES_DIR / "gooddata.yaml")
        assert source_dir == "analytics"

    def test_get_source_dir_default(self, tmp_path: Path) -> None:
        """When source_dir is not in config, fall back to default."""
        config = {
            "profiles": {"default": {"host": "https://h", "token": "t"}},
            "default_profile": "default",
        }
        config_path = tmp_path / "gooddata.yaml"
        config_path.write_text(yaml.dump(config))
        source_dir = _get_source_dir(config_path)
        assert source_dir == DEFAULT_SOURCE_DIR

    def test_get_workspace_id(self) -> None:
        workspace_id = _get_workspace_id(_FIXTURES_DIR / "gooddata.yaml")
        assert workspace_id == "test-workspace"

    def test_get_workspace_id_missing(self, tmp_path: Path) -> None:
        """Raise error when workspace_id is not set in profile."""
        config = {
            "profiles": {"default": {"host": "https://h", "token": "t"}},
            "default_profile": "default",
        }
        config_path = tmp_path / "gooddata.yaml"
        config_path.write_text(yaml.dump(config))
        with pytest.raises(ValueError, match="workspace_id"):
            _get_workspace_id(config_path)

    def test_no_nodejs_dependency(self) -> None:
        """Ensure no Node.js artifacts remain in the CLI module."""
        cli_dir = Path(__file__).parent.parent.parent / "src" / "gooddata_sdk" / "cli"
        assert not (cli_dir / "package.json").exists()
