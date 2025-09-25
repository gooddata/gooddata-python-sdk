# DeclarativeWorkspaceDataFilterColumn


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | Data type of the column | 
**name** | **str** | Name of the column | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_data_filter_column import DeclarativeWorkspaceDataFilterColumn

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceDataFilterColumn from a JSON string
declarative_workspace_data_filter_column_instance = DeclarativeWorkspaceDataFilterColumn.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceDataFilterColumn.to_json())

# convert the object into a dict
declarative_workspace_data_filter_column_dict = declarative_workspace_data_filter_column_instance.to_dict()
# create an instance of DeclarativeWorkspaceDataFilterColumn from a dict
declarative_workspace_data_filter_column_from_dict = DeclarativeWorkspaceDataFilterColumn.from_dict(declarative_workspace_data_filter_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


