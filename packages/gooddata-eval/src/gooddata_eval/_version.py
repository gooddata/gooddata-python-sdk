# (C) 2026 GoodData Corporation
from importlib import metadata

try:
    __version__ = metadata.version("gooddata-eval")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
