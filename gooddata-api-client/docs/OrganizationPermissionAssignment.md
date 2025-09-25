# OrganizationPermissionAssignment

Organization permission assignments

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee_identifier** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**permissions** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.organization_permission_assignment import OrganizationPermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationPermissionAssignment from a JSON string
organization_permission_assignment_instance = OrganizationPermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(OrganizationPermissionAssignment.to_json())

# convert the object into a dict
organization_permission_assignment_dict = organization_permission_assignment_instance.to_dict()
# create an instance of OrganizationPermissionAssignment from a dict
organization_permission_assignment_from_dict = OrganizationPermissionAssignment.from_dict(organization_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


