# JsonApiAnalyticalDashboardOut

JSON:API representation of analyticalDashboard entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardOutAttributes**](JsonApiAnalyticalDashboardOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAnalyticalDashboardOutMeta**](JsonApiAnalyticalDashboardOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAnalyticalDashboardOutRelationships**](JsonApiAnalyticalDashboardOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out import JsonApiAnalyticalDashboardOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOut from a JSON string
json_api_analytical_dashboard_out_instance = JsonApiAnalyticalDashboardOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOut.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_dict = json_api_analytical_dashboard_out_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOut from a dict
json_api_analytical_dashboard_out_from_dict = JsonApiAnalyticalDashboardOut.from_dict(json_api_analytical_dashboard_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


