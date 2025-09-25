# DeclarativeUserGroupIdentifier

A user group identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the user group. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_user_group_identifier import DeclarativeUserGroupIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserGroupIdentifier from a JSON string
declarative_user_group_identifier_instance = DeclarativeUserGroupIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserGroupIdentifier.to_json())

# convert the object into a dict
declarative_user_group_identifier_dict = declarative_user_group_identifier_instance.to_dict()
# create an instance of DeclarativeUserGroupIdentifier from a dict
declarative_user_group_identifier_from_dict = DeclarativeUserGroupIdentifier.from_dict(declarative_user_group_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


