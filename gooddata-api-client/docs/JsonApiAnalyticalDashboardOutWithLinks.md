# JsonApiAnalyticalDashboardOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardOutAttributes**](JsonApiAnalyticalDashboardOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAnalyticalDashboardOutMeta**](JsonApiAnalyticalDashboardOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAnalyticalDashboardOutRelationships**](JsonApiAnalyticalDashboardOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_with_links import JsonApiAnalyticalDashboardOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutWithLinks from a JSON string
json_api_analytical_dashboard_out_with_links_instance = JsonApiAnalyticalDashboardOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutWithLinks.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_with_links_dict = json_api_analytical_dashboard_out_with_links_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutWithLinks from a dict
json_api_analytical_dashboard_out_with_links_from_dict = JsonApiAnalyticalDashboardOutWithLinks.from_dict(json_api_analytical_dashboard_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


