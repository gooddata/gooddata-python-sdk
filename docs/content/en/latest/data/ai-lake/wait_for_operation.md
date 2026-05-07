---
title: "wait_for_operation"
linkTitle: "wait_for_operation"
weight: 30
no_list: true
superheading: "catalog_ai_lake."
api_ref: "CatalogAILakeService.wait_for_operation"
---



``wait_for_operation(operation_id: str, timeout_s: float = 300.0, poll_s: float = 2.0) -> CatalogAILakeOperation``

Blocks until an AI Lake operation reaches a terminal status, polling
every `poll_s` seconds. Returns the final `CatalogAILakeOperation` on
success, raises `CatalogAILakeOperationError` if the operation finishes
in `failed` state, and raises `TimeoutError` if the operation does not
finish within `timeout_s`.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="operation_id" p_type="str" >}}
The operation ID returned by the action that started the operation.
{{< /parameter >}}
{{< parameter p_name="timeout_s" p_type="float" >}}
Maximum time to wait, in seconds. Defaults to `300.0`.
{{< /parameter >}}
{{< parameter p_name="poll_s" p_type="float" >}}
Sleep between polls, in seconds. Defaults to `2.0`.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="operation" p_type="CatalogAILakeOperation" >}}
The terminal-state operation; `op.is_succeeded` is guaranteed `True`.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Raises"%}}
{{< parameter p_type="CatalogAILakeOperationError" >}}
Operation finished with `status="failed"`. The exception carries the
full operation snapshot on its `operation` attribute.
{{< /parameter >}}
{{< parameter p_type="TimeoutError" >}}
Operation did not reach a terminal state within `timeout_s`.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
from gooddata_sdk import CatalogAILakeOperationError

operation_id = sdk.catalog_ai_lake.analyze_statistics(
    instance_id="warehouse-prod",
    table_names=["agg_orders_country_daily"],
)
try:
    op = sdk.catalog_ai_lake.wait_for_operation(operation_id, timeout_s=600.0)
except CatalogAILakeOperationError as exc:
    print(f"analyze failed: {exc.operation.error}")
except TimeoutError:
    print("analyze still pending; resume polling later with get_operation()")
```
