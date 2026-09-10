# gooddata-flight-server

A batteries-included Arrow Flight RPC server framework built on `pyarrow.flight`. It owns
everything around the RPC methods themselves — process bootstrap, graceful start/stop
lifecycle, layered configuration, structured logging, Prometheus metrics, OpenTelemetry
tracing, health endpoints and pluggable token authentication — so that a downstream service
only has to implement the Flight methods and point the CLI at them.

Consumed as a framework, including by projects outside this repo, so its public surface is
an external contract.

## Owns

- The Flight RPC server runtime and its `gooddata-flight-server` CLI
- Server bootstrap, lifecycle, health monitoring, observability and auth integration
- `TaskExecutor` and the task model for long-running Flight data generation
- Configuration patterns for hosting custom Flight method providers

## Does NOT Own

- Core GoodData Cloud domain, catalog and compute APIs → `gooddata-sdk`. This package has
  **no dependency on `gooddata-sdk`** and is generic Flight infrastructure.
- Product-specific data source functions and semantic model mapping → `gooddata-flexconnect`
- Lifecycle provisioning and backup workflows → `gooddata-pipelines`

## Architecture

**Entry point**: `gooddata_flight_server.cli:server_cli`.

**Key stack**: `pyarrow.flight` for transport, `dynaconf` for configuration,
`opentelemetry-api`/`-sdk` and `prometheus-client` for telemetry, `structlog` for logging,
`readerwriterlock` and `orjson` internally.

### The methods-provider contract

A hosting module must contain **exactly one** function decorated with
`@flight_server_methods`, with the signature `(ctx: ServerContext) -> FlightServerMethods`.
The CLI's `--methods-provider <dotted.module>` resolves it: the module is imported and
scanned, and zero or multiple decorated functions raise `FlightMethodsModuleError`. The
`ServerContext` handed in carries the settings, the health monitor and the `TaskExecutor`.

### Lifecycle is a template method

`ServerBase` drives `start()`, `stop()`, `abort()`, `wait_for_start()` and
`wait_for_stop()` on a dedicated main thread with condition-variable handshakes, and
defines the extension points subclasses implement: `_startup_services()`,
`_shutdown_services()`, `_abort_services()`, plus an optional `_pre_startup()` hook.
`GoodDataFlightServer` is the concrete implementation the CLI uses. New startup or shutdown
behavior belongs in those hooks, not in an ad hoc code path.

## Public API surface

The re-exports in `src/gooddata_flight_server/__init__.py` **are** the contract — roughly
36 names, including `ServerConfig`, `ServerContext`, `FlightServerMethods`,
`FlightServerMethodsFactory`, `create_server`, `GoodDataFlightServer`, `Task`, `TaskResult`,
`TaskExecutor`, `TaskError`, `ArrowData`, `TokenVerificationStrategy`,
`TokenAuthMiddleware`, `ErrorInfo`, `ErrorCode`, `RetryInfo`, `ServerHealthMonitor`,
`CallInfo`, `CallFinalizer` and `flight_server_methods`.

Everything else under `server/`, `tasks/`, `config/`, `health/` and `utils/` is internal
and freely refactorable. Changing or removing anything reachable as `gf.<name>` is a
breaking change for out-of-repo consumers, so treat that file as the thing to check before
renaming.

## Configuration

`--config` takes an ordered list of TOML files handed to Dynaconf with
`envvar_prefix="GOODDATA_FLIGHT"` and `environments=False`. Environment overrides follow
`GOODDATA_FLIGHT_{SECTION}__{SETTING}`. The `[server]` section is validated against a fixed
schema; any other section passes through untouched into `ctx.settings` for service-specific
config — which is how `gooddata-flexconnect` gets its own keys.

## Authentication

`authentication_method` is `none` or `token`. Under `token`, `token_verification` names
either the built-in `EnumeratedTokenVerification` or a dotted module path; the loader takes
the first class in that module subclassing `TokenVerificationStrategy` and instantiates it
via its `create(ctx)` classmethod. The token arrives as `Bearer <token>` in the
`authorization` Flight call header.

## Testing

Package-local pytest suites under `tests/`.

The suite uses **checked-in** certificates at `tests/server/tls/*.pem`, loaded by
`tests/server/conftest.py`. `make dev-certs` is *not* a prerequisite for running tests — it
writes a fresh CA/server/client chain into the gitignored `test_data/`, which nothing in the
test suite reads, and exists for driving the server by hand with TLS or mTLS enabled.
