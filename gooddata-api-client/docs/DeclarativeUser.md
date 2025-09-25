# DeclarativeUser

A user and its properties

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth_id** | **str** | User identification in the authentication manager. | [optional] 
**email** | **str** | User email address | [optional] 
**firstname** | **str** | User first name | [optional] 
**id** | **str** | User identifier. | 
**lastname** | **str** | User last name | [optional] 
**permissions** | [**List[DeclarativeUserPermission]**](DeclarativeUserPermission.md) |  | [optional] 
**settings** | [**List[DeclarativeSetting]**](DeclarativeSetting.md) | A list of user settings. | [optional] 
**user_groups** | [**List[DeclarativeUserGroupIdentifier]**](DeclarativeUserGroupIdentifier.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_user import DeclarativeUser

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUser from a JSON string
declarative_user_instance = DeclarativeUser.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUser.to_json())

# convert the object into a dict
declarative_user_dict = declarative_user_instance.to_dict()
# create an instance of DeclarativeUser from a dict
declarative_user_from_dict = DeclarativeUser.from_dict(declarative_user_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


