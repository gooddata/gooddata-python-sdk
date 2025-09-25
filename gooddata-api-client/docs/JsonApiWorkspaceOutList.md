# JsonApiWorkspaceOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiWorkspaceOutWithLinks]**](JsonApiWorkspaceOutWithLinks.md) |  | 
**included** | [**List[JsonApiWorkspaceOutWithLinks]**](JsonApiWorkspaceOutWithLinks.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_out_list import JsonApiWorkspaceOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOutList from a JSON string
json_api_workspace_out_list_instance = JsonApiWorkspaceOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOutList.to_json())

# convert the object into a dict
json_api_workspace_out_list_dict = json_api_workspace_out_list_instance.to_dict()
# create an instance of JsonApiWorkspaceOutList from a dict
json_api_workspace_out_list_from_dict = JsonApiWorkspaceOutList.from_dict(json_api_workspace_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


