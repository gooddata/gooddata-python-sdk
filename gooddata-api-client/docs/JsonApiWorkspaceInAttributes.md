# JsonApiWorkspaceInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cache_extra_limit** | **int** |  | [optional] 
**data_source** | [**JsonApiWorkspaceInAttributesDataSource**](JsonApiWorkspaceInAttributesDataSource.md) |  | [optional] 
**description** | **str** |  | [optional] 
**early_access** | **str** | The early access feature identifier. It is used to enable experimental features. Deprecated in favor of earlyAccessValues. | [optional] 
**early_access_values** | **List[str]** | The early access feature identifiers. They are used to enable experimental features. | [optional] 
**name** | **str** |  | [optional] 
**prefix** | **str** | Custom prefix of entity identifiers in workspace | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_in_attributes import JsonApiWorkspaceInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceInAttributes from a JSON string
json_api_workspace_in_attributes_instance = JsonApiWorkspaceInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceInAttributes.to_json())

# convert the object into a dict
json_api_workspace_in_attributes_dict = json_api_workspace_in_attributes_instance.to_dict()
# create an instance of JsonApiWorkspaceInAttributes from a dict
json_api_workspace_in_attributes_from_dict = JsonApiWorkspaceInAttributes.from_dict(json_api_workspace_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


