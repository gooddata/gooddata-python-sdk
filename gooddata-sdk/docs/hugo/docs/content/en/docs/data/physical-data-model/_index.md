---
title: "Physical Data Model"
linkTitle: "Physical Data Model"
weight: 10
no_list: true
---

Manage physical data models.

See [Create a Physical Data Model](https://www.gooddata.com/developers/cloud-native/doc/cloud/model-data/create-pdm/) to about the physical data model in GoodData.

## Methods

* [get_declarative_pdm](./get_declarative_pdm/)
* [put_declarative_pdm](./put_declarative_pdm/)
* [store_declarative_pdm](./store_declarative_pdm/)
* [load_declarative_pdm](./load_declarative_pdm/)
* [load_and_put_declarative_pdm](./load_and_put_declarative_pdm/)
* [scan_and_put_pdm](./scan_and_put_pdm/)
* [store_pdm_to_disk](./store_pdm_to_disk/)
* [load_pdm_from_disk](./load_pdm_from_disk/)

## Example

```python
from gooddata_sdk import GoodDataSdk
from pathlib import Path

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

# Get all data sources
ds_objects = sdk.catalog_data_source.get_declarative_data_sources()

print(ds_objects.data_sources[0])
# CatalogDeclarativeDataSource(id=demo-test-ds, type=POSTGRESQL)

# Put data sources with credentials and test data source connection before put
sdk.catalog_data_source.put_declarative_data_sources(
    declarative_data_sources=ds_objects,
    credentials_path=Path("credentials"),
    test_data_sources=True
)
```
