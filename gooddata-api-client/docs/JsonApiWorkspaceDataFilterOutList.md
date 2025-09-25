# JsonApiWorkspaceDataFilterOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiWorkspaceDataFilterOutWithLinks]**](JsonApiWorkspaceDataFilterOutWithLinks.md) |  | 
**included** | [**List[JsonApiWorkspaceDataFilterSettingOutWithLinks]**](JsonApiWorkspaceDataFilterSettingOutWithLinks.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_out_list import JsonApiWorkspaceDataFilterOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterOutList from a JSON string
json_api_workspace_data_filter_out_list_instance = JsonApiWorkspaceDataFilterOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterOutList.to_json())

# convert the object into a dict
json_api_workspace_data_filter_out_list_dict = json_api_workspace_data_filter_out_list_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterOutList from a dict
json_api_workspace_data_filter_out_list_from_dict = JsonApiWorkspaceDataFilterOutList.from_dict(json_api_workspace_data_filter_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


