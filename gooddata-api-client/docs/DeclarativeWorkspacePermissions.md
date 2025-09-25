# DeclarativeWorkspacePermissions

Definition of permissions associated with a workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hierarchy_permissions** | [**List[DeclarativeWorkspaceHierarchyPermission]**](DeclarativeWorkspaceHierarchyPermission.md) |  | [optional] 
**permissions** | [**List[DeclarativeSingleWorkspacePermission]**](DeclarativeSingleWorkspacePermission.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_workspace_permissions import DeclarativeWorkspacePermissions

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspacePermissions from a JSON string
declarative_workspace_permissions_instance = DeclarativeWorkspacePermissions.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspacePermissions.to_json())

# convert the object into a dict
declarative_workspace_permissions_dict = declarative_workspace_permissions_instance.to_dict()
# create an instance of DeclarativeWorkspacePermissions from a dict
declarative_workspace_permissions_from_dict = DeclarativeWorkspacePermissions.from_dict(declarative_workspace_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


