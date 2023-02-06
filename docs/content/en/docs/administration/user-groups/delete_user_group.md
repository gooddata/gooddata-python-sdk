---
title: "delete_user_group"
linkTitle: "delete_user_group"
weight: 70
no_list: true
superheading: "catalog_user."
---



``delete_user_group(user_group_id: str)``

Deletes user group using user group id.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_group_id" p_type="string" >}}
User group identification string. e.g. "123"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Delete user group
sdk.catalog_user.delete_user_group(user_group_id=user_group.id)
```
