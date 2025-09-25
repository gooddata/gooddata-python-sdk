# DashboardDateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_filter** | [**DashboardDateFilterDateFilter**](DashboardDateFilterDateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.dashboard_date_filter import DashboardDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardDateFilter from a JSON string
dashboard_date_filter_instance = DashboardDateFilter.from_json(json)
# print the JSON string representation of the object
print(DashboardDateFilter.to_json())

# convert the object into a dict
dashboard_date_filter_dict = dashboard_date_filter_instance.to_dict()
# create an instance of DashboardDateFilter from a dict
dashboard_date_filter_from_dict = DashboardDateFilter.from_dict(dashboard_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


