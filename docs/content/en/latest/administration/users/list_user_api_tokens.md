---
title: "list_user_api_tokens"
linkTitle: "list_user_api_tokens"
weight: 10
no_list: true
superheading: "catalog_user."
---



``list_user_api_tokens(user_id: str)``

List all user API tokens.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "admin"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="list[CatalogApiToken]" >}}
List of CatalogApiToken instances holding the information about users API tokens.
Note that the bearer token is not returned. It will always be None.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_user.list_user_api_tokens(user_id="admin")
```
