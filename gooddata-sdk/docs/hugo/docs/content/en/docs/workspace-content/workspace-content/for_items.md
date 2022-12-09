---
title: "for_items"
linkTitle: "for_items"
weight: 11
superheading: "table."
---

<!-- TODO -->

``for_items(workspace_id: str, items: list[Union[Attribute, Metric]], filters: Optional[list[Filter]] = None)``

Returns *ExecutionTable*.

Retrieve data as an ExecutionTable from the given list of attributes/metrics, and filters.

## Example

```Python
# Get the items
items=[SimpleMetric(local_id="metric1", item=ObjId(type="metric", id="order_amount"))]
# Get the items as Execution Table
sdk.tables.for_items(workspace_id="123", items=items)

#ExecutionTable(
#   response=Execution(
#       workspace_id=demo,
#       result_id=7c2e246f64fdc7f6364724b4113ccd1162250758
#   ),
#   columns=['metric1'],
#   rows=1
# )
```
