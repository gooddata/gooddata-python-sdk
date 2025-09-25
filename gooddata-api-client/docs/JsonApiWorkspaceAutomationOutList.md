# JsonApiWorkspaceAutomationOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiWorkspaceAutomationOutWithLinks]**](JsonApiWorkspaceAutomationOutWithLinks.md) |  | 
**included** | [**List[JsonApiWorkspaceAutomationOutIncludes]**](JsonApiWorkspaceAutomationOutIncludes.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_automation_out_list import JsonApiWorkspaceAutomationOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceAutomationOutList from a JSON string
json_api_workspace_automation_out_list_instance = JsonApiWorkspaceAutomationOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceAutomationOutList.to_json())

# convert the object into a dict
json_api_workspace_automation_out_list_dict = json_api_workspace_automation_out_list_instance.to_dict()
# create an instance of JsonApiWorkspaceAutomationOutList from a dict
json_api_workspace_automation_out_list_from_dict = JsonApiWorkspaceAutomationOutList.from_dict(json_api_workspace_automation_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


