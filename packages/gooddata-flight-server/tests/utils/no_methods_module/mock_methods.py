#  (C) 2024 GoodData Corporation
from gooddata_flight_server.server.base import FlightServerMethods, ServerContext


class MockMethods(FlightServerMethods):
    def __init__(self, ctx: ServerContext) -> None:
        self._ctx = ctx


# the function is not decorated with the `flight_server_methods` decorator
def mockMethodsFactory(ctx: ServerContext) -> MockMethods:
    return MockMethods(ctx)
