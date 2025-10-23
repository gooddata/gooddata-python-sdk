# (C) 2024 GoodData Corporation
"""
Logging configuration helper functions
"""

import os
from logging.config import fileConfig
from typing import Any, Optional, Union

import orjson
import structlog
from opentelemetry import trace
from structlog.typing import EventDict, WrappedLogger


def _resolve_config(logging_ini: str, for_module: Optional[str]) -> str:
    if os.path.isabs(logging_ini):
        return logging_ini
    else:
        conf_dir = os.path.dirname(for_module) if for_module is not None else os.path.curdir

        return os.path.join(conf_dir, logging_ini)


class _ORJsonRenderer:
    def __init__(self, output_bytes: bool = False):
        self._output_bytes = output_bytes

    @staticmethod
    def default(obj: Any) -> Any:
        # sets are not serializable by default, so convert them to lists
        if isinstance(obj, set):
            return list(obj)
        # otherwise, do nothing, this will make the default logic to kick in

    def __call__(self, logger: Any, name: str, event_dict: Any) -> Union[str, bytes]:
        if self._output_bytes:
            return orjson.dumps(event_dict, default=_ORJsonRenderer.default)

        return orjson.dumps(event_dict, default=_ORJsonRenderer.default).decode("UTF-8")


class _OtelTraceContextInjector:
    """
    Injects trace id, span id and parent span id obtained from current OpenTelemetry span.
    """

    __slots__ = ("_trace_id_key", "_span_id_key", "_parent_span_id_key")

    def __init__(self, trace_ctx_keys: Optional[dict[str, str]] = None) -> None:
        _keys = trace_ctx_keys or {}

        # do one-time lookup of the actual key names under which the different
        # otel info should be hammered. this exists here because server allows
        # admins to provide mapping between default trace/span/parent span
        # and desired key names.
        #
        # the mapping exists to improve fit into different contexts where
        # server is integrated. the default 'trace_id' and 'span_id' keys may
        # thwart observability experience if the rest of the system uses say 'traceId'
        # and 'spanId'.
        self._trace_id_key = _keys.get("trace_id", "trace_id")
        self._span_id_key = _keys.get("span_id", "span_id")
        self._parent_span_id_key = _keys.get("parent_span_id", "parent_span_id")

    def __call__(self, _: WrappedLogger, __: str, event_dict: EventDict) -> EventDict:
        span = trace.get_current_span()
        if span == trace.INVALID_SPAN:
            # bail out right away if the current span is not valid
            #
            # most typically, this happens if the log is being emitted while there is no
            # current span set (e.g. code runs outside a trace span -> very valid scenario)
            return event_dict

        span_ctx = span.get_span_context()
        event_dict[self._trace_id_key] = f"{span_ctx.trace_id:x}"
        event_dict[self._span_id_key] = f"{span_ctx.span_id:x}"

        parent_ctx: Optional[trace.SpanContext] = getattr(span, "parent", None)
        if parent_ctx:
            event_dict[self._parent_span_id_key] = f"{parent_ctx.span_id:x}"

        return event_dict


def _configure_structlog(
    dev_log: bool,
    event_key: str,
    add_trace_ctx: bool = False,
    trace_ctx_keys: Optional[dict[str, str]] = None,
) -> None:
    common_processors: list[Any] = [
        structlog.stdlib.filter_by_level,
        structlog.contextvars.merge_contextvars,
    ]

    if add_trace_ctx:
        common_processors.append(_OtelTraceContextInjector(trace_ctx_keys))

    common_processors.extend(
        [
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
        ]
    )

    if dev_log:
        processors: Any = common_processors + [structlog.dev.ConsoleRenderer()]
    else:
        processors = common_processors + [
            structlog.processors.EventRenamer(event_key),
            _ORJsonRenderer(),
        ]

    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def init_logging(
    logging_ini: str,
    dev_log: bool = False,
    event_key: str = "event",
    for_module: Optional[str] = None,
    add_trace_ctx: bool = False,
    trace_ctx_keys: Optional[dict[str, str]] = None,
) -> str:
    """
    Initializes python logging from the file on the provided path. If the path is absolute, then it is
    used as is. Otherwise lookup is done for a file relative to the provided module if it is specified; if not
    specified, lookup is done for file relative to the current directory.

    :param logging_ini: path to logging ini file
    :param dev_log: specify true to configure logging in development mode; this mode is more convenient
     during dev testing but not so suitable for production
    :param event_key: name of the event key (default event)
    :param for_module: optionally specify, module pathname; relative file config will be resolved
     in regard to this module directory; otherwise goes against current dir
    :param add_trace_ctx: optionally specify whether logging pipeline should include processor that hammers in
     otel tracing information (trace id, span id)
    :param trace_ctx_keys: optionally specify mapping for key names under which trace context will be dumped into
     log events. default values are 'trace_id', 'span_id' and 'parent_span_id'. The mapping allows to override
     those key names
    :return: pathname of log file that was used to configure
    """
    log_config = _resolve_config(logging_ini, for_module)
    fileConfig(log_config)
    _configure_structlog(dev_log, event_key, add_trace_ctx, trace_ctx_keys)

    return log_config
