---
title: "delete_user"
linkTitle: "delete_user"
weight: 30
no_list: true
superheading: "catalog_user."
---



``delete_user(user_id: str)``

Deletes user using user id.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "123"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Delete a user
sdk.catalog_user.delete_user(user_id="abc")
```
