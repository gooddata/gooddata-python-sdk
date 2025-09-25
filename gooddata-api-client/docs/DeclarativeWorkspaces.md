# DeclarativeWorkspaces

A declarative form of a all workspace layout.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_data_filters** | [**List[DeclarativeWorkspaceDataFilter]**](DeclarativeWorkspaceDataFilter.md) |  | 
**workspaces** | [**List[DeclarativeWorkspace]**](DeclarativeWorkspace.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_workspaces import DeclarativeWorkspaces

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaces from a JSON string
declarative_workspaces_instance = DeclarativeWorkspaces.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaces.to_json())

# convert the object into a dict
declarative_workspaces_dict = declarative_workspaces_instance.to_dict()
# create an instance of DeclarativeWorkspaces from a dict
declarative_workspaces_from_dict = DeclarativeWorkspaces.from_dict(declarative_workspaces_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


