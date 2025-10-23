# (C) 2025 GoodData Corporation

"""Exception class for Panther operations.

This module defines the internally used `PantherException` class, which is used
to handle exceptions that occur during operations related to the Panther SDK or
GoodData Cloud API.
"""


class GoodDataApiException(Exception):
    """Exception raised during Panther operations.

    This exception is used to indicate errors that occur during operations
    related to interactions with the GoodData Python SDK or GoodData Cloud API.
    It can include additional context provided through keyword arguments.
    """

    def __init__(self, message: str, **kwargs: str) -> None:
        """Raise a PantherException with a message and optional context.

        Args:
            message (str): The error message describing the exception.
            **kwargs: Additional context for the exception, such as HTTP status,
                    API endpoint, and HTTP method or any other relevant information.
        """

        super().__init__(message)
        self.error_message: str = message

        # Set default values for attributes.
        # TODO: Consider if the defaults for these are still needed
        # - the values were necessary for log schema implementations, which
        #   are not used anymore.
        self.http_status: str = "500 Internal Server Error"
        self.api_endpoint: str = "NA"
        self.http_method: str = "NA"

        # Set attributes from kwargs.
        for key, value in kwargs.items():
            setattr(self, key, value)
