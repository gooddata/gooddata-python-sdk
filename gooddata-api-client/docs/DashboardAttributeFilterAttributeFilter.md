# DashboardAttributeFilterAttributeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_elements** | [**AttributeElements**](AttributeElements.md) |  | 
**display_form** | [**IdentifierRef**](IdentifierRef.md) |  | 
**filter_elements_by** | [**List[AttributeFilterParent]**](AttributeFilterParent.md) |  | [optional] 
**filter_elements_by_date** | [**List[AttributeFilterByDate]**](AttributeFilterByDate.md) |  | [optional] 
**local_identifier** | **str** |  | [optional] 
**negative_selection** | **bool** |  | 
**selection_mode** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**validate_elements_by** | [**List[IdentifierRef]**](IdentifierRef.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.dashboard_attribute_filter_attribute_filter import DashboardAttributeFilterAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardAttributeFilterAttributeFilter from a JSON string
dashboard_attribute_filter_attribute_filter_instance = DashboardAttributeFilterAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(DashboardAttributeFilterAttributeFilter.to_json())

# convert the object into a dict
dashboard_attribute_filter_attribute_filter_dict = dashboard_attribute_filter_attribute_filter_instance.to_dict()
# create an instance of DashboardAttributeFilterAttributeFilter from a dict
dashboard_attribute_filter_attribute_filter_from_dict = DashboardAttributeFilterAttributeFilter.from_dict(dashboard_attribute_filter_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


