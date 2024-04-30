---
title: "get_user"
linkTitle: "get_user"
weight: 20
no_list: true
superheading: "catalog_user."
---



``get_user(user_id: str)``

Gets an individual user using user id.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "123"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogUser" >}}
user entity object.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get a user
user = sdk.catalog_user.get_user(user_id="abc")
```
