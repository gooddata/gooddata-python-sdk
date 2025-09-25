# DeclarativeUserPermissions

Definition of permissions associated with a user.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**List[DeclarativeUserPermission]**](DeclarativeUserPermission.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_user_permissions import DeclarativeUserPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserPermissions from a JSON string
declarative_user_permissions_instance = DeclarativeUserPermissions.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserPermissions.to_json())

# convert the object into a dict
declarative_user_permissions_dict = declarative_user_permissions_instance.to_dict()
# create an instance of DeclarativeUserPermissions from a dict
declarative_user_permissions_from_dict = DeclarativeUserPermissions.from_dict(declarative_user_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


