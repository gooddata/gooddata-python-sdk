# AutomationRawExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**RawExportAutomationRequest**](RawExportAutomationRequest.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_raw_export import AutomationRawExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationRawExport from a JSON string
automation_raw_export_instance = AutomationRawExport.from_json(json)
# print the JSON string representation of the object
print(AutomationRawExport.to_json())

# convert the object into a dict
automation_raw_export_dict = automation_raw_export_instance.to_dict()
# create an instance of AutomationRawExport from a dict
automation_raw_export_from_dict = AutomationRawExport.from_dict(automation_raw_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


