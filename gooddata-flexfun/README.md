# GoodData FlexFun

The GoodData FlexFun package is a GoodData Flight Server-compatible extension
that provides a framework for hosting custom pluggable functions called FlexFuns.
These can be used to act as a dataset for GoodData FlightRPC data sources.

## What is a FlexFun?

In essence, FlexFun is a class that provides a set of methods that can be called by the GoodData Cloud when data is
requested from the corresponding FlightRPC data source dataset.

Each FlexFun provides a `name` used to identify the FlexFun in the GoodData Cloud.
FlexFuns can provide a set of `metadata` that can further influence when and how they are called by GoodData Cloud.
They also provide a `schema` (defined in terms
of [pyarrow.Schema](https://arrow.apache.org/docs/python/generated/pyarrow.Schema.html))
that describes the shape of data that the FlexFun can provide.
Finally, they provide a set of methods that can be called to provide data in response to queries:
* `call` - called to provide data in response to a query
* `cancel` - called to cancel a query if GoodData Cloud decides to stop requesting data (e.g. if there is a timeout)
* `on_load` - called when the FlexFun is created before any `call` or `cancel` methods are called

## Getting Started using the FlexFun Template

The easiest way to get started writing FlexFuns is to use [the template repository](https://github.com/gooddata/gooddata-flexfun-template).
It provides a simple example of a FlexFun that can be used as a starting point for your own FlexFun with all the necessary infrastructure in place.
It also has a README that explains how to get started with the template and some general tips on how to write FlexFuns.

## Getting started using the FlexFun package directly

Install the package alongside the gooddata-flight-server using pip:

```bash
pip install gooddata-flight-server gooddata-flexfun
```

Next, update the GoodData Flight Server configuration to load the FlexFun methods.

```toml
[flexfun]

# specify one or more modules that contain your FlexFun implementations
#
functions = [
    "flexfun.your_function"
]
```

Then when running the GoodData Flight Server, use the `--methods-provider` option to load the FlexFun methods.
For example:

```bash
#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVER_CMD="${SCRIPT_DIR}/.venv/bin/gooddata-flight-server"

export PYTHONPATH="${SCRIPT_DIR}/src"
export CONFIG_ENV="${1:-dev}"

$SERVER_CMD start \
              --methods-provider gooddata_flexfun \
              --config \
                config/${CONFIG_ENV}.server.toml \
                config/flexfun.config.toml \
              --logging-config config/default.logging.ini \
              --dev-log
```

This will start the GoodData Flight Server with the FlexFun methods loaded.
