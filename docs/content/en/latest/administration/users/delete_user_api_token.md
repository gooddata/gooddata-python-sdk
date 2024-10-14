---
title: "delete_user_api_token"
linkTitle: "delete_user_api_token"
weight: 10
no_list: true
superheading: "catalog_user."
---



``delete_user_api_token(user_id: str, api_token_id: str)``

Delete user api token.

{{% parameters-block  title="Parameters"%}}
{{< parameter p_name="user_id" p_type="string" >}}
User identification string. e.g. "admin"
{{< /parameter >}}
{{< parameter p_name="api_token_id" p_type="string" >}}
API token identification string. e.g. "admin_token"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_user.delete_user_api_token(user_id="admin", api_token_id="admin_token")
```
