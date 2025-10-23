#  (C) 2024 GoodData Corporation


class ServerStartupInterrupted(Exception):
    """
    This exception is thrown when server startup was interrupted due to unrecoverable condition. Different init and
    preparation logic may raise this to stop the server startup. The message included in the exception will be
    printed to stderr and server stops with exit code 1.
    """


class FlightMethodsModuleError(ServerStartupInterrupted):
    """
    This exception is thrown whenever there is an error related the flight methods module: loading the module, finding
    the factory, validating the factory, etc.
    """
