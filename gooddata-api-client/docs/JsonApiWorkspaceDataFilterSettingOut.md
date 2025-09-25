# JsonApiWorkspaceDataFilterSettingOut

JSON:API representation of workspaceDataFilterSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceDataFilterSettingInAttributes**](JsonApiWorkspaceDataFilterSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiWorkspaceDataFilterSettingInRelationships**](JsonApiWorkspaceDataFilterSettingInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_setting_out import JsonApiWorkspaceDataFilterSettingOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterSettingOut from a JSON string
json_api_workspace_data_filter_setting_out_instance = JsonApiWorkspaceDataFilterSettingOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterSettingOut.to_json())

# convert the object into a dict
json_api_workspace_data_filter_setting_out_dict = json_api_workspace_data_filter_setting_out_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterSettingOut from a dict
json_api_workspace_data_filter_setting_out_from_dict = JsonApiWorkspaceDataFilterSettingOut.from_dict(json_api_workspace_data_filter_setting_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


