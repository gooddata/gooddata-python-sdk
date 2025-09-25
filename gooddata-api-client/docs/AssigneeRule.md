# AssigneeRule

Identifier of an assignee rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.assignee_rule import AssigneeRule

# TODO update the JSON string below
json = "{}"
# create an instance of AssigneeRule from a JSON string
assignee_rule_instance = AssigneeRule.from_json(json)
# print the JSON string representation of the object
print(AssigneeRule.to_json())

# convert the object into a dict
assignee_rule_dict = assignee_rule_instance.to_dict()
# create an instance of AssigneeRule from a dict
assignee_rule_from_dict = AssigneeRule.from_dict(assignee_rule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


