---
title: "set_hll_type"
linkTitle: "set_hll_type"
weight: 30
no_list: true
superheading: "catalog_organization."
api_ref: "CatalogOrganizationService.set_hll_type"
---



``set_hll_type(value: HLLType)``

Sets the organization-level `hyperLogLogType` setting that controls which
HyperLogLog function family the platform uses when generating SQL over HLL
synopses.

The call is idempotent: it updates the existing setting or creates it if
absent.

| value | when to use |
| -- | -- |
| `"Native"` | StarRocks-native HLL functions. The default. Use when synopses are produced by the platform itself or by a StarRocks-native pipeline. |
| `"Presto"` | Presto-compatible HLL functions. Use when synopses arrive from an upstream Presto pipeline — the binary layout and hash family of Presto HLL synopses differ from StarRocks-native. Requires the StarRocks deployment to carry the Presto HLL UDFs. |

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="value" p_type="HLLType" >}}
Either `"Native"` or `"Presto"` (a `Literal` type re-exported from
`gooddata_sdk` as `HLLType`).
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
from gooddata_sdk import GoodDataSdk

sdk = GoodDataSdk.create(host="https://demo.gooddata.com", token="<token>")

# Customer ingests pre-aggregated tables whose HLL columns were produced by
# Presto. Switch the org so calcique emits Presto-compatible HLL SQL.
sdk.catalog_organization.set_hll_type("Presto")
```
