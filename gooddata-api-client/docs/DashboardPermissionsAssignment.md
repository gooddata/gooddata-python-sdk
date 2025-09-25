# DashboardPermissionsAssignment

Desired levels of permissions for an assignee.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.dashboard_permissions_assignment import DashboardPermissionsAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardPermissionsAssignment from a JSON string
dashboard_permissions_assignment_instance = DashboardPermissionsAssignment.from_json(json)
# print the JSON string representation of the object
print(DashboardPermissionsAssignment.to_json())

# convert the object into a dict
dashboard_permissions_assignment_dict = dashboard_permissions_assignment_instance.to_dict()
# create an instance of DashboardPermissionsAssignment from a dict
dashboard_permissions_assignment_from_dict = DashboardPermissionsAssignment.from_dict(dashboard_permissions_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


