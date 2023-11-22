# (C) 2021 GoodData Corporation
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore # mypy issue #1153

try:
    __version__ = metadata.version("gooddata-sdk")
except metadata.PackageNotFoundError:
    __version__ = "unknown-version"
