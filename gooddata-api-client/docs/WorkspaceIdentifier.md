# WorkspaceIdentifier

A workspace identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the workspace. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.workspace_identifier import WorkspaceIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceIdentifier from a JSON string
workspace_identifier_instance = WorkspaceIdentifier.from_json(json)
# print the JSON string representation of the object
print(WorkspaceIdentifier.to_json())

# convert the object into a dict
workspace_identifier_dict = workspace_identifier_instance.to_dict()
# create an instance of WorkspaceIdentifier from a dict
workspace_identifier_from_dict = WorkspaceIdentifier.from_dict(workspace_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


