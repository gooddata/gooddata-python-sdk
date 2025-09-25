# DeclarativeAnalyticalDashboardPermissionsInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Permission name. | 
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**assignee_rule** | [**AssigneeRule**](AssigneeRule.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_permissions_inner import DeclarativeAnalyticalDashboardPermissionsInner

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardPermissionsInner from a JSON string
declarative_analytical_dashboard_permissions_inner_instance = DeclarativeAnalyticalDashboardPermissionsInner.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardPermissionsInner.to_json())

# convert the object into a dict
declarative_analytical_dashboard_permissions_inner_dict = declarative_analytical_dashboard_permissions_inner_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardPermissionsInner from a dict
declarative_analytical_dashboard_permissions_inner_from_dict = DeclarativeAnalyticalDashboardPermissionsInner.from_dict(declarative_analytical_dashboard_permissions_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


