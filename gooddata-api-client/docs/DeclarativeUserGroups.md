# DeclarativeUserGroups

Declarative form of userGroups and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_groups** | [**List[DeclarativeUserGroup]**](DeclarativeUserGroup.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_user_groups import DeclarativeUserGroups

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserGroups from a JSON string
declarative_user_groups_instance = DeclarativeUserGroups.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserGroups.to_json())

# convert the object into a dict
declarative_user_groups_dict = declarative_user_groups_instance.to_dict()
# create an instance of DeclarativeUserGroups from a dict
declarative_user_groups_from_dict = DeclarativeUserGroups.from_dict(declarative_user_groups_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


