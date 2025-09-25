# JsonApiAutomationInAttributesMetadata

Additional information for the automation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**visible_filters** | [**List[VisibleFilter]**](VisibleFilter.md) |  | [optional] 
**widget** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_attributes_metadata import JsonApiAutomationInAttributesMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInAttributesMetadata from a JSON string
json_api_automation_in_attributes_metadata_instance = JsonApiAutomationInAttributesMetadata.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInAttributesMetadata.to_json())

# convert the object into a dict
json_api_automation_in_attributes_metadata_dict = json_api_automation_in_attributes_metadata_instance.to_dict()
# create an instance of JsonApiAutomationInAttributesMetadata from a dict
json_api_automation_in_attributes_metadata_from_dict = JsonApiAutomationInAttributesMetadata.from_dict(json_api_automation_in_attributes_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


