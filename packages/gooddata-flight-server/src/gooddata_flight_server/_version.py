# (C) 2024 GoodData Corporation
from importlib import metadata

try:
    __version__ = metadata.version("gooddata-flight-server")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
