---
title: "analyze_statistics"
linkTitle: "analyze_statistics"
weight: 10
no_list: true
superheading: "catalog_ai_lake."
api_ref: "CatalogAILakeService.analyze_statistics"
---



``analyze_statistics(instance_id: str, table_names: list[str] | None = None, operation_id: str | None = None) -> str``

Triggers `ANALYZE TABLE` over an AI Lake database instance so the
cost-based optimizer (CBO) picks up fresh statistics. Required after
schema or bulk-data changes — most importantly after registering a
pre-aggregation table whose dimension attributes the platform will later
resolve via filter pushdown.

The call returns immediately with an operation ID; the actual analyze
runs asynchronously. Use [`get_operation`](../get_operation/) or
[`wait_for_operation`](../wait_for_operation/) to poll for completion.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="instance_id" p_type="str" >}}
Database instance name (preferred) or UUID.
{{< /parameter >}}
{{< parameter p_name="table_names" p_type="list[str] | None" >}}
Tables to analyze. If `None` or empty, every table in the instance is
analyzed. Defaults to `None`.
{{< /parameter >}}
{{< parameter p_name="operation_id" p_type="str | None" >}}
Optional client-supplied operation identifier. If omitted, a fresh UUID
is generated. Pass the same value that subsequent
`get_operation` / `wait_for_operation` calls will poll on.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="operation_id" p_type="str" >}}
The operation ID (UUID string) the platform will track this run under.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
operation_id = sdk.catalog_ai_lake.analyze_statistics(
    instance_id="warehouse-prod",
    table_names=["agg_orders_country_daily", "agg_orders_country_monthly"],
)
sdk.catalog_ai_lake.wait_for_operation(operation_id)
```
