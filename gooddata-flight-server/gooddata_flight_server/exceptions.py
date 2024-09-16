#  (C) 2024 GoodData Corporation
from typing import Any


class ServerInitializationError(Exception):
    """
    Base class for exceptions related to server initialization.
    """


class FlightMethodsModuleError(ServerInitializationError):
    """
    Base class for exceptions related to flight methods modules.
    """


class FlightMethodsModuleNotFoundError(FlightMethodsModuleError):
    """
    Raised when the flight methods module is not found.
    """

    def __init__(self, module_name: str) -> None:
        super().__init__(f"Flight methods module {module_name} not found.")


class NoFlightMethodsFactoryError(FlightMethodsModuleError):
    """
    Raised when no flight methods factory is found in a module.
    """

    def __init__(self, module_name: str) -> None:
        super().__init__(
            f"No flight methods factory found in the module {module_name}. "
            "Make sure the module exports exactly one function decorated with the `@flight_server_methods` decorator "
            "that conforms to the FlightMethodsFactory protocol."
        )


class MultipleFlightMethodsFactoriesError(FlightMethodsModuleError):
    """
    Raised when multiple flight methods factories are found in a module.
    """

    def __init__(self, module_name: str, factory_count: int) -> None:
        super().__init__(
            f"Multiple flight methods factories ({factory_count}) found in the module {module_name}"
            "Make sure the module exports exactly one function decorated with the `@flight_server_methods` decorator "
            "that conforms to the FlightMethodsFactory protocol."
        )


class InvalidFlightMethodsFactoryError(FlightMethodsModuleError):
    """
    Raised when the flight methods factory is invalid.
    """

    def __init__(self, module_name: str) -> None:
        super().__init__(
            f"Invalid flight methods factory in the module {module_name}. "
            "Make sure the function conforms to the FlightMethodsFactory protocol: "
            "that it takes the correct number of arguments and returns an instance of FlightServerMethods."
        )


class InvalidFlightMethodsFactoryResultError(FlightMethodsModuleError):
    """
    Raised when the flight methods factory returns an invalid result.
    """

    def __init__(self, actual_result: Any) -> None:
        super().__init__(
            f"The provided FlightMethodsFactory has a valid signature but returned an invalid result of type "
            f"{type(actual_result)}. Make sure the factory function returns an instance of FlightServerMethods."
        )
