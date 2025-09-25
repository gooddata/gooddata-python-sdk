# DeclarativeWorkspaceDataFilters

Declarative form of data filters.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**workspace_data_filters** | [**List[DeclarativeWorkspaceDataFilter]**](DeclarativeWorkspaceDataFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceDataFilters from a JSON string
declarative_workspace_data_filters_instance = DeclarativeWorkspaceDataFilters.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceDataFilters.to_json())

# convert the object into a dict
declarative_workspace_data_filters_dict = declarative_workspace_data_filters_instance.to_dict()
# create an instance of DeclarativeWorkspaceDataFilters from a dict
declarative_workspace_data_filters_from_dict = DeclarativeWorkspaceDataFilters.from_dict(declarative_workspace_data_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


