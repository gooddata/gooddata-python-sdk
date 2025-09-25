# JsonApiWorkspaceSettingIn

JSON:API representation of workspaceSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_setting_in import JsonApiWorkspaceSettingIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceSettingIn from a JSON string
json_api_workspace_setting_in_instance = JsonApiWorkspaceSettingIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceSettingIn.to_json())

# convert the object into a dict
json_api_workspace_setting_in_dict = json_api_workspace_setting_in_instance.to_dict()
# create an instance of JsonApiWorkspaceSettingIn from a dict
json_api_workspace_setting_in_from_dict = JsonApiWorkspaceSettingIn.from_dict(json_api_workspace_setting_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


