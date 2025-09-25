# UserManagementUserGroupMember


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | [optional] [readonly] 

## Example

```python
from gooddata_api_client.models.user_management_user_group_member import UserManagementUserGroupMember

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUserGroupMember from a JSON string
user_management_user_group_member_instance = UserManagementUserGroupMember.from_json(json)
# print the JSON string representation of the object
print(UserManagementUserGroupMember.to_json())

# convert the object into a dict
user_management_user_group_member_dict = user_management_user_group_member_instance.to_dict()
# create an instance of UserManagementUserGroupMember from a dict
user_management_user_group_member_from_dict = UserManagementUserGroupMember.from_dict(user_management_user_group_member_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


