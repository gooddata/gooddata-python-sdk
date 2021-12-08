# (C) 2021 GoodData Corporation
try:
    from importlib import metadata
except ImportError:
    import importlib_metadata as metadata  # type: ignore # mypy issue #1153

__version__: str = metadata.version("gooddata-pandas")
