---
title: "Users and User Groups"
linkTitle: "Users and User Groups"
weight: 50
no_list: true
---

Manage users and user groups together.

See [Manage Permissions](https://www.gooddata.com/docs/cloud/manage-deployment/manage-permissions/) to learn how permissions work in GoodData.

### Declarative Methods

* [get_declarative_users_user_groups](./get_declarative_users_user_groups/)
* [put_declarative_users_user_groups](./put_declarative_users_user_groups/)
* [store_declarative_users_user_groups](./store_declarative_users_user_groups/)
* [load_declarative_users_user_groups](./load_declarative_users_user_groups/)
* [load_and_put_declarative_users_user_groups](./load_and_put_declarative_users_user_groups/)

## Example
List, create and delete users and user groups:

```python
from gooddata_sdk import GoodDataSdk
from pathlib import Path

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

users_and_user_groups = sdk.catalog_user.get_declarative_users_user_groups()

len(users_and_user_groups.users)

len(users_and_user_groups.user_groups)
```
