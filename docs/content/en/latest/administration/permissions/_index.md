---
title: "Permissions"
linkTitle: "Permissions"
weight: 20
no_list: true
---

Manage workspace permissions.

See [Manage Permissions](https://www.gooddata.com/docs/cloud/manage-deployment/manage-permissions/) to learn how permissions work in GoodData.

### Declarative Methods

* [get_declarative_permissions](./get_declarative_permissions/)
* [put_declarative_permissions](./put_declarative_permissions/)
* [get_declarative_organization_permissions](./get_declarative_organization_permissions/)
* [put_declarative_permissions](./put_declarative_organization_permissions/)
* [manage_organization_permissions](./manage_organization_permissions/)
* [list_available_assignees](./list_available_assignees/)
* [list_dashboard_permissions](./list_dashboard_permissions/)
* [manage_dashboard_permissions](./manage_dashboard_permissions/)

## Example

Get, modify and then set permissions for a given workspace:

```python
from gooddata_sdk import GoodDataSdk

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

workspace_id = "123"

# Get permissions in declarative from
declarative_permissions = sdk.catalog_permission.get_declarative_permissions(workspace_id=workspace_id)

declarative_permissions.permissions = []

# Update permissions on the server with your changes
sdk.catalog_permission.put_declarative_permissions(workspace_id=workspace_id,
                                                    declarative_workspace_permissions=declarative_permissions)
```
