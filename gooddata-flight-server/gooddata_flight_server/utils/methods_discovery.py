#  (C) 2024 GoodData Corporation
import importlib
from typing import Optional

from gooddata_flight_server.server.base import FlightServerMethodsAbstractFactory, FlightServerMethodsFactory


def get_method_factory_from_module(module_name: str, root: Optional[str] = None) -> FlightServerMethodsFactory:
    """
    Get the method abstract factory from the given module.

    :param module_name: name of the module containing the methods abstract factory.
    :param root: root package of the module: this is used to resolve relative module names (mainly useful in tests).
    :return: a FlightServerMethodsFactory instance.
    """

    module = importlib.import_module(module_name, package=root)

    factories: list[FlightServerMethodsFactory] = []

    for member in module.__dict__.values():
        if not isinstance(member, type) or not issubclass(member, FlightServerMethodsAbstractFactory):
            # filter out module members which are not classes that implement the
            # FlightServerMethodsAbstractFactory interface
            continue

        if member is FlightServerMethodsAbstractFactory:
            # the FlightServerMethodsAbstractFactory class itself is likely imported in the module -
            # don't want to use that
            continue

        abstract_factory = member()
        factories.append(abstract_factory.get_factory())

    if len(factories) != 1:
        raise ValueError(
            f"Expected exactly one FlightServerMethodsAbstractFactory in {module_name}, got {len(factories)}"
        )

    return factories[0]
