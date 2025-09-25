# DeclarativeAnalyticalDashboardPermissionForAssignee

Analytical dashboard permission for an assignee.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Permission name. | 
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_permission_for_assignee import DeclarativeAnalyticalDashboardPermissionForAssignee

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardPermissionForAssignee from a JSON string
declarative_analytical_dashboard_permission_for_assignee_instance = DeclarativeAnalyticalDashboardPermissionForAssignee.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardPermissionForAssignee.to_json())

# convert the object into a dict
declarative_analytical_dashboard_permission_for_assignee_dict = declarative_analytical_dashboard_permission_for_assignee_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardPermissionForAssignee from a dict
declarative_analytical_dashboard_permission_for_assignee_from_dict = DeclarativeAnalyticalDashboardPermissionForAssignee.from_dict(declarative_analytical_dashboard_permission_for_assignee_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


