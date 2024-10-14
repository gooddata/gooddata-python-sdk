---
title: "get_user_api_token"
linkTitle: "get_user_api_token"
weight: 10
no_list: true
superheading: "catalog_user."
---



``get_user_api_token(user_id: str, api_token_id: str)``

Get user api token.

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
Instance of CatalogApiToken holding the information about API token.
Note that the bearer token is not returned. It will always be None.
{{< /parameter >}}
{{% /parameters-block %}}
## Example

```python
sdk.catalog_user.get_user_api_token(user_id="admin", api_token_id="admin_token")
```
