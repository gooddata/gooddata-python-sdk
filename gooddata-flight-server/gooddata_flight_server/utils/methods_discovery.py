#  (C) 2024 GoodData Corporation
import importlib
import importlib.util
from pathlib import Path
from types import ModuleType
from typing import Optional

from gooddata_flight_server.server.base import FlightServerMethodsAbstractFactory, FlightServerMethodsFactory


def _get_method_factory_from_module(module: ModuleType, debug_name: str) -> FlightServerMethodsFactory:
    factories = []
    for obj in module.__dict__.values():
        if (
            isinstance(obj, type)
            and issubclass(obj, FlightServerMethodsAbstractFactory)
            and obj is not FlightServerMethodsAbstractFactory  # Exclude the base class itself
        ):
            abstract_factory = obj()
            factories.append(abstract_factory.get_factory())

    if not factories or len(factories) != 1:
        raise ValueError(
            f"Expected exactly one FlightServerMethodsAbstractFactory in {debug_name}, got {len(factories)}"
        )

    return factories[0]


def get_method_factory_from_file(module_path: str) -> FlightServerMethodsFactory:
    """
    Get the method abstract factory from the given path.

    :param module_path: path to the module containing the methods abstract factory.
    :return: a FlightServerMethodsFactory instance.
    """

    module_name = Path(module_path).stem
    # Dynamically load the provider module
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    if not spec or not spec.loader:
        raise ImportError(f"Cannot load module from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    return _get_method_factory_from_module(module, module_path)


def get_method_factory_from_module(module_name: str, root: Optional[str] = None) -> FlightServerMethodsFactory:
    """
    Get the method abstract factory from the given module.

    :param module_name: name of the module containing the methods abstract factory.
    :param root: root package of the module: this is used to resolve relative module names (mainly useful in tests).
    :return: a FlightServerMethodsFactory instance.
    """

    module = importlib.import_module(module_name, package=root)

    return _get_method_factory_from_module(module, module_name)
