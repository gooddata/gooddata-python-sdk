# DeclarativeAnalyticalDashboardPermissionForAssigneeRule

Analytical dashboard permission for a collection of assignees identified by a rule.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Permission name. | 
**assignee_rule** | [**AssigneeRule**](AssigneeRule.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_permission_for_assignee_rule import DeclarativeAnalyticalDashboardPermissionForAssigneeRule

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardPermissionForAssigneeRule from a JSON string
declarative_analytical_dashboard_permission_for_assignee_rule_instance = DeclarativeAnalyticalDashboardPermissionForAssigneeRule.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardPermissionForAssigneeRule.to_json())

# convert the object into a dict
declarative_analytical_dashboard_permission_for_assignee_rule_dict = declarative_analytical_dashboard_permission_for_assignee_rule_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardPermissionForAssigneeRule from a dict
declarative_analytical_dashboard_permission_for_assignee_rule_from_dict = DeclarativeAnalyticalDashboardPermissionForAssigneeRule.from_dict(declarative_analytical_dashboard_permission_for_assignee_rule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


