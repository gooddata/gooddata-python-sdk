# (C) 2026 GoodData Corporation
"""Validated run configuration produced by the CLI and consumed by the runner."""

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class RunConfig:
    host: str
    token: str
    workspace_id: str
    dataset_folder: Path | None = None
    langfuse_dataset: str | None = None
    models: list[str] = field(default_factory=list)
    runs: int = 2
    concurrency: int = 1
    json_path: Path | None = None
    log_to_langfuse: bool = False
    quiet: bool = False
    kind: str = "visualization"
