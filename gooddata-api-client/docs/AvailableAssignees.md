# AvailableAssignees


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_groups** | [**List[UserGroupAssignee]**](UserGroupAssignee.md) | List of user groups | 
**users** | [**List[UserAssignee]**](UserAssignee.md) | List of users | 

## Example

```python
from gooddata_api_client.models.available_assignees import AvailableAssignees

# TODO update the JSON string below
json = "{}"
# create an instance of AvailableAssignees from a JSON string
available_assignees_instance = AvailableAssignees.from_json(json)
# print the JSON string representation of the object
print(AvailableAssignees.to_json())

# convert the object into a dict
available_assignees_dict = available_assignees_instance.to_dict()
# create an instance of AvailableAssignees from a dict
available_assignees_from_dict = AvailableAssignees.from_dict(available_assignees_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


