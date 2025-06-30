#  (C) 2024 GoodData Corporation
from typing import Any, Optional

import pyarrow.flight
import structlog

from gooddata_flight_server.server.auth.token_verifier import (
    TokenVerificationStrategy,
)


class TokenAuthMiddleware(pyarrow.flight.ServerMiddleware):
    MiddlewareName = "auth_token"

    def __init__(self, token: str, token_data: Any) -> None:
        super().__init__()

        self._token = token
        self._token_data = token_data

    @property
    def token_data(self) -> Any:
        return self._token_data


_DEFAULT_AUTH_TOKEN_HEADER = "Authorization"
_LOGGER = structlog.get_logger("gooddata_flight_server.auth")
_BEARER_END_IDX = 7


class TokenAuthMiddlewareFactory(pyarrow.flight.ServerMiddlewareFactory):
    def __init__(
        self,
        token_header_name: Optional[str],
        strategy: TokenVerificationStrategy,
    ):
        super().__init__()

        self._token_header_name = token_header_name
        self._strategy = strategy

    def _extract_token(self, headers: dict[str, list[str]]) -> str:
        def _auth_header_value(lookup: str) -> str:
            _lookup = lookup.lower()
            values = [value for header, values in headers.items() if header.lower() == _lookup for value in values]

            if len(values) > 1:
                raise pyarrow.flight.FlightUnauthenticatedError(
                    f"Authentication failed because the authentication header '{lookup}' is specified multiple times."
                )

            if not len(values):
                raise pyarrow.flight.FlightUnauthenticatedError(
                    "Authentication failed because the authentication header bearing the token was not included "
                    "on the call."
                )

            return values[0]

        if self._token_header_name is None:
            token = _auth_header_value(_DEFAULT_AUTH_TOKEN_HEADER)
            if not token.startswith("Bearer "):
                raise pyarrow.flight.FlightUnauthenticatedError(
                    "Authentication failed because the 'Authorization' header does not start with 'Bearer '"
                )

            return token[_BEARER_END_IDX:].strip()

        token = _auth_header_value(self._token_header_name)
        return token.strip()

    def start_call(self, info: pyarrow.flight.CallInfo, headers: dict[str, list[str]]) -> Optional[TokenAuthMiddleware]:
        try:
            token = self._extract_token(headers)
            result = self._strategy.verify(call_info=info, token=token)

            return TokenAuthMiddleware(token=token, token_data=result)
        except pyarrow.flight.FlightUnauthenticatedError as e:
            _LOGGER.info("authentication_failed", reason=str(e))
            raise
        except pyarrow.flight.FlightUnauthorizedError as e:
            _LOGGER.info("authorization_failed", reason=str(e))
            raise
