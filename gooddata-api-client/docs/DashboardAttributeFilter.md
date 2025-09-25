# DashboardAttributeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_filter** | [**DashboardAttributeFilterAttributeFilter**](DashboardAttributeFilterAttributeFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.dashboard_attribute_filter import DashboardAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardAttributeFilter from a JSON string
dashboard_attribute_filter_instance = DashboardAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(DashboardAttributeFilter.to_json())

# convert the object into a dict
dashboard_attribute_filter_dict = dashboard_attribute_filter_instance.to_dict()
# create an instance of DashboardAttributeFilter from a dict
dashboard_attribute_filter_from_dict = DashboardAttributeFilter.from_dict(dashboard_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


