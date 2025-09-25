# ManageDashboardPermissionsRequestInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | **List[str]** |  | 
**assignee_identifier** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**assignee_rule** | [**AssigneeRule**](AssigneeRule.md) |  | 

## Example

```python
from gooddata_api_client.models.manage_dashboard_permissions_request_inner import ManageDashboardPermissionsRequestInner

# TODO update the JSON string below
json = "{}"
# create an instance of ManageDashboardPermissionsRequestInner from a JSON string
manage_dashboard_permissions_request_inner_instance = ManageDashboardPermissionsRequestInner.from_json(json)
# print the JSON string representation of the object
print(ManageDashboardPermissionsRequestInner.to_json())

# convert the object into a dict
manage_dashboard_permissions_request_inner_dict = manage_dashboard_permissions_request_inner_instance.to_dict()
# create an instance of ManageDashboardPermissionsRequestInner from a dict
manage_dashboard_permissions_request_inner_from_dict = ManageDashboardPermissionsRequestInner.from_dict(manage_dashboard_permissions_request_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


