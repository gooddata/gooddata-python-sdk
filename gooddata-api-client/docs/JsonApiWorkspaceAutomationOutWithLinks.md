# JsonApiWorkspaceAutomationOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationOutAttributes**](JsonApiAutomationOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceAutomationOutRelationships**](JsonApiWorkspaceAutomationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_automation_out_with_links import JsonApiWorkspaceAutomationOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceAutomationOutWithLinks from a JSON string
json_api_workspace_automation_out_with_links_instance = JsonApiWorkspaceAutomationOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceAutomationOutWithLinks.to_json())

# convert the object into a dict
json_api_workspace_automation_out_with_links_dict = json_api_workspace_automation_out_with_links_instance.to_dict()
# create an instance of JsonApiWorkspaceAutomationOutWithLinks from a dict
json_api_workspace_automation_out_with_links_from_dict = JsonApiWorkspaceAutomationOutWithLinks.from_dict(json_api_workspace_automation_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


