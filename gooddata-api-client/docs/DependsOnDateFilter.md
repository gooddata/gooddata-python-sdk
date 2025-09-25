# DependsOnDateFilter

Filter definition type for dates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_filter** | [**DateFilter**](DateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.depends_on_date_filter import DependsOnDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DependsOnDateFilter from a JSON string
depends_on_date_filter_instance = DependsOnDateFilter.from_json(json)
# print the JSON string representation of the object
print(DependsOnDateFilter.to_json())

# convert the object into a dict
depends_on_date_filter_dict = depends_on_date_filter_instance.to_dict()
# create an instance of DependsOnDateFilter from a dict
depends_on_date_filter_from_dict = DependsOnDateFilter.from_dict(depends_on_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


