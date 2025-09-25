# UserManagementUserGroupsItem

List of groups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**List[UserManagementDataSourcePermissionAssignment]**](UserManagementDataSourcePermissionAssignment.md) |  | 
**id** | **str** |  | 
**name** | **str** | Group name | [optional] 
**organization_admin** | **bool** | Is group organization admin | 
**user_count** | **int** | The number of users belonging to the group | 
**workspaces** | [**List[UserManagementWorkspacePermissionAssignment]**](UserManagementWorkspacePermissionAssignment.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_user_groups_item import UserManagementUserGroupsItem

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUserGroupsItem from a JSON string
user_management_user_groups_item_instance = UserManagementUserGroupsItem.from_json(json)
# print the JSON string representation of the object
print(UserManagementUserGroupsItem.to_json())

# convert the object into a dict
user_management_user_groups_item_dict = user_management_user_groups_item_instance.to_dict()
# create an instance of UserManagementUserGroupsItem from a dict
user_management_user_groups_item_from_dict = UserManagementUserGroupsItem.from_dict(user_management_user_groups_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


