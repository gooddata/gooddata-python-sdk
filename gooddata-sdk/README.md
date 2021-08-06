# GoodData Python SDK

The `gooddata-sdk` package aims to provide clean and convenient Python APIs to interact with GoodData.CN.

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics.

## Services

### Catalog Service

DOC TBD

### Insights Service

DOC TBD

### Compute Service

DOC TBD

### Table Service

A convenience service that allows you to consume analytics in typical tabular format. The service allows free-form
computations and computations of data for GoodData.CN Insights.

For instance behold how it is possible to get tabular data for an insight defined on your GD.CN server:

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
