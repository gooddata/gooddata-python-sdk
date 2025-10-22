#  (C) 2024 GoodData Corporation

import pytest
from gooddata_flight_server.exceptions import FlightMethodsModuleError
from gooddata_flight_server.server.base import FlightServerMethods
from gooddata_flight_server.utils.methods_discovery import get_methods_factory


def test_get_methods_from_module():
    """
    Test the methods discovery function on a simple mock module.
    """
    factory = get_methods_factory(".valid_methods_module", root="tests.utils")
    assert factory is not None
    # skip mocking the whole server context, it is not the point of this test
    methods = factory(None)  # type: ignore
    assert isinstance(methods, FlightServerMethods)


def test_get_methods_from_invalid_module_multiple():
    """
    Test the methods discovery function on a mock module that provides more than one methods factory.
    """
    with pytest.raises(FlightMethodsModuleError):
        get_methods_factory(".multiple_methods_module", root="tests.utils")


def test_get_methods_from_invalid_module_none():
    """
    Test the methods discovery function on a mock module that provides no methods factories.
    """
    with pytest.raises(FlightMethodsModuleError):
        get_methods_factory(".no_methods_module", root="tests.utils")


def test_get_methods_from_invalid_module_invalid_signature():
    """
    Test the methods discovery function on a mock module that provides an invalid methods factory.
    """
    with pytest.raises(FlightMethodsModuleError):
        get_methods_factory(".invalid_methods_module", root="tests.utils")


def test_get_methods_from_invalid_module_non_existent():
    """
    Test the methods discovery function on module that does not exist.
    """
    with pytest.raises(FlightMethodsModuleError):
        get_methods_factory(".non_existent_module", root="tests.utils")
