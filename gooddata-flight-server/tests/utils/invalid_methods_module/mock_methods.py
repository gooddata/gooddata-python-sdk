#  (C) 2024 GoodData Corporation
from gooddata_flight_server.server.base import FlightServerMethods, ServerContext
from gooddata_flight_server.utils.methods_discovery import flight_server_methods


class MockMethods(FlightServerMethods):
    def __init__(self, ctx: ServerContext) -> None:
        self._ctx = ctx


# the function is decorated with the `flight_server_methods` decorator
# but has a wrong signature
@flight_server_methods
def mockMethodsFactory(ctx: ServerContext, extra_parameter: str) -> MockMethods:
    print(extra_parameter)
    return MockMethods(ctx)
