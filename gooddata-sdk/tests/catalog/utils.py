# (C) 2022 GoodData Corporation
from __future__ import annotations

import os
from pathlib import Path


def create_directory(path: Path) -> None:
    if not os.path.exists(path):
        os.makedirs(path)
