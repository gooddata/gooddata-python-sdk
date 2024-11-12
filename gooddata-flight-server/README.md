# GoodData Flight Server

The GoodData Flight Server is an opinionated, pluggable Flight RPC Server implementation.

It builds on top of the Flight RPC components provided by [PyArrow](https://pypi.org/project/pyarrow/) and
on functions and capabilities typically needed when building production-ready
Flight RPC data services:

- A robust configuration system leveraging [Dynaconf](https://www.dynaconf.com/)
- Enablement of data service observability (logging, metrics, tracing)
- Health checking exposed via liveness and readiness endpoints
- Token-based authentication with pluggable token verification methods

Next to this, the server also comes with infrastructure that you can leverage
for building data service functionality itself:

- Library for generating and serving Flights created using long-running tasks
- Extendable error handling infrastructure that allows your service to
  provide error information in structured manner

Code in this package is derived from our production codebase, where we run
and operate many different data services and have this infrastructure proven
and battle-tested.

## Getting Started

The `gooddata-flight-server` package is like any other. You can install it
using `pip install gooddata-flight-server` or - more common - add it as dependency
to your project.

The server takes care of all the boilerplate, and you take care of implementing
the Flight RPC methods - similar as you would implement them using PyArrow's Flight
server.

Here is a very simple example of the data service's Flight RPC methods implementation:

```python
import gooddata_flight_server as gf
import pyarrow.flight


class DataServiceMethods(gf.FlightServerMethods):
  """
  This example data service serves some sample static data. Any
  DoGet request will return that static data. All other Flight RPC
  methods are left unimplemented.

  Note how the class holds onto the `ServerContext` - the implementations
  will usually want to do this because the context contains additional
  dependencies such as:

  - Location to send out in FlightInfo
  - Health monitor that the implementation can use to indicate
    its status
  - Task executor to perform long-running tasks
  """

  StaticData = pyarrow.table({
    "col1": [1, 2, 3]
  })

  def __init__(self, ctx: gf.ServerContext) -> None:
    self._ctx = ctx

  def do_get(self,
             context: pyarrow.flight.ServerCallContext,
             ticket: pyarrow.flight.Ticket
             ) -> pyarrow.flight.FlightDataStream:
    return pyarrow.flight.RecordBatchStream(
      self.StaticData
    )


@gf.flight_server_methods
def my_service(ctx: gf.ServerContext) -> gf.FlightServerMethods:
  """
  Factory function for the data service. It returns implementation of Flight RPC
  methods which are then integrated into the server.

  The ServerContext passed in `ctx` allows you to access available configuration
  and various useful server components.
  """
  return DataServiceMethods(ctx)


if __name__ == "__main__":
  # additional options & config files can be passed to the
  # create_server methods; more on this later
  server = gf.create_server(my_service)
  server.start()

  # the main thread will block on this call
  #
  # SIGINT/SIGTERM causes graceful shutdown - the method will
  # exit once server is stopped.
  server.wait_for_stop()
```

Notice the annotated `my_service` function. This is a factory for your data service's
Flight RPC methods. The server will call it out at appropriate time during the startup.
It will pass you the full context available at the time from where your code can access:

- available configuration loaded using Dynaconf
- health-checking components
- components to use for running long-running tasks.

During startup, the server will register signal handlers for SIGINT and SIGTERM - it will
perform graceful shutdown and tear everything down in the correct order when it receives them.

The server also comes with a simple CLI that you can use to start it up and load particular
data service:

```shell
$ gooddata-flight-server start --methods-provider my_service.main
```

The CLI will import the `my_service.main` Python module and look for a function decorated
with `@flight_server_methods`. It will start the server and make it initialize your data service
implementation and integrate it into the Flight RPC server.

Without any configuration, the server will bind to `127.0.0.1:17001` and run without TLS and not
use any authentication. It will not start health check or metric endpoints and will not start
the OpenTelemetry exporters.

NOTE: the CLI also has other arguments that let you specify configuration files to load and
logging configuration to use.

### Configuration

The server uses [Dynaconf](https://www.dynaconf.com/) to for all its configuration. There are
many settings already in place to influence server's configuration and behavior. Your data service
code can also leverage Dynaconf config to configure itself: you can pass any number of configuration
files / env variables at startup; the server will load them all using Dynaconf and let your code
work with Dynaconf structures.

We recommend you to check out the Dynaconf documentation to learn more about how it works and
what are the capabilities. This text will only highlight the most common usage.

The available server settings are documented in the [sample-config.toml](sample-config.toml).
You can take this and use it as template for your own configuration.

To use a configuration file during startup, you can start the server like this:

```shell
$ gooddata-flight-server start \
  --methods-provider my_service.main \
  --config server.config.toml
```

In case your service needs its own configuration, it is often a good idea to keep it in
a separate file and add that to startup:

```shell
$ gooddata-flight-server start \
  --methods-provider my_service.main \
  --config server.config.toml my_service.config.toml
```

#### Environment variables

All settings that you can code into the config file can be also provided using environment
variables.

The server's Dynaconf integration is set up so that all environment variables are
expected to be prefixed with `GOODDATA_FLIGHT_`.

The environment variable naming convention is set up by Dynaconf and goes as follows:
`GOODDATA_FLIGHT_{SECTION}__{SETTING_NAME}`

Where the `SECTION` is for example `[server]`. For convenience, the [sample-config.toml](sample-config.toml)
indicates the full name of respective environment variable in each setting's documentation.

#### Configuration for your service

If your service needs its own configuration, you should aim to have a TOML config file like this:

```toml
[my_service]
# env: GOODDATA_FLIGHT_MY_SERVICE__OPT1
opt1 = "value"
```

When you provide such config file to server, it will parse it and make its contents available in the `ctx.settings`.
You can then access value of this setting in your factory function. For example like this:

```python
import gooddata_flight_server as gf

_MY_CONFIG_SECTION = "my_service"

@gf.flight_server_methods
def my_service(ctx: gf.ServerContext) -> gf.FlightServerMethods:
    opt1 = ctx.settings.get(f"{_MY_CONFIG_SECTION}.opt1")

    # ... create and return server methods ...
```

### Authentication

Currently, the server supports two modes of authentication:

- no authentication
- token-based authentication and allows you to plug in custom token verification logic

The token verification method that comes built-in with the server is a simple one: the token is
an arbitrary, secret value shared between server and client. You configure the list of valid secret
tokens at server start-up and then at your discretion distribute these secret values to clients.

By default, the server runs with no authentication. To turn on the token based authentication,
you have to:

- Set the `authentication_method` setting to `token`.

  By default, the server will use the built-in token verification strategy
  called `EnumeratedTokenVerification`.

- Configure the secret tokens.

  You can do this using environment variable: `GOODDATA_FLIGHT_ENUMERATED_TOKENS__TOKENS='["", ""]'`.
  Put the secret token(s) inside the quotes. Alternatively, you can code tokens into a configuration file
  such as this:

  ```toml
  [enumerated_tokens]
  tokens = ["", ""]
  ```

  IMPORTANT: never commit secrets to your VCS.

With this setup in place, the server will expect the Flight clients to include token in the
`authorization` header in form of `Bearer <token>`. The token must be present on every
call.

Here is an example how to make a call that includes the `authorization` header:

```python
import pyarrow.flight

def example_call_using_tokens():
    opts = pyarrow.flight.FlightCallOptions(headers=[(b"authorization", b"Bearer <token>")])
    client = pyarrow.flight.FlightClient("grpc+tls://localhost:17001")

    for flight in client.list_flights(b"", opts):
        print(flight)
```

## Developer Manual

This part of the documentation explains additional capabilities of the server.

### Long-running tasks

Part of this package is a component that you can use to generate Flight data using long-running
tasks: the `TaskExecutor` component. The server will configure and create an instance of TaskExecutor
at startup; your server can access it via `ServerContext`.

The `TaskExecutor` implementation wraps on top of `ThreadPoolExecutor`: you can configure the number of
threads available for your tasks using `task_threads` setting. Each active task will use one thread from
this pool. If all threads are occupied, the tasks will be queued using FIFO strategy.

To use the `TaskExecutor`, you have to encapsulate the Flight data generation logic into a class
that extends the `Task` interface. Here, in the `run()` method you implement the necessary
algorithm that generates data.

The `Task` interface comes with a contract how your code should return the result (data) or raise
errors. The `TaskExecutor` will hold onto the results generated by your task and retain them for
a configured amount of time (see `task_result_ttl_sec` setting). The infrastructure recognizes that
your task may generate result that can be consumed either repeatedly (say Arrow Tables) or just
once (say RecordBatchReader backed by live stream).

Here is an example showing how to code a task, how to integrate its execution and how to
send out data that it generated:

```python
from typing import Union, Any

import pyarrow.flight

import gooddata_flight_server as gf


class MyServiceTask(gf.Task):
    def __init__(
            self,
            task_specific_payload: Any,
            cmd: bytes,
    ):
        super().__init__(cmd)

        self._task_specific_payload = task_specific_payload

    def run(self) -> Union[gf.TaskResult, gf.TaskError]:
        # tasks support cancellation; your code can check for
        # cancellation at any time; if the task was cancelled the
        # method will raise exception.
        #
        # do not forget to do cleanup on cancellation
        self.check_cancelled()

        # ... do whatever is needed to generate the data
        data: pyarrow.RecordBatchReader = some_method_to_generate_data()

        # when the data is ready, wrap it in a result that implements
        # the FlightDataTaskResult interface; there are built-in implementations
        # to wrap Arrow Table or Arrow RecordBatchReader.
        #
        # you can write your own result if you need special handling
        # of result and/or resources bound to the result.
        return gf.FlightDataTaskResult.for_data(data)


class DataServiceMethods(gf.FlightServerMethods):
    def __init__(self, ctx: gf.ServerContext) -> None:
        self._ctx = ctx

    def _prepare_flight_info(self, task_result: gf.TaskExecutionResult) -> pyarrow.flight.FlightInfo:
        if task_result.error is not None:
            raise task_result.error.as_flight_error()

        if task_result.cancelled:
            raise gf.ErrorInfo.for_reason(
                gf.ErrorCode.COMMAND_CANCELLED,
                f"Service call was cancelled. Invocation task was: '{task_result.task_id}'.",
            ).to_server_error()

        result = task_result.result

        return pyarrow.flight.FlightInfo(
            schema=result.get_schema(),
            descriptor=pyarrow.flight.FlightDescriptor.for_command(task_result.cmd),
            endpoints=[
                pyarrow.flight.FlightEndpoint(
                    ticket=pyarrow.flight.Ticket(ticket=task_result.task_id.encode()),
                    locations=[self._ctx.location],
                )
            ],
            total_records=-1,
            total_bytes=-1,
        )

    def get_flight_info(
            self,
            context: pyarrow.flight.ServerCallContext,
            descriptor: pyarrow.flight.FlightDescriptor,
    ) -> pyarrow.flight.FlightInfo:
        cmd = descriptor.command
        # parse & validate the command
        some_parsed_command = ...

        # create your custom task; you will usually pass the parsed command
        # so that task knows what to do. The 'raw' command is required as well because
        # it should be bounced back in the FlightInfo
        task = MyServiceTask(task_specific_payload=some_parsed_command, cmd=cmd)
        self._ctx.task_executor.submit(task)

        # wait for the task to complete
        result = self._ctx.task_executor.wait_for_result(task_id=task.task_id)

        # once the task completes, create the FlightInfo or raise exception in
        # case the task failed. The ticket in the FlightInfo should contain the
        # task identifier.
        return self._prepare_flight_info(result)

    def do_get(self,
               context: pyarrow.flight.ServerCallContext,
               ticket: pyarrow.flight.Ticket
               ) -> pyarrow.flight.FlightDataStream:
        # caller comes to pick the data; the ticket should be the task identifier
        task_id = ticket.ticket.decode()

        # this utility method on the base class takes care of everything needed
        # to correctly create FlightDataStream from the task result (or die trying
        # in case the task result is no longer preset, or the result indicates that
        # the task has failed)
        return self.do_get_task_result(context, self._ctx.task_executor, task_id)
```

### Custom token verification strategy

At the moment, the built-in token verification strategy supported by the server is the
most basic one. In cases when this strategy is not good enough, you can code your own
and plug it into the server.

The `TokenVerificationStrategy` interface sets contract for your custom strategy. You
implement this class inside a Python module and then tell the server to load that
module.

For example, you create a module `my_service.auth.custom_token_verification` where you
implement the verification strategy:

```python
import gooddata_flight_server as gf
import pyarrow.flight
from typing import Any


class MyCustomTokenVerification(gf.TokenVerificationStrategy):
    def verify(self, call_info: pyarrow.flight.CallInfo, token: str) -> Any:
        # implement your arbitrary logic here;
        #
        # see method and class documentation to learn more
        raise NotImplementedError

    @classmethod
    def create(cls, ctx: gf.ServerContext) -> "TokenVerificationStrategy":
        # code has chance to read any necessary settings from `ctx.settings`
        # property and then use those values to construct the class
        #
        # see method and class documentation to learn more
        return MyCustomTokenVerification()
```

Then, you can use the `token_verification` setting to tell the server to look up
and load token verification strategy from `my_service.auth.custom_token_verification` module.

Using custom verification strategy, you can implement support for say JWT tokens or look
up valid tokens inside some database.

NOTE: As is, the server infrastructure does not concern itself with how the clients actually
obtain the valid tokens. At the moment, this is outside of this project's scope. You can distribute
tokens to clients using some procedure or implement custom APIs where clients have to log in
in order to obtain a valid token.

### Logging

The server comes with the `structlog` installed by default. The `structlog` is used and configured
so that it uses Python stdlib logging backend. The `structlog` pipeline is set up so that:

- In dev mode, the logs are pretty-printed into console (achieved by `--dev-log` option of the server)
- In production deployment, the logs are serialized into JSON (using orjson) which is then written out.
  This is ideal for consumption in log aggregators.

By default, the stdlib loggers are configured using the [default.logging.ini](./gooddata_flight_server/server/default.logging.ini)
file. In the default setup, all INFO-level logs are emitted.

If you want to customize the logging configuration, then:

- make a copy of this file and tweak it as you need
- either pass path to your config file to the `create_server` function or use `--logging-config`
  argument on the CLI

The config file is the standard Python logging configuration file. You can learn about its intricacies
in Python documentation.

NOTE: you typically do not want to touch the formatter settings inside the logging ini file - the
`structlog` library creates the entire log lines accordingly to deployment mode.

The use of `structlog` and loggers is fairly straightforward:

```python
import structlog

_LOGGER = structlog.get_logger("my_service")
_LOGGER.info("event-name", some_event_key="value_to_log")
```

#### Recommendations

Here are few assorted recommendations based on our production experience with `structlog`:

- You can log complex objects such as lists, tuples, dicts and data classes no problem
  - Be careful though. What can be serialized into dev-log may not always serialize
    using `orjson` into production logs
- Always log exceptions using the special [exc_info](https://www.structlog.org/en/stable/exceptions.html) event key.
- Mind the cardinality of the logger instances. If you have a class of which you may have thousands of
  instances, then it is **not a good idea** to create a logger instance for each instance of your class - even
  if the logger name is the same; this is because each logger instance comes with memory overhead.

### Prometheus Metrics

The server can be configured to start HTTP endpoint that exposes values of Prometheus
metrics. This is disabled by default.

To get started with Prometheus metrics you need to:

- Set `metrics_host` and `metrics_port`

  - Check out the config file comments to learn more about these settings.
  - What you have to remember is that the Prometheus scraper is an external process that
    needs to reach the HTTP endpoint via network.

From then on, you can start using the Prometheus client to create various types of metrics. For example:

```python
from prometheus_client import Counter

# instantiate counter
MY_COUNTER = Counter(
    "my_counter",
    "Fitting description of `my_counter`.",
)

def some_function():
    # ...
    MY_COUNTER.inc()
```

#### Recommendations

Here are a few assorted recommendations based on our production experience:

- You must avoid double-declaration of metrics. If you try to define metric with same
  identifier twice, the registration will fail.

- It is nice to declare all/most metrics in single place. For example create `my_metrics.py`
  file and in that have `MyMetrics` class with one static field per metric.

  This approach leads to better 'discoverability' of available metrics just by looking
  at code. Using class with static field per-metric in turn makes imports and autocomplete
  more convenient.

### Open Telemetry

The server can be configured to integrate with OpenTelemetry and start and auto-configure
OpenTelemetry exporters. It will also auto-fill the ResourceAttributes by doing discovery where possible.

See the `otel_*` options in the configuration files to learn more. In a nutshell it
goes as follows:

- Configure which exporter to use using `otel_exporter_type` setting.

  Nowadays, the `otlp-grpc` or `otlp-http` is the usual choice.

  Depending on the exporter you use, you may/must specify additional, exporter-specific
  environment variables to configure the exporter. The supported environment variables
  are documented in the respective OpenTelemetry exporter package; e.g. they are not
  something special to GoodData's Flight Server.

  See [official exporter documentation](https://opentelemetry-python.readthedocs.io/en/latest/exporter/otlp/otlp.html#module-opentelemetry.exporter.otlp.proto.grpc).

- Install the respective exporter package.

- Tweak the other `otel_*` settings: you must at minimum set the `otel_service_name`

  The settings apart from `otel_service_name` will fall back to defaults.

To start tracing, you need to initialize a tracer. You can do so as follows:

```python
from opentelemetry import trace

MY_TRACER: trace.Tracer = trace.ProxyTracer("my_tracer")
```

Typically, you want to create one instance of tracer for your entire data service and then
import that instance and use it wherever needed to create spans:

```python
from your_module_with_tracer import MY_TRACER

def some_function():
    # ... code
    with MY_TRACER.start_as_current_span("do_some_work") as span:
        # ... code
        pass
```

Note: there are many ways to instrument your code with spans. See [OpenTelemetry documentation](https://opentelemetry.io/docs/languages/python/instrumentation/)
to find out more.

#### Recommendations

Here are a few assorted recommendations based on our production experience:

- Always use the `ProxyTracer`. The underlying initialization code done by the server
  will correctly set the actual tracer that will be called from the ProxyTracer.

  This way, if you turn off OpenTelemetry (by commenting out the `otel_export_type` setting or setting it
  to 'none'), the NoOpTracer will be injected under the covers and all the tracing code will
  be no-op as well.

### Health Checks

The server comes with a basic health-checking infrastructure - this is especially useful
when deploying to environments (such as k8s) that monitor health of your server and can automatically
restart it in case of problems.

When you configure the `health_check_host` (and optionally also `health_check_port`) setting, the
server will expose two HTTP endpoints:

- `/ready` - indicates whether the server is up and ready to serve requests

  The endpoint will respond with status `500` if the server is not ready. Otherwise will respond with
  `202`. The server is deemed ready when all its modules are up and the Flight RPC server is
  'unlocked' to handle requests.

- `/live` - indicates whether the server is still alive and can be used. The liveness is determined
  from the status of the modules.

  Each of the server's modules can report its status to a central health checking service. If any of
  the modules is unhealthy, the whole server is unhealthy.

  Similar to the readiness, the server will respond with status `500` when not healthy. Otherwise, it
  will respond with status `202`.

Creating health-checks is fairly straightforward:

- Your service's factory function receives `ServerContext`

  - The `ServerContext` contains `health` property - which returns an instance of `ServerHealthMonitor`

  - At this occasion, your code should hold onto / propagate the health monitor to any mission-critical
    modules / components used by your implementation

- The `ServerHealthMonitor` has `set_module_status(module, status)` method - you can use this to indicate status

  - The module `name` argument to this method can be anything you see fit
  - The status is either `ModuleHealthStatus.OK` or `ModuleHealthStatus.NOT_OK`
  - When your module is `NOT_OK`, the entire server is `NOT_OK`
  - Usually, there is a grace period for which the server can be `NOT_OK`; after the time is up,
    environment will restart the server
  - If you return your module back to `OK` status, the server returns to `OK` status as well - thus
    avoiding the automatic restarts.

Here is an example component using health monitoring:

```python
import gooddata_flight_server as gf

class YourMissionCriticalComponent:
    """
    Let's say this component is used to perform some heavy lifting / important job.

    The component is created in your service's factory and is used during Flight RPC
    invocation. You propagate the `health` monitor to it at construction time.
    """
    def __init__(self, health: gf.ServerHealthMonitor) -> None:
        self._health = health

    def some_important_method(self):
        try:
            # this does some important work
            return
        except OSError:
            # it runs into some kind of unrecoverable error (OSError here is purely example);
            # by setting the status to NOT_OK, your component indicates that it is unhealthy
            # and the /live endpoint will report the entire server as unhealthy.
            #
            # usually, the liveness checks have a grace period. if you set the module back
            # to `gf.ModuleHealthStatus.OK` everything turns healthy again. If the grace
            # period elapses, the server will usually be restarted by the environment.
            self._health.set_module_status("YourMissionCriticalComponent", gf.ModuleHealthStatus.NOT_OK)
            raise
```

## Troubleshooting

### Clients cannot read data during GetFlightInfo->DoGet flow; getting DNS errors

The root cause here is usually misconfiguration of `listen_host` and `advertise_host`

You must always remember that `GetFlightInfo` returns a `FlightInfo` that is used
by clients to obtain the data using `DoGet`. The `FlightInfo` contains the location(s)
that the client will connect to - they must be reachable by the client.

There are a few things to check:

1. Ensure that your service implementation correctly sets Location in the FlightInfo

   Usually, you want to set the location to the value that your service implementation
   receives in the `ServerContext`. This location is prepared by the server and contains
   the value of `advertise_host` and `advertise_port`.

2. Ensure that the `advertise_host` is set correctly; mistakes can happen easily especially
   in dockerized environments. The documentation of `listen_host` and `advertise_host`
   has additional detail.

   To highlight specifics of Dockerized deployment:

   - The server most often needs to listen on `0.0.0.0`
   - The server must, however, advertise different hostname/IP - one that is reachable from
     outside the container

### The server's RSS keeps on growing; looks like server leaking memory

This can be usually observed on servers that are write-heavy: servers that handle a lot
of `DoPut` or `DoExchange` requests. When such servers run in environments that enforce
RSS limits, they can end up killed.

Often, this not a leak but a behavior of `malloc`. Even if you tell PyArrow to use
the `jemalloc` allocator, the underlying gRPC server used by Flight RPC will use `malloc` and
by default `malloc` will take its time returning unused memory back to the system.

And since the gRPC server is responsible for allocating memory for the received Arrow data,
it is often the `DoPut` or `DoExchange` workload that look like leaking memory.

If the RSS size is a problem (say you are running service inside k8s with memory limit), the
usual strategy is to:

1. Set / tweak malloc behavior using `GLIBC_TUNABLES` environment variable; reduce
   the malloc trim threshold and possibly also reduce number of malloc arenas

   Here is a quite aggressive: `GLIBC_TUNABLES="glibc.malloc.trim_threshold=4:glibc.malloc.arena_max=2:glibc.malloc.tcache_count=0"`

2. Periodically call `malloc_trim` to poke malloc to trim any unneeded allocations and
   return them to the system.

   The GoodData Flight server already implements period malloc trim. By default, the interval
   is set to `30 seconds`. You can change this interval using the `malloc_trim_interval_sec`
   setting.

Additionally, we recommend to read up on [Python Memory Management](https://realpython.com/python-memory-management/) -
especially the part where CPython is not returning unused blocks back to the system. This may be another reason for
RSS growth - the tricky bit here being that it really depends on object creation patterns in your service.
