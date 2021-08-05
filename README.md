# GoodData.CN Python Foundations

This repository contains Python packages useful for integration with GoodData.CN:

-  gooddata-afm-client, gooddata-metadata-client: low-level API clients generated from GD.CN Open API specifications
-  gooddata-sdk: a Python SDK providing added value functions and convenience layers on top of the clients
-  gooddata-fdw: a GD.CN Foreign Data Wrapper for PostgreSQL

Code is compatible with Python 3.9 or newer.

## API Clients

These are generated using the openapi-generator. The generated clients are fairly convoluted and can be tricky
to use. They do work with some known issues and allow you to call any metadata or computation API in your GoodData.CN
installation.

### Known issues

The complexity of some of the GD.CN API schemas combined with the bugs in the generated code mean you may need to
disable return type checking and/or type checking when creating model objects.

Use the `_check_return_type=False` keyword parameter when calling generated API client methods to disable return
type checking. For example:

```python
import gooddata_metadata_client.apis as metadata_apis

api = metadata_apis.WorkspaceObjectControllerApi()
metrics = api.get_all_entities_metrics('workspace_id', size=500, _check_return_type=False)
```

Use the `_check_type=False` keyword parameter when creating objects from generated models. For example:

```python
import gooddata_afm_client.models as afm_models

afm_models.RelativeDateFilterBody(dataset=..., granularity=..., _from=..., to=..., _check_type=False)
```

## Python SDK

The Python SDK aims to provide cleaner APIs and convenience layers on top of the generated clients.

For instance behold how it is possible to read an Insight from GD.CN server, trigger its computation and then
read the data:

```python
import gooddata_sdk

sdk = gooddata_sdk.GoodDataSdk(HOST, TOKEN)

# reads insight from workspace
insight = sdk.insights.get_insight(workspace_id, insight_id)

# triggers computation for the insight. the result will be returned in a tabular form
table = sdk.tables.for_insight(workspace_id, insight)

# and this is how you can read data row-by-row and do something with it
for row in table.read_all():
    print(row)
```

## GoodData.CN Foreign Data Wrapper for PostgreSQL

Foreign Data Wrapper (FDW) presents a way to map GoodData.CN semantic layer and/or insights stored in your GoodData.CN
into PostgreSQL as foreign tables that you can then query using SQL.

Check out the [gooddata-fdw package](./gooddata-fdw) documentation to learn more and get started.

## GoodData to pandas adapters

The [gooddata-pandas](./gooddata-pandas) is a thin layer that utilizes Python SDK and allows you to conveniently
create pandas series and data frames.
