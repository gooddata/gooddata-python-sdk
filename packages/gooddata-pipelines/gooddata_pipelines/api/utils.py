# (C) 2025 GoodData Corporation

"""Utility functions for GoodData Cloud API interactions."""

from typing import Any, Callable

from gooddata_api_client import ApiException  # type: ignore

from gooddata_pipelines.api.exceptions import GoodDataApiException


def raise_with_context(**context_kwargs: str) -> Callable:
    """
    Decorator to catch exceptions raised by SDK methods and raise a GoodDataApiException
    with additional context information.

    Args:
        context_kwargs (dict): Additional context information to include in the
            GoodDataApiException.
    """

    def decorator(fn: Callable) -> Callable:
        def wrapper(*method_args: Any, **method_kwargs: Any) -> Callable:
            try:
                return fn(*method_args, **method_kwargs)
            except Exception as e:
                # Process known exceptions
                if isinstance(e, ApiException):
                    context_kwargs["http_status"] = f"{e.status} {e.reason}"
                    exception_content = e.body
                else:
                    exception_content = str(e)

                # Format the exception message: "{exception_type}: {exception_content}"
                message = f"{type(e).__name__}: {exception_content}"

                raise GoodDataApiException(
                    message, **context_kwargs, **method_kwargs
                )

        return wrapper

    return decorator
