#  (C) 2024 GoodData Corporation
import os
from pathlib import Path

from gooddata_flight_server.config.config import (
    AuthenticationMethod,
    OtelExporterType,
    read_config,
)

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
    assert server_config.otel_config.extract_context_from_headers is True


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
    assert server_config.otel_config.extract_context_from_headers is False

    assert server_config.authentication_method == AuthenticationMethod.NoAuth
    assert server_config.token_header_name is None
    assert server_config.token_verification is None


def test_read_tls():
    keyfile = os.path.join(_CURRENT_DIR, "private_key.pem")
    os.environ["GOODDATA_FLIGHT_SERVER__TLS_PRIVATE_KEY"] = f"@{keyfile}"

    _, server_config = read_config((_config_file("tls-config.toml"),))

    assert server_config.use_tls is True
    assert server_config.use_mutual_tls is True
    assert server_config.tls_cert_and_key is not None
    assert server_config.tls_cert_and_key[0] == b"inlined cert"
    assert server_config.tls_cert_and_key[1] == b"The matrix has you :D\n"
    assert server_config.tls_root_cert is not None
    assert server_config.tls_root_cert == b"inlined ca cert"


def test_read_auth():
    _, server_config = read_config((_config_file("auth-config.toml"),))

    assert server_config.authentication_method == AuthenticationMethod.Token
    assert server_config.token_header_name == "x-my-header"
    assert server_config.token_verification == "EnumeratedTokenVerification"
