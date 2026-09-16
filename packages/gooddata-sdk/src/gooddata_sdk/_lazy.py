# (C) 2025 GoodData Corporation
"""Helper for exposing subpackage contents as attributes without importing them eagerly."""

from collections.abc import Callable
from importlib import import_module
from types import ModuleType


def submodule_getattr(package: str) -> Callable[[str], ModuleType]:
    """Build a PEP 562 ``__getattr__`` that imports ``<package>.<name>`` on first access.

    The SDK no longer imports its whole module tree at startup, so subpackages are no longer
    populated as a side effect of ``import gooddata_sdk``. Without this, attribute access such
    as ``gooddata_sdk.catalog.workspace`` would raise ``AttributeError`` unless that submodule
    happened to have been imported already by something else.

    Args:
        package (str): Dotted name of the package the ``__getattr__`` belongs to (``__name__``).

    Returns:
        Callable[[str], ModuleType]: Function to assign to the package's ``__getattr__``.
    """

    def __getattr__(name: str) -> ModuleType:
        try:
            return import_module(f"{package}.{name}")
        except ModuleNotFoundError as e:
            # Only translate "this submodule does not exist"; a missing dependency *inside* an
            # existing submodule must keep its original error rather than look like a typo.
            if e.name != f"{package}.{name}":
                raise
            raise AttributeError(f"module {package!r} has no attribute {name!r}") from None

    return __getattr__
