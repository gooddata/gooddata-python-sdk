# GoodData FlexFun

The GoodData FlexFun is a GoodData Flight Server-compatible extension that provides a set of functions for working with GoodData FlightRPC server.

## Usage

Install the package using pip:

```bash
pip install gooddata-flexfun
```

Then when running the GoodData Flight Server, use the `--methods-provider-module` option to load the FlexFun methods.
For example:

```bash
#!/bin/bash

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
SERVER_CMD="${SCRIPT_DIR}/.venv/bin/gooddata-flight-server"

export PYTHONPATH="${SCRIPT_DIR}/src"
export CONFIG_ENV="${1:-dev}"

$SERVER_CMD start \
              --methods-provider-module gooddata_flexfun \
              --config \
                config/${CONFIG_ENV}.server.toml \
                config/flexfun.config.toml \
              --logging-config config/default.logging.ini \
              --dev-log
```

This will start the GoodData Flight Server with the FlexFun methods loaded.
