# JsonApiWorkspaceSettingOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_setting_out_with_links import JsonApiWorkspaceSettingOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceSettingOutWithLinks from a JSON string
json_api_workspace_setting_out_with_links_instance = JsonApiWorkspaceSettingOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceSettingOutWithLinks.to_json())

# convert the object into a dict
json_api_workspace_setting_out_with_links_dict = json_api_workspace_setting_out_with_links_instance.to_dict()
# create an instance of JsonApiWorkspaceSettingOutWithLinks from a dict
json_api_workspace_setting_out_with_links_from_dict = JsonApiWorkspaceSettingOutWithLinks.from_dict(json_api_workspace_setting_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


