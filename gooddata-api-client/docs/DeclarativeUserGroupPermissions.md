# DeclarativeUserGroupPermissions

Definition of permissions associated with a user-group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**List[DeclarativeUserGroupPermission]**](DeclarativeUserGroupPermission.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_user_group_permissions import DeclarativeUserGroupPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserGroupPermissions from a JSON string
declarative_user_group_permissions_instance = DeclarativeUserGroupPermissions.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserGroupPermissions.to_json())

# convert the object into a dict
declarative_user_group_permissions_dict = declarative_user_group_permissions_instance.to_dict()
# create an instance of DeclarativeUserGroupPermissions from a dict
declarative_user_group_permissions_from_dict = DeclarativeUserGroupPermissions.from_dict(declarative_user_group_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


