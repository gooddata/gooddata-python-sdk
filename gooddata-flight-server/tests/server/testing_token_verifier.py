#  (C) 2024 GoodData Corporation
from typing import Any

import pyarrow.flight
from gooddata_flight_server.server.auth.token_verifier import TokenVerificationStrategy


class TestingTokenVerifier(TokenVerificationStrategy):
    def verify(self, call_info: pyarrow.flight.CallInfo, token: str) -> Any:
        if not token.startswith("test_token"):
            raise pyarrow.flight.FlightUnauthenticatedError()
