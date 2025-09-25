# JsonApiWorkspaceSettingOut

JSON:API representation of workspaceSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_setting_out import JsonApiWorkspaceSettingOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceSettingOut from a JSON string
json_api_workspace_setting_out_instance = JsonApiWorkspaceSettingOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceSettingOut.to_json())

# convert the object into a dict
json_api_workspace_setting_out_dict = json_api_workspace_setting_out_instance.to_dict()
# create an instance of JsonApiWorkspaceSettingOut from a dict
json_api_workspace_setting_out_from_dict = JsonApiWorkspaceSettingOut.from_dict(json_api_workspace_setting_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


