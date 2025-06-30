#  (C) 2024 GoodData Corporation
import dataclasses
import enum
import os
import platform
import socket
from dataclasses import dataclass
from typing import Any, Optional

from dynaconf import Dynaconf, ValidationError, Validator

_SERVER_SECTION_NAME = "server"


class OtelExporterType(enum.Enum):
    """
    Supported OpenTelemetry exporter types.
    """

    Zipkin = "zipkin"
    OtlpHttp = "otlp-http"
    OtlpGrpc = "otlp-grpc"
    Console = "console"


class AuthenticationMethod(enum.Enum):
    """
    Authentication method specifies how to authenticate requests.
    """

    NoAuth = "none"
    Token = "token"


@dataclass(frozen=True)
class OtelConfig:
    exporter_type: Optional[OtelExporterType]
    service_name: str
    service_namespace: Optional[str]
    service_instance_id: Optional[str]
    extract_context_from_headers: bool


@dataclass(frozen=True)
class ServerConfig:
    listen_host: str
    listen_port: int
    advertise_host: str
    advertise_port: int

    use_tls: bool
    use_mutual_tls: bool
    tls_cert_and_key: Optional[tuple[bytes, bytes]]
    tls_root_cert: Optional[bytes]

    authentication_method: AuthenticationMethod
    token_header_name: Optional[str]
    token_verification: Optional[str]

    task_threads: int
    task_close_threads: int
    task_result_ttl_sec: int

    metrics_host: Optional[str]
    metrics_port: int

    health_check_host: Optional[str]
    health_check_port: int

    malloc_trim_interval_sec: int
    log_event_key_name: str
    log_trace_keys: dict[str, str]

    otel_config: OtelConfig

    def without_tls(self) -> "ServerConfig":
        def _basic_sanity(val: bytes) -> bytes:
            return val[0:38] + b"..." + val[-38:]

        sanitized_root_cert: Optional[bytes] = None
        sanitized_cert_and_key: Optional[tuple[bytes, bytes]] = None

        if self.tls_root_cert is not None:
            sanitized_root_cert = _basic_sanity(self.tls_root_cert)

        if self.tls_cert_and_key is not None:
            sanitized_cert_and_key = (
                _basic_sanity(self.tls_cert_and_key[0]),
                _basic_sanity(self.tls_cert_and_key[1]),
            )

        return dataclasses.replace(
            self,
            tls_cert_and_key=sanitized_cert_and_key,
            tls_root_cert=sanitized_root_cert,
        )


class _Settings:
    ListenHost = "listen_host"
    ListenPort = "listen_port"
    AdvertiseHost = "advertise_host"
    AdvertisePort = "advertise_port"
    UseTls = "use_tls"
    UseMtls = "use_mtls"
    TlsCertificate = "tls_certificate"
    TlsPrivateKey = "tls_private_key"
    TlsRoot = "tls_root_certificate"
    AuthenticationMethod = "authentication_method"
    TokenHeaderName = "token_header_name"
    TokenVerification = "token_verification"
    TaskThreads = "task_threads"
    TaskCloseThreads = "task_close_threads"
    TaskResultTtlSec = "task_result_ttl_sec"
    MetricsHost = "metrics_host"
    MetricsPort = "metrics_port"
    HealthcheckHost = "health_check_host"
    HealthcheckPort = "health_check_port"
    MallocTrimIntervalSec = "malloc_trim_interval_sec"
    LogEventKeyName = "log_event_key_name"
    LogTraceKeys = "log_trace_keys"
    OtelExporterType = "otel_exporter_type"
    OtelServiceName = "otel_service_name"
    OtelServiceNamespace = "otel_service_namespace"
    OtelServiceInstanceId = "otel_service_instance_id"
    OtelExtractContext = "otel_extract_context"


