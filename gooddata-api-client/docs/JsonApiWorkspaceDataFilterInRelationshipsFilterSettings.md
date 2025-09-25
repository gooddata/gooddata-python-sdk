# JsonApiWorkspaceDataFilterInRelationshipsFilterSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiWorkspaceDataFilterSettingLinkage]**](JsonApiWorkspaceDataFilterSettingLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_in_relationships_filter_settings import JsonApiWorkspaceDataFilterInRelationshipsFilterSettings

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterInRelationshipsFilterSettings from a JSON string
json_api_workspace_data_filter_in_relationships_filter_settings_instance = JsonApiWorkspaceDataFilterInRelationshipsFilterSettings.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterInRelationshipsFilterSettings.to_json())

# convert the object into a dict
json_api_workspace_data_filter_in_relationships_filter_settings_dict = json_api_workspace_data_filter_in_relationships_filter_settings_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterInRelationshipsFilterSettings from a dict
json_api_workspace_data_filter_in_relationships_filter_settings_from_dict = JsonApiWorkspaceDataFilterInRelationshipsFilterSettings.from_dict(json_api_workspace_data_filter_in_relationships_filter_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


