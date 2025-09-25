# DeclarativeAnalyticalDashboardPermissionAssignment

Analytical dashboard permission.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_permission_assignment import DeclarativeAnalyticalDashboardPermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardPermissionAssignment from a JSON string
declarative_analytical_dashboard_permission_assignment_instance = DeclarativeAnalyticalDashboardPermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardPermissionAssignment.to_json())

# convert the object into a dict
declarative_analytical_dashboard_permission_assignment_dict = declarative_analytical_dashboard_permission_assignment_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardPermissionAssignment from a dict
declarative_analytical_dashboard_permission_assignment_from_dict = DeclarativeAnalyticalDashboardPermissionAssignment.from_dict(declarative_analytical_dashboard_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


