# JsonApiWorkspaceOutMeta


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**config** | [**JsonApiWorkspaceOutMetaConfig**](JsonApiWorkspaceOutMetaConfig.md) |  | [optional] 
**data_model** | [**JsonApiWorkspaceOutMetaDataModel**](JsonApiWorkspaceOutMetaDataModel.md) |  | [optional] 
**hierarchy** | [**JsonApiWorkspaceOutMetaHierarchy**](JsonApiWorkspaceOutMetaHierarchy.md) |  | [optional] 
**permissions** | **List[str]** | List of valid permissions for a logged-in user. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_out_meta import JsonApiWorkspaceOutMeta

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOutMeta from a JSON string
json_api_workspace_out_meta_instance = JsonApiWorkspaceOutMeta.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOutMeta.to_json())

# convert the object into a dict
json_api_workspace_out_meta_dict = json_api_workspace_out_meta_instance.to_dict()
# create an instance of JsonApiWorkspaceOutMeta from a dict
json_api_workspace_out_meta_from_dict = JsonApiWorkspaceOutMeta.from_dict(json_api_workspace_out_meta_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


