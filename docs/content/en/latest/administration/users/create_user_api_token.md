---
title: "create_user_api_token"
linkTitle: "create_user_api_token"
weight: 10
no_list: true
superheading: "catalog_user."
---



``create_user_api_token(user_id: str, api_token_id: str)``

Create a new user api token.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "admin"
{{< /parameter >}}
{{< parameter p_name="api_token_id" p_type="string" >}}
API token identification string. e.g. "admin_token"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="CatalogApiToken" >}}
Instance of CatalogApiToken holding the information about API token (its id, and bearer token).
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_user.create_user_api_token(user_id="admin", api_token_id="admin_token")
```
