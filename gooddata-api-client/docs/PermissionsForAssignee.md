# PermissionsForAssignee

Desired levels of permissions for an assignee identified by an identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** |  | 
**assignee_identifier** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.permissions_for_assignee import PermissionsForAssignee

# TODO update the JSON string below
json = "{}"
# create an instance of PermissionsForAssignee from a JSON string
permissions_for_assignee_instance = PermissionsForAssignee.from_json(json)
# print the JSON string representation of the object
print(PermissionsForAssignee.to_json())

# convert the object into a dict
permissions_for_assignee_dict = permissions_for_assignee_instance.to_dict()
# create an instance of PermissionsForAssignee from a dict
permissions_for_assignee_from_dict = PermissionsForAssignee.from_dict(permissions_for_assignee_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


