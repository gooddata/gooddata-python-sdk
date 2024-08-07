# (C) 2024 GoodData Corporation
"""
This is a thin wrapper around the PyArrow FlightServerBase. It exists to provide a typed interface.

There are two main pieces:

-  FlightServer - this is an extension of pyarrow.flight.FlightServerBase; the sole purpose here is to decouple
   implementation of the technical parts and the actual handling of Flight RPC Methods
-  FlightServerMethods - base class containing typed definitions of all Flight RPC Methods
"""

from typing import Dict, Generator, List, Optional, Tuple, Union

import pyarrow.flight
from typing_extensions import TypeAlias

from gooddata_flight_server.server.flight_rpc.server_methods import (
    FlightServerMethods,
)

FlightServerLocation: TypeAlias = Union[str, bytes, Optional[Tuple[str, int]], pyarrow.flight.Location]
FlightTlsCertificates: TypeAlias = List[Tuple[bytes, bytes]]
FlightMiddlewares: TypeAlias = Dict[str, pyarrow.flight.ServerMiddlewareFactory]


class FlightServer(pyarrow.flight.FlightServerBase):
    """
    Creates AND starts the Flight RPC Server. To handle the RPC methods, the server will call out to the
    `methods` object. The `methods` object can be switched from outside, thus allowing caller code to switch
    implementation of the RPC methods at its own discretion. Typical use case for this is to keep returning
    `UNAVAILABLE` until the entire server starts, then switch to the real implementation.

    Please note, that the Flight RPC Server actually starts as soon as this class is created. The `serve` and
    `serve_with_signals` are merely a synchronization mechanism to wait until the server gets stopped.

    When managing the lifecycle of the Flight RPC from outside, it is better not to use the serve() methods.
    """

    def __init__(
        self,
        methods: Optional[FlightServerMethods] = None,
        location: Optional[FlightServerLocation] = None,
        auth_handler: Optional[pyarrow.flight.ServerAuthHandler] = None,
        tls_certificates: Optional[FlightTlsCertificates] = None,
        verify_client: Optional[bool] = None,
        root_certificates: Optional[bytes] = None,
        middleware: Optional[FlightMiddlewares] = None,
    ):
        """
        Create Flight server

        :param methods: implementation of Flight RPC methods to use; when None provided, will use implementation
           that raises NotImplementedError for any method call
        :param location : str, tuple or Location optional, default None
           Location to serve on. Either a gRPC URI like `grpc://localhost:port`,
           a tuple of (host, port) pair, or a Location instance.
           If None is passed then the server will be started on localhost with a
           system provided random port.
        :param auth_handler : ServerAuthHandler optional, default None
            An authentication mechanism to use. May be None.
        :param tls_certificates : list optional, default None
            A list of (certificate, key) pairs.
        :param verify_client : boolean optional, default False
            If True, then enable mutual TLS: require the client to present
            a client certificate, and validate the certificate.
        :param root_certificates : bytes optional, default None
            If enabling mutual TLS, this specifies the PEM-encoded root
            certificate used to validate client certificates.
        :param middleware : list optional, default None
            A dictionary of :class:`ServerMiddlewareFactory` items. The
            keys are used to retrieve the middleware instance during calls
            (see :meth:`ServerCallContext.get_middleware`).
        """
        super().__init__(
            location=location,
            auth_handler=auth_handler,
            tls_certificates=tls_certificates,
            verify_client=verify_client,
            root_certificates=root_certificates,
            middleware=middleware,
        )

        self._methods = methods or FlightServerMethods()

    def switch_methods(self, methods: FlightServerMethods) -> None:
        """
        Switch methods used to handle Flight RPC requests. New requests will be handled using these methods.

        :param methods: new set of methods to use
        :return:
        """
        self._methods = methods

    def serve(self) -> None:
        """
        Serve waits until the underlying server has stopped. This blocks current thread.

        Note that the underlying Flight RPC Service starts up immediately when this class is constructed so this is
        really just a synchronization mechanism.

        :return: nothing
        """
        self.wait()

    def serve_with_signals(self) -> None:
        """
        Serve waits until the underlying server has stopped OR until INT or TERM signal.
        This blocks current thread.

        When signal is received, the server will shut down as soon as current requests are
        done and this method will return.

        Note that the underlying Flight RPC Service starts up immediately when this class is
        constructed so this is really just a synchronization mechanism.

        :return: nothing
        """
        return self.serve()

    #
    # Delegates to methods impl
    #

    def list_flights(
        self, context: pyarrow.flight.ServerCallContext, criteria: bytes
    ) -> Generator[pyarrow.flight.FlightInfo, None, None]:
        return self._methods.list_flights(context, criteria)

    def get_flight_info(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        return self._methods.get_flight_info(context, descriptor)

    def get_schema(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.SchemaResult:
        return self._methods.get_schema(context, descriptor)

    def do_put(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.FlightMetadataWriter,
    ) -> None:
        return self._methods.do_put(context, descriptor, reader, writer)

    def do_get(
        self,
        context: pyarrow.flight.ServerCallContext,
        ticket: pyarrow.flight.Ticket,
    ) -> pyarrow.flight.FlightDataStream:
        return self._methods.do_get(context, ticket)

    def do_exchange(
        self,
        context: pyarrow.flight.ServerCallContext,
        descriptor: pyarrow.flight.FlightDescriptor,
        reader: pyarrow.flight.MetadataRecordBatchReader,
        writer: pyarrow.flight.MetadataRecordBatchWriter,
    ) -> None:
        return self._methods.do_exchange(context, descriptor, reader, writer)

    def list_actions(self, context: pyarrow.flight.ServerCallContext) -> List[Tuple[str, str]]:
        return self._methods.list_actions(context)

    def do_action(
        self,
        context: pyarrow.flight.ServerCallContext,
        action: pyarrow.flight.Action,
    ) -> Generator[pyarrow.flight.Result, None, None]:
        return self._methods.do_action(context, action)
