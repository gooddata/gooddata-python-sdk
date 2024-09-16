#  (C) 2024 GoodData Corporation

import pytest
from gooddata_flight_server.server.base import FlightServerMethods
from gooddata_flight_server.utils.methods_discovery import get_methods_factory


def test_get_methods_from_module():
    """
    Test the methods discovery function on a simple mock module.
    """
    factory = get_methods_factory(".mock_methods_module", root="tests.utils")
    assert factory is not None
    # skip mocking the whole server context, it is not the point of this test
    methods = factory(None)  # type: ignore
    assert isinstance(methods, FlightServerMethods)


def test_get_methods_from_module_invalid():
    """
    Test the methods discovery function on a mock module that provides more than one methods provider.
    """
    with pytest.raises(ValueError):
        get_methods_factory(".invalid_methods_module", root="tests.utils")
