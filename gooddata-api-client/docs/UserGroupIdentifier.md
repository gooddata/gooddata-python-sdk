# UserGroupIdentifier

A list of groups where user is a member

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.user_group_identifier import UserGroupIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of UserGroupIdentifier from a JSON string
user_group_identifier_instance = UserGroupIdentifier.from_json(json)
# print the JSON string representation of the object
print(UserGroupIdentifier.to_json())

# convert the object into a dict
user_group_identifier_dict = user_group_identifier_instance.to_dict()
# create an instance of UserGroupIdentifier from a dict
user_group_identifier_from_dict = UserGroupIdentifier.from_dict(user_group_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


