# DashboardPermissions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**rules** | [**List[RulePermission]**](RulePermission.md) | List of rules | 
**user_groups** | [**List[UserGroupPermission]**](UserGroupPermission.md) | List of user groups | 
**users** | [**List[UserPermission]**](UserPermission.md) | List of users | 

## Example

```python
from gooddata_api_client.models.dashboard_permissions import DashboardPermissions

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardPermissions from a JSON string
dashboard_permissions_instance = DashboardPermissions.from_json(json)
# print the JSON string representation of the object
print(DashboardPermissions.to_json())

# convert the object into a dict
dashboard_permissions_dict = dashboard_permissions_instance.to_dict()
# create an instance of DashboardPermissions from a dict
dashboard_permissions_from_dict = DashboardPermissions.from_dict(dashboard_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


