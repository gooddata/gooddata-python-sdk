# DeclarativeUsersUserGroups

Declarative form of both users and user groups and theirs properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_groups** | [**List[DeclarativeUserGroup]**](DeclarativeUserGroup.md) |  | 
**users** | [**List[DeclarativeUser]**](DeclarativeUser.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_users_user_groups import DeclarativeUsersUserGroups

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUsersUserGroups from a JSON string
declarative_users_user_groups_instance = DeclarativeUsersUserGroups.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUsersUserGroups.to_json())

# convert the object into a dict
declarative_users_user_groups_dict = declarative_users_user_groups_instance.to_dict()
# create an instance of DeclarativeUsersUserGroups from a dict
declarative_users_user_groups_from_dict = DeclarativeUsersUserGroups.from_dict(declarative_users_user_groups_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


