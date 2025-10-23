#  (C) 2024 GoodData Corporation
import os
import platform
import socket
import sys
from typing import Optional

from opentelemetry import trace
from opentelemetry.sdk.resources import (
    OS_DESCRIPTION,
    OS_TYPE,
    PROCESS_PARENT_PID,
    PROCESS_PID,
    PROCESS_RUNTIME_DESCRIPTION,
    PROCESS_RUNTIME_NAME,
    PROCESS_RUNTIME_VERSION,
    SERVICE_INSTANCE_ID,
    SERVICE_NAME,
    SERVICE_NAMESPACE,
    SERVICE_VERSION,
    Resource,
)
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)

from gooddata_flight_server._version import __version__
from gooddata_flight_server.config.config import OtelConfig, OtelExporterType

SERVER_TRACER: trace.Tracer = trace.ProxyTracer("gooddata_flight_server")
"""
Tracer to use for all spans created within the server - all code in this package should
use this one single tracer.
"""


def _create_console_span_exporter() -> SpanExporter:
    return ConsoleSpanExporter()


def _create_zipkin_span_exporter() -> SpanExporter:
    from opentelemetry.exporter.zipkin.json import (
        ZipkinExporter,  # type: ignore
    )

    return ZipkinExporter()


def _create_otlp_grpc_exporter() -> SpanExporter:
    from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import (
        OTLPSpanExporter,  # type: ignore
    )

    return OTLPSpanExporter()


def _create_otlp_http_exporter() -> SpanExporter:
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import (
        OTLPSpanExporter,  # type: ignore
    )

    return OTLPSpanExporter()


def _create_exporter(config: OtelConfig) -> SpanExporter:
    if config.exporter_type == OtelExporterType.Console:
        return _create_console_span_exporter()
    elif config.exporter_type == OtelExporterType.Zipkin:
        return _create_zipkin_span_exporter()
    elif config.exporter_type == OtelExporterType.OtlpGrpc:
        return _create_otlp_grpc_exporter()
    elif config.exporter_type == OtelExporterType.OtlpHttp:
        return _create_otlp_http_exporter()

    raise AssertionError(f"Unsupported exporter type '{config.exporter_type}'.")


def _default_service_instance_id() -> str:
    return socket.gethostbyaddr("127.0.0.1")[0] if platform.system() == "Darwin" else socket.getfqdn()


def _create_resource(config: OtelConfig) -> Resource:
    # all PROCESS_RUNTIME_* attribute values including the code below picked as-is
    # from recommendations written in:
    #
    # https://opentelemetry.io/docs/specs/semconv/resource/process/#python-runtimes
    vinfo = sys.implementation.version
    process_runtime_version = ".".join(
        map(
            str,
            vinfo[:3] if vinfo.releaselevel == "final" and not vinfo.serial else vinfo,
        )
    )

    service_instance_id = config.service_instance_id or _default_service_instance_id()

    return Resource.create(
        attributes={
            SERVICE_NAME: config.service_name,
            SERVICE_VERSION: __version__,
            SERVICE_INSTANCE_ID: service_instance_id,
            SERVICE_NAMESPACE: config.service_namespace or "",
            OS_TYPE: platform.system().lower(),
            OS_DESCRIPTION: platform.platform(terse=True),
            PROCESS_PID: os.getpid(),
            PROCESS_PARENT_PID: os.getppid(),
            PROCESS_RUNTIME_NAME: sys.implementation.name,
            PROCESS_RUNTIME_VERSION: process_runtime_version,
            PROCESS_RUNTIME_DESCRIPTION: sys.version,
            "os.version": platform.release(),
        }
    )


def initialize_otel_tracing(config: Optional[OtelConfig]) -> None:
    """
    Initializes OpenTelemetry tracing according to the provided `config`:

    - If the config is specified, the method creates the desired exporter and
      initializes the tracer provider to pipe traces to it

    - If the config is None, the method will initialize tracer provider to
      NoOp implementation.

    :param config: server's open telemetry configuration
    :return: None
    """
    if config is None or config.exporter_type is None:
        trace.set_tracer_provider(trace.NoOpTracerProvider())
        return

    resource = _create_resource(config)
    span_exporter = _create_exporter(config)

    span_processor = BatchSpanProcessor(span_exporter=span_exporter)

    tracer_provider = TracerProvider(resource=resource)
    tracer_provider.add_span_processor(span_processor=span_processor)
    trace.set_tracer_provider(tracer_provider=tracer_provider)
