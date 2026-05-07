---
title: "AI Lake"
linkTitle: "AI Lake"
weight: 20
no_list: true
---

Drive AI Lake long-running operations from the SDK. Today the surface
covers the actions needed by aggregate-aware logical data models — most
notably the `ANALYZE TABLE` refresh that pre-aggregation workflows rely
on so the cost-based optimizer picks up new statistics.

The AI Lake API uses long-running operations: an action returns
immediately with an `operation_id`, and the client polls until the
operation reaches a terminal status (`succeeded` or `failed`).

### Action Methods

* [analyze_statistics](./analyze_statistics/)

### Operation Methods

* [get_operation](./get_operation/)
* [wait_for_operation](./wait_for_operation/)

## Example

```python
from gooddata_sdk import GoodDataSdk

sdk = GoodDataSdk.create(host="https://demo.gooddata.com", token="<token>")

# Refresh CBO statistics for a single table after a bulk load.
operation_id = sdk.catalog_ai_lake.analyze_statistics(
    instance_id="warehouse-prod",
    table_names=["agg_orders_country_daily"],
)

# Block until the operation finishes; raises CatalogAILakeOperationError
# on failure and TimeoutError if it doesn't finish in time.
op = sdk.catalog_ai_lake.wait_for_operation(operation_id, timeout_s=600.0)
assert op.is_succeeded
```
