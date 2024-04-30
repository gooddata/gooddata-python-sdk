---
title: "for_items"
linkTitle: "for_items"
weight: 11
superheading: "tables."
---



``for_items(workspace_id: str, items: list[Union[Attribute, Metric]], filters: Optional[list[Filter]] = None)``

Gets data as an ExecutionTable from the given list of attributes/metrics, and filters.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{< parameter p_name="items" p_type="list[Union[Attribute, Metric]]" >}}
Attributes and Metrics bundled together.
{{< /parameter >}}
{{< parameter p_name="filters" p_type="Optional[list[Filter]]" >}}
List of filters to be applied.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="ExecutionTable" >}}
Visualization data wrapper object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get the items
items=[SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount"))]
# Get the items as Execution Table
sdk.tables.for_items(workspace_id="123", items=items)

# ExecutionTable(
#   response=Execution(
#       workspace_id=demo,
#       result_id=7c2e246f64fdc7f6364724b4113ccd1162250758
#   ),
#   columns=['metric1'],
#   rows=1
# )
```
