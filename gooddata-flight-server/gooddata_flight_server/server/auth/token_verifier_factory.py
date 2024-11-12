#  (C) 2024 GoodData Corporation
import importlib

import structlog

from gooddata_flight_server.exceptions import ServerStartupInterrupted
from gooddata_flight_server.server.auth.token_verifier import TokenVerificationStrategy
from gooddata_flight_server.server.auth.token_verifier_impl import EnumeratedTokenVerification
from gooddata_flight_server.server.base import ServerContext

_LOGGER = structlog.get_logger("gooddata_flight_server.auth")


def _import_verification_strategy(module_name: str) -> type[TokenVerificationStrategy]:
    _LOGGER.info("load_token_verification", module_name=module_name)
    module = importlib.import_module(module_name)

    for member in module.__dict__.values():
        if not isinstance(member, type) or not issubclass(member, TokenVerificationStrategy):
            # filter out module members which are not classes that implement the
            # TokenVerificationStrategy interface
            continue

        if member == TokenVerificationStrategy:
            # the TokenVerificationStrategy class is likely imported in the module -
            # don't want that to interfere
            continue

        return member

    raise ServerStartupInterrupted(
        f"The module '{module_name}' specified in 'token_verification' setting does not "
        f"include an implementation of {TokenVerificationStrategy.__name__}."
    )


def _find_token_verification_class(ctx: ServerContext) -> type[TokenVerificationStrategy]:
    # config reader must ensure that there is always some value here
    assert ctx.config.token_verification is not None

    if ctx.config.token_verification == "EnumeratedTokenVerification":
        return EnumeratedTokenVerification

    return _import_verification_strategy(ctx.config.token_verification)


def create_token_verification_strategy(ctx: ServerContext) -> TokenVerificationStrategy:
    try:
        cls = _find_token_verification_class(ctx)

        _LOGGER.info("auth_token_strategy_init", cls=cls.__name__)
        return cls.create(ctx)
    except Exception:
        _LOGGER.critical("auth_token_init_failed", exc_info=True)
        raise