_LOCALHOST = "127.0.0.1"
_DEFAULT_ADVERTISE_HOST = socket.gethostbyaddr("127.0.0.1")[0] if platform.system() == "Darwin" else socket.getfqdn()
_DEFAULT_LISTEN_PORT = 17001
_DEFAULT_TASK_THREADS = 32
_DEFAULT_TASK_CLOSE_THREADS = 2
_DEFAULT_TASK_RESULT_TTL_SEC = 60
_DEFAULT_MALLOC_TRIM_INTERVAL_SEC = 30
_DEFAULT_METRICS_PORT = 17101
_DEFAULT_HEALTHCHECK_PORT = 8877
_DEFAULT_LOG_EVENT_KEY_NAME = "event"
_DEFAULT_TOKEN_VERIFICATION = "EnumeratedTokenVerification"

_SUPPORTED_EXPORTERS = [
    "none",
    OtelExporterType.Zipkin.value,
    OtelExporterType.OtlpHttp.value,
    OtelExporterType.OtlpGrpc.value,
    OtelExporterType.Console.value,
]

_SUPPORTED_AUTH_METHOD = [
    AuthenticationMethod.NoAuth.value,
    AuthenticationMethod.Token.value,
]


def _fqsn(name: str) -> str:
    """
    Get fully-qualified server setting name. Given a name of setting, this returns
    name prefixed with server section name. E.g. `listen_url` becomes `server.listen_url`.

    :param name: setting name
    :return: fully qualified setting name
    """
    return f"{_SERVER_SECTION_NAME}.{name}"


def _validate_non_empty_string(val: Any) -> bool:
    return isinstance(val, str) and len(val) > 0


def _validate_non_negative_number(val: Any) -> bool:
    try:
        return int(val) > 0
    except ValueError:
        return False


def _validate_supported_otel_exporter(val: Any) -> bool:
    return val in _SUPPORTED_EXPORTERS


def _validate_supported_auth(val: Any) -> bool:
    return val in _SUPPORTED_AUTH_METHOD


def _validate_mapping(val: Any) -> bool:
    return isinstance(val, dict)


def _validate_boolean(val: Any) -> bool:
    return isinstance(val, bool)


