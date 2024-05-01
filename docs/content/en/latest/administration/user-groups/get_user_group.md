---
title: "get_user_group"
linkTitle: "get_user_group"
weight: 60
no_list: true
superheading: "catalog_user."
---



``get_user_group(user_group_id: str)``

Gets an individual user group using user group id.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="user_group_id" p_type="string" >}}
User Group identification string. e.g. "123"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogUserGroup" >}}
User group entity object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get a user group
user_group = sdk.catalog_user.get_user_group(user_group_id="demoGroup")
```
