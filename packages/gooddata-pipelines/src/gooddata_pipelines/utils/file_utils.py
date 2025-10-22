# (C) 2025 GoodData Corporation

import json
from pathlib import Path
from typing import Any

import attrs
import yaml


class PathUtils:
    """Handles common path operations."""

    @staticmethod
    def validate_path(path: str | Path) -> Path:
        """Validates a path."""
        if not isinstance(path, Path):
            path = Path(path)

        return path

    def check_path_exists(self, path: Path) -> None:
        """Checks if a path exists."""
        if not self.validate_path(path).exists():
            raise FileNotFoundError(f"File {path} does not exist.")


@attrs.define
class JsonUtils:
    """Handles common JSON interactions."""

    path_utils: PathUtils = attrs.field(factory=PathUtils)

    def load(self, path: Path) -> Any:
        """Loads a JSON file."""
        self.path_utils.check_path_exists(path)

        with open(path, "r") as f:
            return json.load(f)

    def dump(self, path: Path, data: Any) -> None:
        """Writes the source to a JSON file."""
        with open(path, "w") as output_file:
            json.dump(data, output_file)


@attrs.define
class YamlUtils:
    """Handles common YMAL interactions."""

    path_utils: PathUtils = attrs.field(factory=PathUtils)

    def safe_load(self, path: Path) -> Any:
        """Safe loads a YAML file."""
        self.path_utils.check_path_exists(path)

        with open(path, "r") as f:
            return yaml.safe_load(f)

    def dump(self, path: str, data: Any) -> None:
        """Writes the source to a YAML file."""
        with open(path, "w") as output_file:
            yaml.dump(data, output_file)
