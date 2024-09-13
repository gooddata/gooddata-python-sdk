#  (C) 2024 GoodData Corporation
import pytest
from gooddata_flight_server import FlightServerMethods
from gooddata_flight_server.utils.methods_discovery import get_method_factory_from_module


def test_get_method_factory_from_module():
    """
    Test the methods discovery function on a simple mock module.
    """
    provider = get_method_factory_from_module(".mock_methods_module", root="tests.utils")
    assert provider is not None

    # do not bother with creating a server context
    methods = provider(None)  # type: ignore
    assert isinstance(methods, FlightServerMethods)


def test_get_method_factory_from_module_invalid():
    """
    Test the methods discovery function on a mock module that provides more than one methods provider.
    """
    with pytest.raises(ValueError):
        get_method_factory_from_module(".invalid_methods_module", root="tests.utils")
