#  (C) 2024 GoodData Corporation
import enum
from dataclasses import dataclass
from typing import Optional


class OtelExporterType(enum.Enum):
    """
    Supported OpenTelemetry exporter types.
    """

    Zipkin = "zipkin"
    OtlpHttp = "otlp-http"
    OtlpGrpc = "otlp-grpc"
    Console = "console"


@dataclass(frozen=True, slots=True)
class OtelConfig:
    service_namespace: str
    service_name: str
    service_instance_id: str
    exporter_type: Optional[OtelExporterType]
