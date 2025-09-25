# UserManagementUsersItem

List of users

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**List[UserManagementDataSourcePermissionAssignment]**](UserManagementDataSourcePermissionAssignment.md) |  | 
**email** | **str** | User email address | [optional] 
**id** | **str** |  | 
**name** | **str** | User name | [optional] 
**organization_admin** | **bool** | Is user organization admin | 
**user_groups** | [**List[UserGroupIdentifier]**](UserGroupIdentifier.md) |  | 
**workspaces** | [**List[UserManagementWorkspacePermissionAssignment]**](UserManagementWorkspacePermissionAssignment.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_users_item import UserManagementUsersItem

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUsersItem from a JSON string
user_management_users_item_instance = UserManagementUsersItem.from_json(json)
# print the JSON string representation of the object
print(UserManagementUsersItem.to_json())

# convert the object into a dict
user_management_users_item_dict = user_management_users_item_instance.to_dict()
# create an instance of UserManagementUsersItem from a dict
user_management_users_item_from_dict = UserManagementUsersItem.from_dict(user_management_users_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


