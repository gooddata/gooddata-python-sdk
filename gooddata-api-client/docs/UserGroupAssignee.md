# UserGroupAssignee

List of user groups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**name** | **str** | User group name | [optional] 

## Example

```python
from gooddata_api_client.models.user_group_assignee import UserGroupAssignee

# TODO update the JSON string below
json = "{}"
# create an instance of UserGroupAssignee from a JSON string
user_group_assignee_instance = UserGroupAssignee.from_json(json)
# print the JSON string representation of the object
print(UserGroupAssignee.to_json())

# convert the object into a dict
user_group_assignee_dict = user_group_assignee_instance.to_dict()
# create an instance of UserGroupAssignee from a dict
user_group_assignee_from_dict = UserGroupAssignee.from_dict(user_group_assignee_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


