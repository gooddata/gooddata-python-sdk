# DashboardDateFilterDateFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**IdentifierRef**](IdentifierRef.md) |  | [optional] 
**bounded_filter** | [**RelativeBoundedDateFilter**](RelativeBoundedDateFilter.md) |  | [optional] 
**data_set** | [**IdentifierRef**](IdentifierRef.md) |  | [optional] 
**var_from** | [**DashboardDateFilterDateFilterFrom**](DashboardDateFilterDateFilterFrom.md) |  | [optional] 
**granularity** | **str** |  | 
**local_identifier** | **str** |  | [optional] 
**to** | [**DashboardDateFilterDateFilterFrom**](DashboardDateFilterDateFilterFrom.md) |  | [optional] 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.dashboard_date_filter_date_filter import DashboardDateFilterDateFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardDateFilterDateFilter from a JSON string
dashboard_date_filter_date_filter_instance = DashboardDateFilterDateFilter.from_json(json)
# print the JSON string representation of the object
print(DashboardDateFilterDateFilter.to_json())

# convert the object into a dict
dashboard_date_filter_date_filter_dict = dashboard_date_filter_date_filter_instance.to_dict()
# create an instance of DashboardDateFilterDateFilter from a dict
dashboard_date_filter_date_filter_from_dict = DashboardDateFilterDateFilter.from_dict(dashboard_date_filter_date_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


