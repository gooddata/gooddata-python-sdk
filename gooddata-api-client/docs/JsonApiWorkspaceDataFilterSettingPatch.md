# JsonApiWorkspaceDataFilterSettingPatch

JSON:API representation of patching workspaceDataFilterSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceDataFilterSettingInAttributes**](JsonApiWorkspaceDataFilterSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceDataFilterSettingInRelationships**](JsonApiWorkspaceDataFilterSettingInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_setting_patch import JsonApiWorkspaceDataFilterSettingPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterSettingPatch from a JSON string
json_api_workspace_data_filter_setting_patch_instance = JsonApiWorkspaceDataFilterSettingPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterSettingPatch.to_json())

# convert the object into a dict
json_api_workspace_data_filter_setting_patch_dict = json_api_workspace_data_filter_setting_patch_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterSettingPatch from a dict
json_api_workspace_data_filter_setting_patch_from_dict = JsonApiWorkspaceDataFilterSettingPatch.from_dict(json_api_workspace_data_filter_setting_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


