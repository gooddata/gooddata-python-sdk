# gooddata-flexconnect

Lets a developer expose their own tabular data as a data source inside GoodData, using a
table-function model: you subclass `FlexConnectFunction`, declare a name and an Arrow
schema, and implement `call()`. A FlexConnect server — `gooddata-flight-server` plus this
package's method provider — discovers your functions at startup, and GoodData maps each
one's schema to a dataset in the semantic model, invoking it over Flight RPC.

Consumed as a framework by projects outside this repo (see the `gooddata-flexconnect-template`
repository), so the function-authoring contract is an external API.

## Owns

- The `FlexConnectFunction` contract for authoring table-function style data sources
- Function registration and discovery
- The typed execution-context decoding of the request payload
- The Flight RPC glue that turns a generic Flight server into a FlexConnect server

## Does NOT Own

- Generic Flight server infrastructure, CLI, config and telemetry → `gooddata-flight-server`
- Core GoodData Cloud domain, catalog and compute APIs → `gooddata-sdk`
- PostgreSQL FDW integration → `gooddata-fdw`

## Architecture

**Depends on**: `gooddata-flight-server` and `gooddata-sdk`, plus `pyarrow`, `dynaconf`,
`structlog`, `orjson`.

All code lives under `src/gooddata_flexconnect/function/`: the base class, the registry,
the execution context, and the Flight methods.

### Authoring a function

A function is a **class**, not a callable. Subclass `FlexConnectFunction` and provide:

- `Name: str` — unique across the server; required
- `Schema: pyarrow.Schema` — the full result schema, declared statically; required
- `call(self, parameters, columns, headers) -> ArrowData` — the implementation

Optional overrides: `create()` (instance factory, called per invocation), `cancel()`, and
the static `on_load(ctx: ServerContext)` for one-time initialization.

### Discovery

Functions are not registered by hand. The server reads the `flexconnect.functions` setting
— a list of importable module paths — and `FlexConnectFunctionRegistry.load()` imports each
module and registers every top-level member that subclasses `FlexConnectFunction`. A
missing or empty `Name`, a duplicate `Name`, or a missing `Schema` raises at load time and
aborts startup. A function that is not exported at module top level is simply never found.

### Hosting

`create_flexconnect_flight_methods` is decorated with `@flight_server_methods` from
`gooddata-flight-server` and returns the `FlightServerMethods` implementation — it is the
single methods factory that turns the generic server into a FlexConnect server. It also
reads `flexconnect.call_deadline_ms` and `flexconnect.polling_interval_ms`.

## Gotchas

**Decode `parameters`, don't hand-parse it.** `call()` receives `parameters` as a raw
JSON-like dict. Use `ExecutionContext.from_parameters(parameters)` — it returns `None` when
there is no `executionContext` key, and otherwise a typed object exposing
`execution_type`, `organization_id`, `workspace_id`, `user_id` and either a
`ReportExecutionRequest` (attributes, metrics, filters) or a `LabelElementsExecutionRequest`.
Because this is public API consumed downstream, hand-rolled parsing in external projects
breaks silently on any wire-format change.

**`columns` is a trimming hint, not a contract.** The full result schema is fixed on the
class before any call. `columns` tells you which of those the caller wants and may be
ignored; it must not change aggregation semantics. Only `parameters` should drive
computation. Conflating "requested columns" with "requested aggregation" is the subtle
correctness trap here.

**Calls are asynchronous with a deadline.** Invocations run as background tasks with a
configurable call deadline and cancellation support, and the RPC layer supports polling for
long-running calls. Relevant when debugging timeouts.

## Testing

Package-local pytest suites under `tests/`. `make dev-certs` generates a CA/server/client
chain into the gitignored `test_data/` for driving a server by hand over TLS; the package
also ships its own checked-in certificates for the tests themselves.
