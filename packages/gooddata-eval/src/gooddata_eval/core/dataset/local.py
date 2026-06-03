# (C) 2026 GoodData Corporation
"""Load a dataset from a flat folder of one-JSON-per-question files."""

from pathlib import Path

import orjson

from gooddata_eval.core.models import DatasetItem


def load_local_dataset(folder: Path) -> list[DatasetItem]:
    """Read every `*.json` file in `folder` into a DatasetItem.

    Args:
        folder: Directory containing one JSON file per question.

    Returns:
        Parsed dataset items, sorted by file name for stable ordering.

    Raises:
        FileNotFoundError: The folder does not exist.
        ValueError: The folder contains no `.json` files, or a file is invalid.
    """
    folder = Path(folder)
    if not folder.is_dir():
        raise FileNotFoundError(f"Dataset folder not found: {folder}")

    json_files = sorted(folder.glob("*.json"))
    if not json_files:
        raise ValueError(f"Dataset folder contains no .json files: {folder}")

    items: list[DatasetItem] = []
    for path in json_files:
        try:
            raw = orjson.loads(path.read_bytes())
        except orjson.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in dataset file {path}: {e}") from e
        items.append(DatasetItem.model_validate(raw))
    return items
