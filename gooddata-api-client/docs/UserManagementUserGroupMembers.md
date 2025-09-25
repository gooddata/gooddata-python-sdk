# UserManagementUserGroupMembers


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**members** | [**List[UserManagementUserGroupMember]**](UserManagementUserGroupMember.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_user_group_members import UserManagementUserGroupMembers

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUserGroupMembers from a JSON string
user_management_user_group_members_instance = UserManagementUserGroupMembers.from_json(json)
# print the JSON string representation of the object
print(UserManagementUserGroupMembers.to_json())

# convert the object into a dict
user_management_user_group_members_dict = user_management_user_group_members_instance.to_dict()
# create an instance of UserManagementUserGroupMembers from a dict
user_management_user_group_members_from_dict = UserManagementUserGroupMembers.from_dict(user_management_user_group_members_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


