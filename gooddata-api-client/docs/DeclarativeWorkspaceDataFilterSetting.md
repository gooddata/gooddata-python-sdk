# DeclarativeWorkspaceDataFilterSetting

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Workspace Data Filters setting description. | [optional] 
**filter_values** | **List[str]** | Only those rows are returned, where columnName from filter matches those values. | 
**id** | **str** | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | **str** | Workspace Data Filters setting title. | 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_data_filter_setting import DeclarativeWorkspaceDataFilterSetting

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceDataFilterSetting from a JSON string
declarative_workspace_data_filter_setting_instance = DeclarativeWorkspaceDataFilterSetting.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceDataFilterSetting.to_json())

# convert the object into a dict
declarative_workspace_data_filter_setting_dict = declarative_workspace_data_filter_setting_instance.to_dict()
# create an instance of DeclarativeWorkspaceDataFilterSetting from a dict
declarative_workspace_data_filter_setting_from_dict = DeclarativeWorkspaceDataFilterSetting.from_dict(declarative_workspace_data_filter_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


