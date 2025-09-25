# JsonApiWorkspaceDataFilterSettingIn

JSON:API representation of workspaceDataFilterSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceDataFilterSettingInAttributes**](JsonApiWorkspaceDataFilterSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceDataFilterSettingInRelationships**](JsonApiWorkspaceDataFilterSettingInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_setting_in import JsonApiWorkspaceDataFilterSettingIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterSettingIn from a JSON string
json_api_workspace_data_filter_setting_in_instance = JsonApiWorkspaceDataFilterSettingIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterSettingIn.to_json())

# convert the object into a dict
json_api_workspace_data_filter_setting_in_dict = json_api_workspace_data_filter_setting_in_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterSettingIn from a dict
json_api_workspace_data_filter_setting_in_from_dict = JsonApiWorkspaceDataFilterSettingIn.from_dict(json_api_workspace_data_filter_setting_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


