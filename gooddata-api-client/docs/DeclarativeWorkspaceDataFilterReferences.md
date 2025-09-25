# DeclarativeWorkspaceDataFilterReferences


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter_column** | **str** | Filter column name | 
**filter_column_data_type** | **str** | Filter column data type | 
**filter_id** | [**DatasetWorkspaceDataFilterIdentifier**](DatasetWorkspaceDataFilterIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_data_filter_references import DeclarativeWorkspaceDataFilterReferences

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceDataFilterReferences from a JSON string
declarative_workspace_data_filter_references_instance = DeclarativeWorkspaceDataFilterReferences.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceDataFilterReferences.to_json())

# convert the object into a dict
declarative_workspace_data_filter_references_dict = declarative_workspace_data_filter_references_instance.to_dict()
# create an instance of DeclarativeWorkspaceDataFilterReferences from a dict
declarative_workspace_data_filter_references_from_dict = DeclarativeWorkspaceDataFilterReferences.from_dict(declarative_workspace_data_filter_references_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


