# DataSourcePermissionAssignment

Data source permission assignments

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee_identifier** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**permissions** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.data_source_permission_assignment import DataSourcePermissionAssignment

# TODO update the JSON string below
json = "{}"
# create an instance of DataSourcePermissionAssignment from a JSON string
data_source_permission_assignment_instance = DataSourcePermissionAssignment.from_json(json)
# print the JSON string representation of the object
print(DataSourcePermissionAssignment.to_json())

# convert the object into a dict
data_source_permission_assignment_dict = data_source_permission_assignment_instance.to_dict()
# create an instance of DataSourcePermissionAssignment from a dict
data_source_permission_assignment_from_dict = DataSourcePermissionAssignment.from_dict(data_source_permission_assignment_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


