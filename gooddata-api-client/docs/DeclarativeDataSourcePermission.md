# DeclarativeDataSourcePermission


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_data_source_permission import DeclarativeDataSourcePermission

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDataSourcePermission from a JSON string
declarative_data_source_permission_instance = DeclarativeDataSourcePermission.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDataSourcePermission.to_json())

# convert the object into a dict
declarative_data_source_permission_dict = declarative_data_source_permission_instance.to_dict()
# create an instance of DeclarativeDataSourcePermission from a dict
declarative_data_source_permission_from_dict = DeclarativeDataSourcePermission.from_dict(declarative_data_source_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


