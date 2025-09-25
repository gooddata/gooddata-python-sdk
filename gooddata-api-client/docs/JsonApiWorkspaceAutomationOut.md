# JsonApiWorkspaceAutomationOut

JSON:API representation of workspaceAutomation entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationOutAttributes**](JsonApiAutomationOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiWorkspaceAutomationOutRelationships**](JsonApiWorkspaceAutomationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_automation_out import JsonApiWorkspaceAutomationOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceAutomationOut from a JSON string
json_api_workspace_automation_out_instance = JsonApiWorkspaceAutomationOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceAutomationOut.to_json())

# convert the object into a dict
json_api_workspace_automation_out_dict = json_api_workspace_automation_out_instance.to_dict()
# create an instance of JsonApiWorkspaceAutomationOut from a dict
json_api_workspace_automation_out_from_dict = JsonApiWorkspaceAutomationOut.from_dict(json_api_workspace_automation_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


