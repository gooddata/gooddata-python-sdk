# (C) 2025 GoodData Corporation

"""Logging observer for the GoodData Pipelines SDK.

This module provides a singleton observer class `LogObserver` that allows
subscribing logger-like objects to receive log messages. The observer emits
unformatted log messages to all subscribed objects, which should implement
the `LoggerLike` protocol.
"""

from enum import Enum
from typing import Any, Protocol


class SingletonMeta(type):
    _instances: dict = {}

    def __call__(cls, *args: Any, **kwargs: Any) -> "SingletonMeta":
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Severity(Enum):
    """Severity levels for logging."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class LoggerLike(Protocol):
    """A protocol for a logger-like object.

    This protocol defines the methods that a logger-like object should implement
    to be compatible with the `LogObserver`. It includes methods for logging
    messages at different severity levels: info, warning, and error.
    """

    def info(self, *args: Any, **kwargs: Any) -> None: ...

    def warning(self, *args: Any, **kwargs: Any) -> None: ...

    def error(self, *args: Any, **kwargs: Any) -> None: ...


class LogObserver(metaclass=SingletonMeta):
    """Singleton observer class for logging messages.

    Emits unformatted log messages to all subscribed logger-like objects.
    """

    # TODO: in future we might want to add a timestamp or other metadata
    # (severity...)? Currently that is left out to subscribers to handle.

    # TODO: with error we're dumping the context as string to the message
    # that could be improved (either passing the context as a separate arg
    # or handling the process here).

    def __init__(self) -> None:
        self.subscribers: list[LoggerLike] = []

    def subscribe(self, subscriber: LoggerLike) -> None:
        """Subscribe a logger-like object to receive log messages.

        Args:
            subscriber (LoggerLike): An object that implements the LoggerLike
            protocol.
        Returns:
            None
        """
        self.subscribers.append(subscriber)

    def unsubscribe(self, subscriber: LoggerLike) -> None:
        """Unsubscribe a logger-like object from receiving log messages.

        Args:
            subscriber (LoggerLike): An object that implements the LoggerLike
            protocol.

        Returns:
            None
        """
        self.subscribers.remove(subscriber)

    def _notify(self, severity: Severity, msg: str) -> None:
        """Notify all subscribers with a log message.

        Args:
            severity (Severity): The severity level of the log message.
            msg (str): The log message to be sent to subscribers.

        Returns:
            None
        """
        for subscriber in self.subscribers:
            if severity == Severity.INFO:
                subscriber.info(msg)
            elif severity == Severity.WARNING:
                subscriber.warning(msg)
            elif severity == Severity.ERROR:
                subscriber.error(msg)

    def info(self, msg: str) -> None:
        """Log an info message."""
        self._notify(Severity.INFO, msg)

    def warning(self, msg: str) -> None:
        """Log a warning message."""
        self._notify(Severity.WARNING, msg)

    def error(self, msg: str) -> None:
        """Log an error message."""
        self._notify(Severity.ERROR, msg)
