#  (C) 2024 GoodData Corporation

from gooddata_flight_server import FlightServerMethods
from gooddata_flight_server.utils.methods_discovery import get_method_factory_from_file, get_method_factory_from_module


def test_get_method_factory_from_file():
    """
    Test the methods discovery function on a simple mock file.
    """
    provider = get_method_factory_from_file("tests/utils/mock_methods_module/abstract_factory.py")
    assert provider is not None

    # do not bother with creating a server context
    methods = provider(None)  # type: ignore
    assert isinstance(methods, FlightServerMethods)


def test_get_method_factory_from_module():
    """
    Test the methods discovery function on a simple mock module.
    """
    provider = get_method_factory_from_module(".mock_methods_module", root="tests.utils")
    assert provider is not None

    # do not bother with creating a server context
    methods = provider(None)  # type: ignore
    assert isinstance(methods, FlightServerMethods)
