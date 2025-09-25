# UserManagementDataSourcePermissionAssignment

Datasource permission assignments for users and userGroups

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Id of the datasource | 
**name** | **str** | Name of the datasource | [optional] [readonly] 
**permissions** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.user_management_data_source_permission_assignment import UserManagementDataSourcePermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of UserManagementDataSourcePermissionAssignment from a JSON string
user_management_data_source_permission_assignment_instance = UserManagementDataSourcePermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(UserManagementDataSourcePermissionAssignment.to_json())

# convert the object into a dict
user_management_data_source_permission_assignment_dict = user_management_data_source_permission_assignment_instance.to_dict()
# create an instance of UserManagementDataSourcePermissionAssignment from a dict
user_management_data_source_permission_assignment_from_dict = UserManagementDataSourcePermissionAssignment.from_dict(user_management_data_source_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


