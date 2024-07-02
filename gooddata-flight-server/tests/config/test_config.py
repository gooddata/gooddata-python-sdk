#  (C) 2024 GoodData Corporation
import os
from pathlib import Path

from gooddata_flight_server.config.config import OtelExporterType, read_config

_CURRENT_DIR = Path(__file__).parent


def _config_file(filename: str) -> str:
    return os.path.join(_CURRENT_DIR, filename)


def test_read_valid():
    _, server_config = read_config((_config_file("sample-config.toml"),))

    assert server_config.listen_host == "127.0.0.1"
    assert server_config.listen_port == 17001
    assert server_config.advertise_port == 17001
    assert server_config.task_threads == 32
    assert server_config.metrics_host == "0.0.0.0"
    assert server_config.metrics_port == 17101
    assert server_config.health_check_host == "0.0.0.0"
    assert server_config.health_check_port == 8877
    assert server_config.log_event_key_name == "event"
    assert server_config.otel_config.exporter_type == OtelExporterType.OtlpGrpc
    assert server_config.otel_config.service_name == "your-service-name"
    assert server_config.otel_config.service_namespace == "your-namespace"
    assert server_config.otel_config.service_instance_id == "your-service-instance-id"


def test_read_empty():
    _, server_config = read_config((_config_file("empty-config.toml"),))

    assert server_config.listen_host == "127.0.0.1"
    assert server_config.listen_port == 17001
    assert server_config.advertise_port == 17001
    assert server_config.task_threads == 32
    assert server_config.metrics_host is None
    assert server_config.metrics_port == 17101
    assert server_config.health_check_host is None
    assert server_config.health_check_port == 8877
    assert server_config.log_event_key_name == "event"
    assert server_config.otel_config.exporter_type is None
    assert server_config.otel_config.service_name is None
    assert server_config.otel_config.service_namespace is None
    assert server_config.otel_config.service_instance_id is None
