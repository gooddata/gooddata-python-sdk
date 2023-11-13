---
title: "Logical Data Model"
linkTitle: "Logical Data Model"
weight: 20
no_list: true
---

Manage logical data models.

See [Create a Logical Data Model](https://www.gooddata.com/docs/cloud/model-data/create-ldm/) to learn abour logical data models in GoodData.

## Methods

* [get_declarative_ldm](./get_declarative_ldm/)
* [put_declarative_ldm](./put_declarative_ldm/)
* [store_declarative_ldm](./store_declarative_ldm/)
* [load_declarative_ldm](./load_declarative_ldm/)
* [load_and_put_declarative_ldm](./load_and_put_declarative_ldm/)
* [store_ldm_to_disk](./store_ldm_to_disk/)
* [load_ldm_from_disk](./load_ldm_from_disk/)

## Example

```python
from gooddata_sdk import GoodDataSdk
from pathlib import Path

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

declarative_ldm = sdk.get_declarative_ldm(workspace_id="123")
sdk.catalog_workspace_content.put_declarative_ldm(workspace_id="456", ldm=logical_model)
```
