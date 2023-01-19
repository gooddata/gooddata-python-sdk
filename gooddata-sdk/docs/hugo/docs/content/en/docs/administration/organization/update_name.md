---
title: "update_name"
linkTitle: "update_name"
weight: 10
no_list: true
superheading: "catalog_organization."
---



``update_name(name: str)``

Updates the name of the organization.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="name" p_type="string" >}}
New name of the organization
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```python
# Update organization name
sdk.catalog_organization.update_name(name="new_organization_name")
```
