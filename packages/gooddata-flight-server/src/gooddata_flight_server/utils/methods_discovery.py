#  (C) 2024 GoodData Corporation
import importlib
from functools import wraps
from inspect import signature
from typing import Optional

from gooddata_flight_server.exceptions import FlightMethodsModuleError
from gooddata_flight_server.server.base import (
    FlightServerMethods,
    FlightServerMethodsFactory,
    ServerContext,
)


def flight_server_methods(fun: FlightServerMethodsFactory) -> FlightServerMethodsFactory:
    """
    Decorator that marks a function as the FlightServerMethodsFactory to be used.
    Any module that should provide the methods factory should contain exactly one function decorated with this decorator.
    """

    @wraps(fun)
    def wrapped(ctx: ServerContext) -> FlightServerMethods:
        return fun(ctx)

    wrapped.__is_flight_server_methods__ = True  # type: ignore
    return wrapped


def _is_flight_server_methods(obj: object) -> bool:
    """
    Checks whether the object is a FlightServerMethods.
    """

    return getattr(obj, "__is_flight_server_methods__", False)


def _is_valid_flight_methods_factory(obj: object) -> bool:
    """
    Check whether the object is a valid FlightServerMethodsFactory.
    """

    return callable(obj) and len(signature(obj).parameters) == 1


def _only_valid_flight_methods_factory(
    module_name: str, factories: list[FlightServerMethodsFactory]
) -> FlightServerMethodsFactory:
    """
    Validate the list of factories and return the only valid one.
    """
    if len(factories) == 0:
        raise FlightMethodsModuleError(
            f"No flight methods factory found in the module {module_name}. "
            "Make sure the module exports exactly one function decorated with the `@flight_server_methods` decorator "
            "that conforms to the FlightMethodsFactory protocol."
        )

    if len(factories) > 1:
        raise FlightMethodsModuleError(
            f"Multiple flight methods factories ({len(factories)}) found in the module {module_name}"
            "Make sure the module exports exactly one function decorated with the `@flight_server_methods` decorator "
            "that conforms to the FlightMethodsFactory protocol."
        )

    factory = factories[0]

    if not _is_valid_flight_methods_factory(factory):
        raise FlightMethodsModuleError(
            f"Invalid flight methods factory in the module {module_name}. "
            "Make sure the function conforms to the FlightMethodsFactory protocol: "
            "that it takes the correct number of arguments and returns an instance of FlightServerMethods."
        )

    return factory


def get_methods_factory(module_name: str, root: Optional[str] = None) -> FlightServerMethodsFactory:
    """
    Get the method factory from the given module.
    The module should contain exactly one method decorated with @flight_server_methods.

    :param module_name: name of the module containing the methods abstract factory.
    :param root: root package of the module: this is used to resolve relative module names (mainly useful in tests).
    :return: a FlightServerMethodsFactory
    """

    try:
        module = importlib.import_module(module_name, package=root)
    except ModuleNotFoundError as e:
        raise FlightMethodsModuleError(f"Flight methods module {module_name} not found.") from e

    factories: list[FlightServerMethodsFactory] = [
        member.__wrapped__  # unwrap the actual instance from the marker decorator to keep the type
        for member in module.__dict__.values()
        if _is_flight_server_methods(member)
    ]

    return _only_valid_flight_methods_factory(module_name, factories)
