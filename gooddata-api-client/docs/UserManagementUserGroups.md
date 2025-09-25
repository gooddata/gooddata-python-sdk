# UserManagementUserGroups


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | Total number of groups | 
**user_groups** | [**List[UserManagementUserGroupsItem]**](UserManagementUserGroupsItem.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_user_groups import UserManagementUserGroups

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUserGroups from a JSON string
user_management_user_groups_instance = UserManagementUserGroups.from_json(json)
# print the JSON string representation of the object
print(UserManagementUserGroups.to_json())

# convert the object into a dict
user_management_user_groups_dict = user_management_user_groups_instance.to_dict()
# create an instance of UserManagementUserGroups from a dict
user_management_user_groups_from_dict = UserManagementUserGroups.from_dict(user_management_user_groups_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


