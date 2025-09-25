# AssigneeIdentifier

Identifier of a user or user-group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.assignee_identifier import AssigneeIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of AssigneeIdentifier from a JSON string
assignee_identifier_instance = AssigneeIdentifier.from_json(json)
# print the JSON string representation of the object
print(AssigneeIdentifier.to_json())

# convert the object into a dict
assignee_identifier_dict = assignee_identifier_instance.to_dict()
# create an instance of AssigneeIdentifier from a dict
assignee_identifier_from_dict = AssigneeIdentifier.from_dict(assignee_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


