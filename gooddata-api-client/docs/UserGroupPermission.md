# UserGroupPermission

List of user groups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** | Name of the user group | [optional] 
**permissions** | [**List[GrantedPermission]**](GrantedPermission.md) | Permissions granted to the user group | [optional] 

## Example

```python
from gooddata_api_client.models.user_group_permission import UserGroupPermission

# TODO update the JSON string below
json = "{}"
# create an instance of UserGroupPermission from a JSON string
user_group_permission_instance = UserGroupPermission.from_json(json)
# print the JSON string representation of the object
print(UserGroupPermission.to_json())

# convert the object into a dict
user_group_permission_dict = user_group_permission_instance.to_dict()
# create an instance of UserGroupPermission from a dict
user_group_permission_from_dict = UserGroupPermission.from_dict(user_group_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


