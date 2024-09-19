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

Here is a very simple example of the data service Flight RPC methods implementation:

```python
import gooddata_flight_server as gf
import pyarrow.flight


class DataServiceMethods(gf.FlightServerMethods):
  """
  This example data service serves some sample static data. Any
  DoGet request will return that static data. All other Flight RPC
  methods are left unimplemented.
  """

  StaticData = pyarrow.table({
    "col1": [1, 2, 3]
  })

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
  return DataServiceMethods()


if __name__ == "__main__":
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

The CLI will look up the `my_service.main` Python module and look for a function decorated
with `@flight_server_methods`. It will start the server and make it initialize your data service
implementation and integrate it into the Flight RPC server.

NOTE: the CLI also has other arguments that let you specify configuration files to load and
logging configuration to use.

## Manual

### Configuration

### Observability

### Health Checks

### Authentication

##
