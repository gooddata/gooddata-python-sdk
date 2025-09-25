# JsonApiWorkspaceDataFilterOut

JSON:API representation of workspaceDataFilter entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiWorkspaceDataFilterInAttributes**](JsonApiWorkspaceDataFilterInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiWorkspaceDataFilterInRelationships**](JsonApiWorkspaceDataFilterInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_data_filter_out import JsonApiWorkspaceDataFilterOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceDataFilterOut from a JSON string
json_api_workspace_data_filter_out_instance = JsonApiWorkspaceDataFilterOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceDataFilterOut.to_json())

# convert the object into a dict
json_api_workspace_data_filter_out_dict = json_api_workspace_data_filter_out_instance.to_dict()
# create an instance of JsonApiWorkspaceDataFilterOut from a dict
json_api_workspace_data_filter_out_from_dict = JsonApiWorkspaceDataFilterOut.from_dict(json_api_workspace_data_filter_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


