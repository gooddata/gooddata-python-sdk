# (C) 2023 GoodData Corporation
from __future__ import annotations

import json
from pathlib import Path


def load_json(path: Path):
    with open(path, encoding="utf8") as f:
        return json.load(f)
