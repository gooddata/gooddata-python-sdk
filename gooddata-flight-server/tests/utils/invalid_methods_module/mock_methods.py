#  (C) 2024 GoodData Corporation
from gooddata_flight_server.server.base import FlightServerMethods, ServerContext
from gooddata_flight_server.utils.methods_discovery import flight_server_methods


class MockMethods(FlightServerMethods):
    def __init__(self, ctx: ServerContext) -> None:
        self._ctx = ctx


@flight_server_methods
def mockMethodsFactory(ctx: ServerContext) -> FlightServerMethods:
    return MockMethods(ctx)


@flight_server_methods
def anotherMockMethodsFactory(ctx: ServerContext) -> FlightServerMethods:
    return MockMethods(ctx)
