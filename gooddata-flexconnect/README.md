# GoodData FlexConnect

GoodData FlexConnect allows you to build your own data source for GoodData Cloud or Cloud Native.

FlexConnect works with a concept similar to 'table functions' that you may already know
from database technologies.

-  To build your own data source, you implement one or more FlexConnect functions. The
   functions compute and return tabular data - how they do it is completely up to you.
-  The functions are hosted and invoked inside a FlexConnect server (which is included in this package).
-  A running FlexConnect server can be added as a data source to your GoodData Cloud or GoodData Cloud Native.
-  The functions available on FlexConnect server will be mapped to data sets within GoodData's Semantic Model
   and from then on can be used during report computation.


## Getting Started using the FlexConnect Template

The easiest way to get started writing FlexConnect functions is to use [the template repository](https://github.com/gooddata/gooddata-flexconnect-template).
It provides a simple example of a FlexConnect function that can be used as a starting point for your own FlexConnect functions with all the necessary infrastructure in place.
It also has a README that explains how to get started with the template and some general tips on how to write FlexConnect functions.

## Getting started using the FlexConnect package directly

Install the package alongside the gooddata-flight-server using pip:

```bash
pip install gooddata-flight-server gooddata-flexconnect
```

Next, update the GoodData Flight Server configuration to load the FlexConnect functions.

```toml
[flexconnect]

# specify one or more modules that contain your FlexConnect function implementations
#
functions = [
    "flexconnect.your_function"
]
```

Then when running the GoodData Flight Server, use the `--methods-provider` option to load the FlexConnect.
For example:

```bash
#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVER_CMD="${SCRIPT_DIR}/.venv/bin/gooddata-flight-server"

export PYTHONPATH="${SCRIPT_DIR}/src"
export CONFIG_ENV="${1:-dev}"

$SERVER_CMD start \
              --methods-provider gooddata_flexconnect \
              --config \
                config/${CONFIG_ENV}.server.toml \
                config/flexconnect.config.toml \
              --logging-config config/default.logging.ini \
              --dev-log
```
