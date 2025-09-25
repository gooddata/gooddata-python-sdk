# JsonApiAnalyticalDashboardPatch

JSON:API representation of patching analyticalDashboard entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardPatchAttributes**](JsonApiAnalyticalDashboardPatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_patch import JsonApiAnalyticalDashboardPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardPatch from a JSON string
json_api_analytical_dashboard_patch_instance = JsonApiAnalyticalDashboardPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardPatch.to_json())

# convert the object into a dict
json_api_analytical_dashboard_patch_dict = json_api_analytical_dashboard_patch_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardPatch from a dict
json_api_analytical_dashboard_patch_from_dict = JsonApiAnalyticalDashboardPatch.from_dict(json_api_analytical_dashboard_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


