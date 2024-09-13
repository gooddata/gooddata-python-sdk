#  (C) 2024 GoodData Corporation
from gooddata_flight_server import FlightServerMethods
from gooddata_flight_server.server.base import (
    FlightServerMethodsAbstractFactory,
    FlightServerMethodsFactory,
    ServerContext,
)


class MockMethods(FlightServerMethods):
    def __init__(self, ctx: ServerContext) -> None:
        self._ctx = ctx


class MockMethodsAbstractFactory(FlightServerMethodsAbstractFactory):
    def get_factory(self) -> FlightServerMethodsFactory:
        def factory(ctx: ServerContext) -> FlightServerMethods:
            return MockMethods(ctx)

        return factory


class AnotherMockMethodsAbstractFactory(FlightServerMethodsAbstractFactory):
    def get_factory(self) -> FlightServerMethodsFactory:
        def factory(ctx: ServerContext) -> FlightServerMethods:
            return MockMethods(ctx)

        return factory
