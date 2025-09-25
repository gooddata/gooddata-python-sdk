# RawExportAutomationRequest

Export request object describing the export properties and overrides for raw exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_override** | [**RawCustomOverride**](RawCustomOverride.md) |  | [optional] 
**execution** | [**AFM**](AFM.md) |  | 
**execution_settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested resulting file type. | 
**metadata** | **object** | Free-form JSON object | [optional] 

## Example

```python
from gooddata_api_client.models.raw_export_automation_request import RawExportAutomationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RawExportAutomationRequest from a JSON string
raw_export_automation_request_instance = RawExportAutomationRequest.from_json(json)
# print the JSON string representation of the object
print(RawExportAutomationRequest.to_json())

# convert the object into a dict
raw_export_automation_request_dict = raw_export_automation_request_instance.to_dict()
# create an instance of RawExportAutomationRequest from a dict
raw_export_automation_request_from_dict = RawExportAutomationRequest.from_dict(raw_export_automation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


