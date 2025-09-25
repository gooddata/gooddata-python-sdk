# DeclarativeUsers

Declarative form of users and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**users** | [**List[DeclarativeUser]**](DeclarativeUser.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_users import DeclarativeUsers

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUsers from a JSON string
declarative_users_instance = DeclarativeUsers.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUsers.to_json())

# convert the object into a dict
declarative_users_dict = declarative_users_instance.to_dict()
# create an instance of DeclarativeUsers from a dict
declarative_users_from_dict = DeclarativeUsers.from_dict(declarative_users_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


