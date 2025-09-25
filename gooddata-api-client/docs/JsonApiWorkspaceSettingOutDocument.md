# JsonApiWorkspaceSettingOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiWorkspaceSettingOut**](JsonApiWorkspaceSettingOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceSettingOutDocument from a JSON string
json_api_workspace_setting_out_document_instance = JsonApiWorkspaceSettingOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceSettingOutDocument.to_json())

# convert the object into a dict
json_api_workspace_setting_out_document_dict = json_api_workspace_setting_out_document_instance.to_dict()
# create an instance of JsonApiWorkspaceSettingOutDocument from a dict
json_api_workspace_setting_out_document_from_dict = JsonApiWorkspaceSettingOutDocument.from_dict(json_api_workspace_setting_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


