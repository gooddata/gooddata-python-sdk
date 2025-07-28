# (C) 2025 GoodData Corporation
from importlib import metadata

try:
    __version__ = metadata.version("gooddata-pipelines")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
