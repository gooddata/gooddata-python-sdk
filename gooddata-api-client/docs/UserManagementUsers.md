# UserManagementUsers


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**total_count** | **int** | The total number of users is based on applied filters. | 
**users** | [**List[UserManagementUsersItem]**](UserManagementUsersItem.md) |  | 

## Example

```python
from gooddata_api_client.models.user_management_users import UserManagementUsers

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementUsers from a JSON string
user_management_users_instance = UserManagementUsers.from_json(json)
# print the JSON string representation of the object
print(UserManagementUsers.to_json())

# convert the object into a dict
user_management_users_dict = user_management_users_instance.to_dict()
# create an instance of UserManagementUsers from a dict
user_management_users_from_dict = UserManagementUsers.from_dict(user_management_users_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


