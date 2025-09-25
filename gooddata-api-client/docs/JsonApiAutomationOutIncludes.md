# JsonApiAutomationOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationResultOutAttributes**](JsonApiAutomationResultOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAutomationResultOutRelationships**](JsonApiAutomationResultOutRelationships.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_out_includes import JsonApiAutomationOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationOutIncludes from a JSON string
json_api_automation_out_includes_instance = JsonApiAutomationOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationOutIncludes.to_json())

# convert the object into a dict
json_api_automation_out_includes_dict = json_api_automation_out_includes_instance.to_dict()
# create an instance of JsonApiAutomationOutIncludes from a dict
json_api_automation_out_includes_from_dict = JsonApiAutomationOutIncludes.from_dict(json_api_automation_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


