#  (C) 2024 GoodData Corporation
import abc
from typing import Any

import pyarrow.flight

from gooddata_flight_server.server.base import ServerContext


class TokenVerificationStrategy(abc.ABC):
    """
    Token verification strategy is used by server's token authentication
    middleware to perform the actual verification:

    - The middleware is responsible for extracting the token
    - The strategy is responsible for verifying that the token is valid and
      if applicable return any information carried in the token.
    - The middleware is responsible for holding onto value returned by the
      verifier and make it available to call handling code.
    """

    @abc.abstractmethod
    def verify(self, call_info: pyarrow.flight.CallInfo, token: str) -> Any:
        """
        Perform token verification.

        - If the token is not valid, this method should raise either pyarrow.flight.FlightUnauthenticated
        - If the token is valid but fails authorization for current call, this method
          should raise pyarrow.Flight.FlightUnauthorized

        Otherwise, the method should return either nothing or a custom value describing
        the contents of the token - as it sees fit.

        For example a JWT Token Verification strategy may extract claims and return them in a
        dictionary.

        :param call_info: current call info
        :param token: token to verify
        :return: either nothing or a custom value with info extracted from the token
        :raises pyarrow.flight.FlightUnauthenticated - when the token is invalid / fails validation
        :raises pyarrow.flight.FlightUnauthorized - when the token is valid but the caller holding
         the token is not authorized to make the call
        """
        raise NotImplementedError

    @classmethod
    def create(cls, ctx: ServerContext) -> "TokenVerificationStrategy":
        """
        This method is called exactly once during the server startup to obtain
        a singleton of the concrete verification strategy to be used by
        the server.

        A typical use case here is to inspect the settings included in the server
        context and obtain any essential configuration from the `settings`.

        The strategy _may_ use this opportunity to perform any long-running
        and blocking one-time initialization.

        :param ctx: server context where the verification strategy will be used
        :return: an instance of the strategy.
        """
        return cls()
