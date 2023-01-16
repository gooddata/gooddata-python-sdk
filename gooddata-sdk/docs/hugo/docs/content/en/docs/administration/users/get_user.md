---
title: "get_user"
linkTitle: "get_user"
weight: 20
no_list: true
superheading: "catalog_user."
---

<!-- TODO -->

``get_user(user_id: str)``

Get an individual user using User id.

## Example

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

```python
# Get a user
user = sdk.catalog_user.get_user(user_id="abc")
```
