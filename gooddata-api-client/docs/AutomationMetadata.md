# AutomationMetadata

Additional information for the automation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**visible_filters** | [**List[VisibleFilter]**](VisibleFilter.md) |  | [optional] 
**widget** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.automation_metadata import AutomationMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationMetadata from a JSON string
automation_metadata_instance = AutomationMetadata.from_json(json)
# print the JSON string representation of the object
print(AutomationMetadata.to_json())

# convert the object into a dict
automation_metadata_dict = automation_metadata_instance.to_dict()
# create an instance of AutomationMetadata from a dict
automation_metadata_from_dict = AutomationMetadata.from_dict(automation_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


