# PermissionsForAssigneeRule

Desired levels of permissions for a collection of assignees identified by a rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** |  | 
**assignee_rule** | [**AssigneeRule**](AssigneeRule.md) |  | 

## Example

```python
from gooddata_api_client.models.permissions_for_assignee_rule import PermissionsForAssigneeRule

# TODO update the JSON string below
json = "{}"
# create an instance of PermissionsForAssigneeRule from a JSON string
permissions_for_assignee_rule_instance = PermissionsForAssigneeRule.from_json(json)
# print the JSON string representation of the object
print(PermissionsForAssigneeRule.to_json())

# convert the object into a dict
permissions_for_assignee_rule_dict = permissions_for_assignee_rule_instance.to_dict()
# create an instance of PermissionsForAssigneeRule from a dict
permissions_for_assignee_rule_from_dict = PermissionsForAssigneeRule.from_dict(permissions_for_assignee_rule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


