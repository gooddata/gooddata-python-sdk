# (C) 2026 GoodData Corporation
"""Validated run configuration produced by the CLI and consumed by the runner."""

from dataclasses import dataclass
from pathlib import Path


@dataclass
class RunConfig:
    host: str
    token: str
    workspace_id: str
    dataset_folder: Path | None = None
    langfuse_dataset: str | None = None
    model: str | None = None
    provider_id: str | None = None
    runs: int = 2
    json_path: Path | None = None
    log_to_langfuse: bool = False
    quiet: bool = False
