# JsonApiAutomationPatch

JSON:API representation of patching automation entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationInAttributes**](JsonApiAutomationInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiAutomationInRelationships**](JsonApiAutomationInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_automation_patch import JsonApiAutomationPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationPatch from a JSON string
json_api_automation_patch_instance = JsonApiAutomationPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationPatch.to_json())

# convert the object into a dict
json_api_automation_patch_dict = json_api_automation_patch_instance.to_dict()
# create an instance of JsonApiAutomationPatch from a dict
json_api_automation_patch_from_dict = JsonApiAutomationPatch.from_dict(json_api_automation_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


