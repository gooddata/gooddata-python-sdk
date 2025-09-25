# JsonApiAutomationInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alert** | [**JsonApiAutomationInAttributesAlert**](JsonApiAutomationInAttributesAlert.md) |  | [optional] 
**are_relations_valid** | **bool** |  | [optional] 
**dashboard_tabular_exports** | [**List[JsonApiAutomationInAttributesDashboardTabularExportsInner]**](JsonApiAutomationInAttributesDashboardTabularExportsInner.md) |  | [optional] 
**description** | **str** |  | [optional] 
**details** | **object** | Additional details to be included in the automated message. | [optional] 
**evaluation_mode** | **str** | Specify automation evaluation mode. | [optional] 
**external_recipients** | [**List[JsonApiAutomationInAttributesExternalRecipientsInner]**](JsonApiAutomationInAttributesExternalRecipientsInner.md) | External recipients of the automation action results. | [optional] 
**image_exports** | [**List[JsonApiAutomationInAttributesImageExportsInner]**](JsonApiAutomationInAttributesImageExportsInner.md) |  | [optional] 
**metadata** | [**JsonApiAutomationInAttributesMetadata**](JsonApiAutomationInAttributesMetadata.md) |  | [optional] 
**raw_exports** | [**List[JsonApiAutomationInAttributesRawExportsInner]**](JsonApiAutomationInAttributesRawExportsInner.md) |  | [optional] 
**schedule** | [**JsonApiAutomationInAttributesSchedule**](JsonApiAutomationInAttributesSchedule.md) |  | [optional] 
**slides_exports** | [**List[JsonApiAutomationInAttributesSlidesExportsInner]**](JsonApiAutomationInAttributesSlidesExportsInner.md) |  | [optional] 
**state** | **str** | Current state of the automation. | [optional] 
**tabular_exports** | [**List[JsonApiAutomationInAttributesTabularExportsInner]**](JsonApiAutomationInAttributesTabularExportsInner.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**visual_exports** | [**List[JsonApiAutomationInAttributesVisualExportsInner]**](JsonApiAutomationInAttributesVisualExportsInner.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_attributes import JsonApiAutomationInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInAttributes from a JSON string
json_api_automation_in_attributes_instance = JsonApiAutomationInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInAttributes.to_json())

# convert the object into a dict
json_api_automation_in_attributes_dict = json_api_automation_in_attributes_instance.to_dict()
# create an instance of JsonApiAutomationInAttributes from a dict
json_api_automation_in_attributes_from_dict = JsonApiAutomationInAttributes.from_dict(json_api_automation_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


