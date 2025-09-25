# JsonApiAutomationOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationOutAttributes**](JsonApiAutomationOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAutomationOutRelationships**](JsonApiAutomationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_out_with_links import JsonApiAutomationOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationOutWithLinks from a JSON string
json_api_automation_out_with_links_instance = JsonApiAutomationOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationOutWithLinks.to_json())

# convert the object into a dict
json_api_automation_out_with_links_dict = json_api_automation_out_with_links_instance.to_dict()
# create an instance of JsonApiAutomationOutWithLinks from a dict
json_api_automation_out_with_links_from_dict = JsonApiAutomationOutWithLinks.from_dict(json_api_automation_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


