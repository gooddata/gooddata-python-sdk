---
title: "get_operation"
linkTitle: "get_operation"
weight: 20
no_list: true
superheading: "catalog_ai_lake."
api_ref: "CatalogAILakeService.get_operation"
---



``get_operation(operation_id: str) -> CatalogAILakeOperation``

Fetches the current state of a long-running AI Lake operation.

The returned `CatalogAILakeOperation` carries `id`, `kind`, `status`
(`"pending"`, `"succeeded"`, or `"failed"`), an optional `result` dict
on success, and an optional `error` dict on failure. Use the
`is_terminal` / `is_succeeded` / `is_failed` properties to branch on
status.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="operation_id" p_type="str" >}}
The operation ID returned by the action that started the operation
(e.g. `analyze_statistics`).
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="operation" p_type="CatalogAILakeOperation" >}}
Snapshot of the operation's current status and payload.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
operation_id = sdk.catalog_ai_lake.analyze_statistics(instance_id="warehouse-prod")
op = sdk.catalog_ai_lake.get_operation(operation_id)
if op.is_terminal:
    print(op.status, op.result or op.error)
```
