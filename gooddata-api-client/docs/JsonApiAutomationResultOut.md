# JsonApiAutomationResultOut

JSON:API representation of automationResult entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationResultOutAttributes**](JsonApiAutomationResultOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiAutomationResultOutRelationships**](JsonApiAutomationResultOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_automation_result_out import JsonApiAutomationResultOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationResultOut from a JSON string
json_api_automation_result_out_instance = JsonApiAutomationResultOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationResultOut.to_json())

# convert the object into a dict
json_api_automation_result_out_dict = json_api_automation_result_out_instance.to_dict()
# create an instance of JsonApiAutomationResultOut from a dict
json_api_automation_result_out_from_dict = JsonApiAutomationResultOut.from_dict(json_api_automation_result_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


