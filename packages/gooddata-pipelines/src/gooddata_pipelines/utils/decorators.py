# (C) 2025 GoodData Corporation

from typing import Any, Callable

from gooddata_pipelines.logger.logger import LogObserver

logger: LogObserver = LogObserver()


def log_and_reraise_exception(message: str) -> Callable:
    """
    Decorator to log an exception and re-raise it.

    Args:
        message (str): The message to log.
    """

    def decorator(fn: Callable) -> Callable:
        def wrapper(*method_args: Any, **method_kwargs: Any) -> Callable:
            try:
                return fn(*method_args, **method_kwargs)
            except Exception:
                logger.error(
                    f"{message}, {fn.__name__}, Args: {method_args}, Kwargs: {method_kwargs}"
                )
                raise

        return wrapper

    return decorator