_VALIDATORS = [
    Validator(
        _fqsn(_Settings.ListenHost),
        default=_LOCALHOST,
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.ListenHost} must be an IP address or hostname.",
        },
    ),
    Validator(
        _fqsn(_Settings.ListenPort),
        default=_DEFAULT_LISTEN_PORT,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.ListenPort} must be a valid port number.",
        },
    ),
    Validator(
        _fqsn(_Settings.AdvertiseHost),
        default=_DEFAULT_ADVERTISE_HOST,
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.AdvertiseHost} must be an IP address or hostname.",
        },
    ),
    Validator(
        _fqsn(_Settings.AdvertisePort),
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.AdvertisePort} must be a valid port number.",
        },
    ),
    Validator(
        _fqsn(_Settings.UseTls),
        default=False,
        condition=_validate_boolean,
        cast=bool,
        messages={
            "condition": f"{_Settings.UseTls} must be a boolean value.",
        },
    ),
    Validator(
        _fqsn(_Settings.UseMtls),
        default=False,
        condition=_validate_boolean,
        cast=bool,
        messages={
            "condition": f"{_Settings.UseMtls} must be a boolean value.",
        },
    ),
    Validator(
        _fqsn(_Settings.TlsCertificate),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.TlsCertificate} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.TlsPrivateKey),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.TlsPrivateKey} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.TlsRoot),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.TlsRoot} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.AuthenticationMethod),
        condition=_validate_supported_auth,
        default=AuthenticationMethod.NoAuth.value,
        cast=str,
        messages={
            "condition": f"{_Settings.AuthenticationMethod} must be one of {', '.join(_SUPPORTED_AUTH_METHOD)}.",
        },
    ),
    Validator(
        _fqsn(_Settings.TokenHeaderName),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.TokenHeaderName} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.TokenVerification),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.TokenVerification} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.TaskThreads),
        default=_DEFAULT_TASK_THREADS,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.TaskThreads} must be a positive number.",
        },
    ),
    Validator(
        _fqsn(_Settings.TaskCloseThreads),
        default=_DEFAULT_TASK_CLOSE_THREADS,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.TaskCloseThreads} must be a positive number.",
        },
    ),
    Validator(
        _fqsn(_Settings.TaskResultTtlSec),
        default=_DEFAULT_TASK_RESULT_TTL_SEC,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.TaskResultTtlSec} must be a positive number (number of seconds).",
        },
    ),
    Validator(
        _fqsn(_Settings.MetricsHost),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.MetricsHost} must be an IP address or hostname.",
        },
    ),
    Validator(
        _fqsn(_Settings.MetricsPort),
        default=_DEFAULT_METRICS_PORT,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.MetricsHost} must be a valid port number.",
        },
    ),
    Validator(
        _fqsn(_Settings.HealthcheckHost),
        condition=_validate_non_empty_string,
        cast=str,
        messages={
            "condition": f"{_Settings.HealthcheckHost} must be an IP address or hostname.",
        },
    ),
    Validator(
        _fqsn(_Settings.HealthcheckPort),
        default=_DEFAULT_HEALTHCHECK_PORT,
        condition=_validate_non_negative_number,
        cast=int,
        messages={
            "condition": f"{_Settings.HealthcheckPort} must be a valid port number.",
        },
    ),
    Validator(
        _fqsn(_Settings.MallocTrimIntervalSec),
        default=_DEFAULT_MALLOC_TRIM_INTERVAL_SEC,
        condition=_validate_non_negative_number,
        messages={
            "condition": f"{_Settings.MallocTrimIntervalSec} must be a positive number.",
        },
    ),
    Validator(
        _fqsn(_Settings.LogEventKeyName),
        default=_DEFAULT_LOG_EVENT_KEY_NAME,
        condition=_validate_non_empty_string,
        messages={
            "condition": f"{_Settings.LogEventKeyName} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.LogTraceKeys),
        condition=_validate_mapping,
        messages={
            "condition": f"{_Settings.LogTraceKeys} must be a mapping between 'trace_id', 'span_id' "
            f"and 'parent_span_id' -> keys that should appear in structured log messages.",
        },
    ),
    Validator(
        _fqsn(_Settings.OtelExporterType),
        cast=str,
        condition=_validate_supported_otel_exporter,
        messages={
            "condition": f"{_Settings.OtelExporterType} must be one of {', '.join(_SUPPORTED_EXPORTERS)}.",
        },
    ),
    Validator(
        _fqsn(_Settings.OtelServiceName),
        cast=str,
        condition=_validate_non_empty_string,
        messages={
            "condition": f"{_Settings.OtelServiceName} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.OtelServiceNamespace),
        cast=str,
        condition=_validate_non_empty_string,
        messages={
            "condition": f"{_Settings.OtelServiceNamespace} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.OtelServiceInstanceId),
        cast=str,
        condition=_validate_non_empty_string,
        messages={
            "condition": f"{_Settings.OtelServiceInstanceId} must be a non-empty string.",
        },
    ),
    Validator(
        _fqsn(_Settings.OtelExtractContext),
        cast=bool,
        default=False,
        condition=_validate_boolean,
        messages={
            "condition": f"{_Settings.OtelExtractContext} must be a boolean value.",
        },
    ),
]


def _read_tls_setting(settings: Dynaconf, setting: str) -> Optional[bytes]:
    value: str = settings.get(setting)
    if value is None:
        return None

    value = value.strip()
    if value.startswith("@"):
        with open(value[1:], "rb") as f:
            return f.read()

    return value.encode("ascii")


def _create_server_config(settings: Dynaconf) -> ServerConfig:
    server_settings = settings.get(_SERVER_SECTION_NAME)
    if server_settings is None:
        raise ValidationError(f"The configuration does not contain the '{_SERVER_SECTION_NAME}'.")

    exporter_type = server_settings.get(_Settings.OtelExporterType)
    if exporter_type == "none":
        exporter_type = None

    # advertise port defaults to value of listen port
    advertise_port = server_settings.get(_Settings.AdvertisePort) or server_settings.get(_Settings.ListenPort)

    use_tls = server_settings.get(_Settings.UseTls)
    tls_cert_and_key: Optional[tuple[bytes, bytes]] = None
    tls_root_cert: Optional[bytes] = None

    if use_tls:
        cert = _read_tls_setting(server_settings, _Settings.TlsCertificate)
        if cert is None:
            raise ValidationError(
                f"When you specify 'use_tls = true', then you must provide '{_Settings.TlsCertificate}'."
            )

        key = _read_tls_setting(server_settings, _Settings.TlsPrivateKey)
        if key is None:
            raise ValidationError(
                f"When you specify 'use_tls = true', then you must provide '{_Settings.TlsPrivateKey}'."
            )

        tls_cert_and_key = (cert, key)

    use_mtls = server_settings.get(_Settings.UseMtls)
    if use_mtls:
        tls_root_cert = _read_tls_setting(server_settings, _Settings.TlsRoot)

    _auth_method = AuthenticationMethod(server_settings.get(_Settings.AuthenticationMethod))
    _token_verification: Optional[str] = None
    if _auth_method == AuthenticationMethod.Token:
        _token_verification = server_settings.get(_Settings.TokenVerification) or _DEFAULT_TOKEN_VERIFICATION

    return ServerConfig(
        listen_host=server_settings.get(_Settings.ListenHost),
        listen_port=server_settings.get(_Settings.ListenPort),
        advertise_host=server_settings.get(_Settings.AdvertiseHost),
        advertise_port=advertise_port,
        use_tls=use_tls,
        use_mutual_tls=use_mtls,
        tls_cert_and_key=tls_cert_and_key,
        tls_root_cert=tls_root_cert,
        authentication_method=_auth_method,
        token_header_name=server_settings.get(_Settings.TokenHeaderName),
        token_verification=_token_verification,
        task_threads=server_settings.get(_Settings.TaskThreads),
        task_close_threads=server_settings.get(_Settings.TaskCloseThreads),
        task_result_ttl_sec=server_settings.get(_Settings.TaskResultTtlSec),
        metrics_host=server_settings.get(_Settings.MetricsHost),
        metrics_port=server_settings.get(_Settings.MetricsPort),
        health_check_host=server_settings.get(_Settings.HealthcheckHost),
        health_check_port=server_settings.get(_Settings.HealthcheckPort),
        malloc_trim_interval_sec=server_settings.get(_Settings.MallocTrimIntervalSec),
        log_event_key_name=server_settings.get(_Settings.LogEventKeyName),
        log_trace_keys=dict(server_settings.get(_Settings.LogTraceKeys) or {}),
        otel_config=OtelConfig(
            exporter_type=OtelExporterType(exporter_type) if exporter_type is not None else None,
            service_name=server_settings.get(_Settings.OtelServiceName),
            service_namespace=server_settings.get(_Settings.OtelServiceNamespace),
            service_instance_id=server_settings.get(_Settings.OtelServiceInstanceId),
            extract_context_from_headers=server_settings.get(_Settings.OtelExtractContext),
        ),
    )


def _load_dynaconf(files: tuple[str, ...] = ()) -> Dynaconf:
    """
    Initializes Dynaconf instance, optionally using a set of configuration files. Dynaconf will read config
    from env variables with the `GDFS_` prefix. See: https://www.dynaconf.com/ to learn more.

    :param files: configuration files to read
    :returns
    """
    for file in files:
        if not os.path.exists(file):
            raise ValidationError(f"Settings file {file} does not exist.")
        elif not os.path.isfile(file):
            raise ValidationError(f"Path {file} is a directory and not a settings file.")

    return Dynaconf(
        settings_files=files,
        envvar_prefix="GOODDATA_FLIGHT",
        environments=False,
    )


def read_config(files: tuple[str, ...]) -> tuple[Dynaconf, ServerConfig]:
    settings = _load_dynaconf(files)
    settings.validators.register(*_VALIDATORS)
    settings.validators.validate()

    return settings, _create_server_config(settings)
