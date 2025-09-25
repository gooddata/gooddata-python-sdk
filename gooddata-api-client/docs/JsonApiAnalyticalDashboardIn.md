# JsonApiAnalyticalDashboardIn

JSON:API representation of analyticalDashboard entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardInAttributes**](JsonApiAnalyticalDashboardInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_in import JsonApiAnalyticalDashboardIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardIn from a JSON string
json_api_analytical_dashboard_in_instance = JsonApiAnalyticalDashboardIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardIn.to_json())

# convert the object into a dict
json_api_analytical_dashboard_in_dict = json_api_analytical_dashboard_in_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardIn from a dict
json_api_analytical_dashboard_in_from_dict = JsonApiAnalyticalDashboardIn.from_dict(json_api_analytical_dashboard_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


