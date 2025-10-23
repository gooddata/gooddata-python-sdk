# GoodData Pandas

This package contains a thin layer that utilizes gooddata-sdk and allows you to conveniently create pandas series and
data frames from the computations done against semantic model in your [GoodData.CN](https://www.gooddata.com/developers/cloud-native/) workspace.

See [DOCUMENTATION](https://gooddata-pandas.readthedocs.io/en/latest/) for more details.

## Requirements

-  GoodData.CN installation; either running on your cloud
   infrastructure or the free Community Edition running on your workstation

-  Python 3.9 or newer

## Installation

Run the following command to install the `gooddata-pandas` package on your system:

    pip install gooddata-pandas

## Example

Create an indexed and a not-indexed series:

```python
from gooddata_pandas import GoodPandas

# GoodData.CN host in the form of uri eg. "http://localhost:3000"
host = "http://localhost:3000"
# GoodData.CN user token
token = "some_user_token"
# initialize the adapter to work on top of GD.CN host and use the provided authentication token
gp = GoodPandas(host, token)

workspace_id = "demo"
series = gp.series(workspace_id)

# create indexed series
indexed_series = series.indexed(index_by="label/label_id", data_by="fact/measure_id")

# create non-indexed series containing just the values of measure sliced by elements of the label
non_indexed = series.not_indexed(data_by="fact/measure_id", granularity="label/label_id")
```

## Bugs & Requests

Please use the [GitHub issue tracker](https://github.com/gooddata/gooddata-python-sdk/issues) to submit bugs
or request features.

## Changelog

Consult [Github releases](https://github.com/gooddata/gooddata-python-sdk/releases) for a released versions
and list of changes.
