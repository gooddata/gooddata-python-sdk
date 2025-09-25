# DeclarativeUserGroupPermission

Definition of a user-group permission assigned to a user/user-group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_user_group_permission import DeclarativeUserGroupPermission

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserGroupPermission from a JSON string
declarative_user_group_permission_instance = DeclarativeUserGroupPermission.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserGroupPermission.to_json())

# convert the object into a dict
declarative_user_group_permission_dict = declarative_user_group_permission_instance.to_dict()
# create an instance of DeclarativeUserGroupPermission from a dict
declarative_user_group_permission_from_dict = DeclarativeUserGroupPermission.from_dict(declarative_user_group_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


