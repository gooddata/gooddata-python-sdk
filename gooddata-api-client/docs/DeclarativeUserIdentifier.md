# DeclarativeUserIdentifier

A user identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | User identifier. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_user_identifier import DeclarativeUserIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserIdentifier from a JSON string
declarative_user_identifier_instance = DeclarativeUserIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserIdentifier.to_json())

# convert the object into a dict
declarative_user_identifier_dict = declarative_user_identifier_instance.to_dict()
# create an instance of DeclarativeUserIdentifier from a dict
declarative_user_identifier_from_dict = DeclarativeUserIdentifier.from_dict(declarative_user_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


