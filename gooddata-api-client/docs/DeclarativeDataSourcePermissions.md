# DeclarativeDataSourcePermissions

Data source permissions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**permissions** | [**List[DeclarativeDataSourcePermission]**](DeclarativeDataSourcePermission.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_data_source_permissions import DeclarativeDataSourcePermissions

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDataSourcePermissions from a JSON string
declarative_data_source_permissions_instance = DeclarativeDataSourcePermissions.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDataSourcePermissions.to_json())

# convert the object into a dict
declarative_data_source_permissions_dict = declarative_data_source_permissions_instance.to_dict()
# create an instance of DeclarativeDataSourcePermissions from a dict
declarative_data_source_permissions_from_dict = DeclarativeDataSourcePermissions.from_dict(declarative_data_source_permissions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


