---
title: "Workspaces"
linkTitle: "Workspaces"
weight: 10
no_list: true
---

Manage workspaces. Entity and Declarative methods are supported.

### Entity Methods

* [create_or_update](./create_or_update/)
* [get_workspace](./get_workspace/)
* [clone_workspace](./clone_workspace/)
* [delete_workspace](./delete_workspace/)
* [list_workspaces](./list_workspaces/)

### Declarative Methods

* [get_declarative_workspace](./get_declarative_workspace/)
* [put_declarative_workspace](./put_declarative_workspace/)
* [store_declarative_workspace](./store_declarative_workspace/)
* [load_declarative_workspace](./load_declarative_workspace/)
* [load_and_put_declarative_workspace](./load_and_put_declarative_workspace/)
* [get_declarative_workspaces](./get_declarative_workspaces/)
* [put_declarative_workspaces](./put_declarative_workspaces/)
* [store_declarative_workspaces](./store_declarative_workspaces/)
* [load_declarative_workspaces](./load_declarative_workspaces/)
* [load_and_put_declarative_workspaces](./load_and_put_declarative_workspaces/)
* [get_declarative_automations](./get_declarative_automations/)
* [put_declarative_automations](./put_declarative_automations/)


## Example

List, create, update and delete workspaces:

```python
from gooddata_sdk import GoodDataSdk, CatalogWorkspace

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# List workspaces
workspaces = sdk.catalog_workspace.list_workspaces()

print(workspaces)
# [
#   CatalogWorkspace(id=demo, name=Demo),
#   CatalogWorkspace(id=demo_west, name=Demo West),
#   CatalogWorkspace(id=demo_west_california, name=Demo West California)
# ]

# Create new workspace entity locally
my_workspace_object = CatalogWorkspace(workspace_id="test_demo",
                                        name="Test demo",
                                        parent_id="demo")

# Create workspace
sdk.catalog_workspace.create_or_update(workspace=my_workspace_object)

# Edit local workspace entity
my_workspace_object.name = "Test"

# Update workspace
sdk.catalog_workspace.create_or_update(workspace=my_workspace_object)

# Get workspace
workspace = sdk.catalog_workspace.get_workspace(workspace_id="test_demo")

print(workspace)
# CatalogWorkspace(id=test_demo, name=Test)

# Delete workspace
sdk.catalog_workspace.delete_workspace(workspace_id="test_demo")
```
