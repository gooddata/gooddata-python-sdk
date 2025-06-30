# (C) 2023 GoodData Corporation
from importlib import metadata

try:
    __version__ = metadata.version("gooddata-dbt")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
