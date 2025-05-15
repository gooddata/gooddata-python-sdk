# GoodData Python SDK

The `gooddata-sdk` package provides a clean and convenient Python API to interact with [GoodData](https://www.gooddata.com/).

At the moment the SDK provides services to inspect and interact with the Semantic Model and consume analytics:
* Catalog Workspaces Service
* Catalog Workspace Content Service
* Catalog Data Source Service
* Catalog User Service
* Catalog Permission Service
* Catalog Organization Service
* Visualizations Service
* Compute Service
* Table Service

See [DOCUMENTATION](https://www.gooddata.com/docs/python-sdk/1.42.0) for more details.

## Requirements

-  GoodData Cloud or GoodData.CN installation
-  Python 3.9 or newer

## Installation

Run the following command to install the `gooddata-sdk` package on your system:

    pip install gooddata-sdk

## Example

Compute an visualization:
```python
import gooddata_sdk

# GoodData host in the form of uri
host = "http://localhost:3000"
# GoodData user token
token = "some_user_token"
sdk = gooddata_sdk.GoodDataSdk.create(host, token)

workspace_id = "demo"
visualization_id = "customers_trend"
# reads visualization from workspace
visualization = sdk.visualizations.get_visualization(workspace_id, visualization_id)
# triggers computation for the visualization. the result will be returned in a tabular form
table = sdk.tables.for_visualization(workspace_id, visualization)

# and this is how you can read data row-by-row and do something with it
for row in table.read_all():
    print(row)
```


## Bugs & Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues) to submit bugs
or request features.

## Changelog

See  [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for released versions
and a list of changes.
