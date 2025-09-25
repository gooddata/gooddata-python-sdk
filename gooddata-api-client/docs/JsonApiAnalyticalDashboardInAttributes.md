# JsonApiAnalyticalDashboardInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | Free-form JSON content. Maximum supported length is 250000 characters. | 
**description** | **str** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_in_attributes import JsonApiAnalyticalDashboardInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardInAttributes from a JSON string
json_api_analytical_dashboard_in_attributes_instance = JsonApiAnalyticalDashboardInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardInAttributes.to_json())

# convert the object into a dict
json_api_analytical_dashboard_in_attributes_dict = json_api_analytical_dashboard_in_attributes_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardInAttributes from a dict
json_api_analytical_dashboard_in_attributes_from_dict = JsonApiAnalyticalDashboardInAttributes.from_dict(json_api_analytical_dashboard_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


