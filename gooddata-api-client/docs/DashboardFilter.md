# DashboardFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_filter** | [**DashboardAttributeFilterAttributeFilter**](DashboardAttributeFilterAttributeFilter.md) |  | 
**date_filter** | [**DashboardDateFilterDateFilter**](DashboardDateFilterDateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.dashboard_filter import DashboardFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardFilter from a JSON string
dashboard_filter_instance = DashboardFilter.from_json(json)
# print the JSON string representation of the object
print(DashboardFilter.to_json())

# convert the object into a dict
dashboard_filter_dict = dashboard_filter_instance.to_dict()
# create an instance of DashboardFilter from a dict
dashboard_filter_from_dict = DashboardFilter.from_dict(dashboard_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


