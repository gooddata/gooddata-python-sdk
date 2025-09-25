# DeclarativeWorkspaceHierarchyPermission


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_hierarchy_permission import DeclarativeWorkspaceHierarchyPermission

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceHierarchyPermission from a JSON string
declarative_workspace_hierarchy_permission_instance = DeclarativeWorkspaceHierarchyPermission.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceHierarchyPermission.to_json())

# convert the object into a dict
declarative_workspace_hierarchy_permission_dict = declarative_workspace_hierarchy_permission_instance.to_dict()
# create an instance of DeclarativeWorkspaceHierarchyPermission from a dict
declarative_workspace_hierarchy_permission_from_dict = DeclarativeWorkspaceHierarchyPermission.from_dict(declarative_workspace_hierarchy_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


