# JsonApiAnalyticalDashboardOutMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**access_info** | [**JsonApiAnalyticalDashboardOutMetaAccessInfo**](JsonApiAnalyticalDashboardOutMetaAccessInfo.md) |  | [optional] 
**origin** | [**JsonApiAggregatedFactOutMetaOrigin**](JsonApiAggregatedFactOutMetaOrigin.md) |  | [optional] 
**permissions** | **List[str]** | List of valid permissions for a logged-in user. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_meta import JsonApiAnalyticalDashboardOutMeta

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutMeta from a JSON string
json_api_analytical_dashboard_out_meta_instance = JsonApiAnalyticalDashboardOutMeta.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutMeta.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_meta_dict = json_api_analytical_dashboard_out_meta_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutMeta from a dict
json_api_analytical_dashboard_out_meta_from_dict = JsonApiAnalyticalDashboardOutMeta.from_dict(json_api_analytical_dashboard_out_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


