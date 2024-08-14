#  (C) 2024 GoodData Corporation
from typing import Any

import pyarrow.flight
from dynaconf import ValidationError

from gooddata_flight_server.server.auth.token_verifier import TokenVerificationStrategy
from gooddata_flight_server.server.base import ServerContext

_TOKEN_ENUMERATION_SECTION = "enumerated_tokens"
_TOKEN_SETTING = "tokens"


class EnumeratedTokenVerification(TokenVerificationStrategy):
    """
    A simple token verification strategy that successfully verifies
    a token if it matches one of the tokens specified in the settings.
    """

    def __init__(self, allowed_tokens: set[str]) -> None:
        self._tokens = allowed_tokens

    def verify(self, call_info: pyarrow.flight.CallInfo, token: str) -> Any:
        if token not in self._tokens:
            raise pyarrow.flight.FlightUnauthenticatedError("Authentication token is not valid.")

        return None

    @classmethod
    def create(cls, ctx: ServerContext) -> "TokenVerificationStrategy":
        tokens = list(ctx.settings.get(f"{_TOKEN_ENUMERATION_SECTION}.{_TOKEN_SETTING}") or [])
        if not len(tokens):
            raise ValidationError(
                f"The 'EnumeratedTokenVerification' requires that you configure "
                f"which tokens are allowed to use. You have to include section "
                f"[{EnumeratedTokenVerification}] with a '{_TOKEN_SETTING}' setting that contains "
                f"list of tokens. Alternatively, you can specify environment variable "
                f"GOODDATA_FLIGHT_ENUMERATED_TOKENS__TOKENS."
            )

        return EnumeratedTokenVerification(set(tokens))
