# JsonApiAutomationIn

JSON:API representation of automation entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAutomationInAttributes**](JsonApiAutomationInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiAutomationInRelationships**](JsonApiAutomationInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_automation_in import JsonApiAutomationIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationIn from a JSON string
json_api_automation_in_instance = JsonApiAutomationIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationIn.to_json())

# convert the object into a dict
json_api_automation_in_dict = json_api_automation_in_instance.to_dict()
# create an instance of JsonApiAutomationIn from a dict
json_api_automation_in_from_dict = JsonApiAutomationIn.from_dict(json_api_automation_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


