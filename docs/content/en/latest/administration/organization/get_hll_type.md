---
title: "get_hll_type"
linkTitle: "get_hll_type"
weight: 31
no_list: true
superheading: "catalog_organization."
api_ref: "CatalogOrganizationService.get_hll_type"
---



``get_hll_type() -> HLLType | None``

Reads the organization-level `hyperLogLogType` setting. Returns the
configured value (`"Native"` or `"Presto"`), or `None` when the setting
is unset or carries an unrecognized value.

See [`set_hll_type`](../set_hll_type/) for the meaning of each value and
when to choose `"Native"` versus `"Presto"`.

{{% parameters-block title="Returns"%}}
{{< parameter p_name="value" p_type="HLLType | None" >}}
`"Native"`, `"Presto"`, or `None` if unset.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
current = sdk.catalog_organization.get_hll_type()
if current is None:
    sdk.catalog_organization.set_hll_type("Native")
```
