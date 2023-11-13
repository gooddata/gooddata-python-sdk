---
title: "Workspace Data Filters"
linkTitle: "Workspace Data Filters"
weight: 50
no_list: true
---

Manage workspace data filters.

See [Set Up Data Filters in Workspaces](https://www.gooddata.com/docs/cloud/manage-deployment/manage-workspaces/workspace-data-filters/) to learn how workspace data filters work in GoodData.

## Methods

* [get_declarative_workspace_data_filters](./get_declarative_workspace_data_filters/)
* [put_declarative_workspace_data_filters](./put_declarative_workspace_data_filters/)
* [store_declarative_workspace_data_filters](./store_declarative_workspace_data_filters/)
* [load_declarative_workspace_data_filters](./load_declarative_workspace_data_filters/)
* [load_and_put_declarative_workspace_data_filters](./load_and_put_declarative_workspace_data_filters/)

## Example

```python
from gooddata_sdk import GoodDataSdk
from pathlib import Path

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

declarative_workspace_filters = sdk.catalog_workspace.get_declarative_workspace_data_filters()
len(declarative_workspace_filters.workspace_data_filters)
```
