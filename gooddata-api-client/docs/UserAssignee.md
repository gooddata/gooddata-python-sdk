# UserAssignee

List of users

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | User email address | [optional] 
**id** | **str** |  | 
**name** | **str** | User name | [optional] 

## Example

```python
from gooddata_api_client.models.user_assignee import UserAssignee

# TODO update the JSON string below
json = "{}"
# create an instance of UserAssignee from a JSON string
user_assignee_instance = UserAssignee.from_json(json)
# print the JSON string representation of the object
print(UserAssignee.to_json())

# convert the object into a dict
user_assignee_dict = user_assignee_instance.to_dict()
# create an instance of UserAssignee from a dict
user_assignee_from_dict = UserAssignee.from_dict(user_assignee_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


