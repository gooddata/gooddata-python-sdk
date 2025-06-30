# (C) 2021 GoodData Corporation
from importlib import metadata

try:
    __version__ = metadata.version("gooddata-sdk")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
