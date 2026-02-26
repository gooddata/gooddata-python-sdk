# gooddata_api_client.model.declarative_analytical_dashboard_permission_for_assignee_rule.DeclarativeAnalyticalDashboardPermissionForAssigneeRule

Analytical dashboard permission for a collection of assignees identified by a rule.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Analytical dashboard permission for a collection of assignees identified by a rule. | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[DeclarativeAnalyticalDashboardPermissionAssignment](DeclarativeAnalyticalDashboardPermissionAssignment.md) | [**DeclarativeAnalyticalDashboardPermissionAssignment**](DeclarativeAnalyticalDashboardPermissionAssignment.md) | [**DeclarativeAnalyticalDashboardPermissionAssignment**](DeclarativeAnalyticalDashboardPermissionAssignment.md) |  | 
[all_of_1](#all_of_1) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# all_of_1

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**assigneeRule** | [**AssigneeRule**](AssigneeRule.md) | [**AssigneeRule**](AssigneeRule.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

