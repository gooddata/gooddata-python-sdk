#  (C) 2024 GoodData Corporation
import abc
from dataclasses import dataclass

import pyarrow.flight
from dynaconf import Dynaconf

from gooddata_flight_server.config.config import ServerConfig
from gooddata_flight_server.server.flight_rpc.server_methods import FlightServerMethods


@dataclass(slots=True, frozen=True)
class ServerContext:
    settings: Dynaconf
    config: ServerConfig
    location: pyarrow.flight.Location


class FlightServerMethodsFactory(abc.ABC):
    @abc.abstractmethod
    def create_methods(self, context: ServerContext) -> FlightServerMethods:
        raise NotImplementedError
