# DeclarativeUserGroup

A user-group and its properties

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | UserGroup identifier. | 
**name** | **str** | Name of UserGroup | [optional] 
**parents** | [**List[DeclarativeUserGroupIdentifier]**](DeclarativeUserGroupIdentifier.md) |  | [optional] 
**permissions** | [**List[DeclarativeUserGroupPermission]**](DeclarativeUserGroupPermission.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_user_group import DeclarativeUserGroup

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserGroup from a JSON string
declarative_user_group_instance = DeclarativeUserGroup.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserGroup.to_json())

# convert the object into a dict
declarative_user_group_dict = declarative_user_group_instance.to_dict()
# create an instance of DeclarativeUserGroup from a dict
declarative_user_group_from_dict = DeclarativeUserGroup.from_dict(declarative_user_group_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


