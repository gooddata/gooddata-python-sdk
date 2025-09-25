# JsonApiAutomationOut

JSON:API representation of automation entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationOutAttributes**](JsonApiAutomationOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAutomationOutRelationships**](JsonApiAutomationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_automation_out import JsonApiAutomationOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationOut from a JSON string
json_api_automation_out_instance = JsonApiAutomationOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationOut.to_json())

# convert the object into a dict
json_api_automation_out_dict = json_api_automation_out_instance.to_dict()
# create an instance of JsonApiAutomationOut from a dict
json_api_automation_out_from_dict = JsonApiAutomationOut.from_dict(json_api_automation_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


