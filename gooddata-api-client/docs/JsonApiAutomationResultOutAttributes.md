# JsonApiAutomationResultOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error_message** | **str** |  | [optional] 
**executed_at** | **datetime** | Timestamp of the last automation run. | 
**status** | **str** | Status of the last automation run. | 
**trace_id** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_result_out_attributes import JsonApiAutomationResultOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationResultOutAttributes from a JSON string
json_api_automation_result_out_attributes_instance = JsonApiAutomationResultOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationResultOutAttributes.to_json())

# convert the object into a dict
json_api_automation_result_out_attributes_dict = json_api_automation_result_out_attributes_instance.to_dict()
# create an instance of JsonApiAutomationResultOutAttributes from a dict
json_api_automation_result_out_attributes_from_dict = JsonApiAutomationResultOutAttributes.from_dict(json_api_automation_result_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


