# GoodData Python SDK

The `gooddata-sdk` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics:
* Catalog Service
* Insights Service
* Compute Service
* Table Service

Example of insight execution:
```python
import gooddata_sdk

# GoodData.CN host in the form of uri eg. "http://localhost:3000"
host = "http://localhost:3000"
# GoodData.CN user token
token = "some_user_token"
sdk = gooddata_sdk.GoodDataSdk.create(host, token)

workspace_id = "demo"
insight_id = "customers_trend"
# reads insight from workspace
insight = sdk.insights.get_insight(workspace_id, insight_id)
# triggers computation for the insight. the result will be returned in a tabular form
table = sdk.tables.for_insight(workspace_id, insight)

# and this is how you can read data row-by-row and do something with it
for row in table.read_all():
    print(row)
```

## Documentation

Documentation is available [here](https://gooddata-sdk.readthedocs.io)

## Bugs/Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues)` to submit bugs
or request features.

## Changelog

Consult [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for a released versions
and list of changes.
