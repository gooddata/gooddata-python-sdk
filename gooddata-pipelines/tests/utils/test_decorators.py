# (C) 2025 GoodData Corporation

from typing import Any

import pytest

from gooddata_pipelines.utils.decorators import log_and_reraise_exception


@pytest.fixture()
def mocked_logger(mocker):
    return mocker.patch("gooddata_pipelines.utils.decorators.logger")


def test_log_and_re_raise_no_exception(mocked_logger):
    """Decorator should return inner function result and not log on success."""

    @log_and_reraise_exception("no-op")
    def target(a: int, b: int, *, c: int) -> int:
        return a + b + c

    result = target(1, 2, c=3)

    assert result == 6
    mocked_logger.error.assert_not_called()


def test_log_and_re_raise_logs_and_reraises(mocked_logger):
    """Decorator should log error and re-raise the original exception."""

    @log_and_reraise_exception("boom")
    def target(*args: Any, **kwargs: Any) -> None:
        raise ValueError("explosion")

    with pytest.raises(ValueError, match="explosion"):
        target(1, 2, a=3)

    mocked_logger.error.assert_called_once_with(
        "boom, target, Args: (1, 2), Kwargs: {'a': 3}"
    )
