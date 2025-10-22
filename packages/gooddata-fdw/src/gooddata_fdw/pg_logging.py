# (C) 2021 GoodData Corporation
from logging import CRITICAL, DEBUG, ERROR, INFO, WARNING

from gooddata_fdw.environment import log_to_postgres


def _log_debug(msg: str) -> None:
    log_to_postgres(f"gooddata_fdw: {msg}", level=DEBUG)


def _log_info(msg: str) -> None:
    log_to_postgres(f"gooddata_fdw: {msg}", level=INFO)


def _log_warn(msg: str) -> None:
    log_to_postgres(f"gooddata_fdw: {msg}", level=WARNING)


def _log_error(msg: str) -> None:
    log_to_postgres(f"gooddata_fdw: {msg}", level=ERROR)


def _log_critical(msg: str) -> None:
    log_to_postgres(f"gooddata_fdw: {msg}", level=CRITICAL)
