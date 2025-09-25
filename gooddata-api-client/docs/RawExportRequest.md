# RawExportRequest

Export request object describing the export properties and overrides for raw exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_override** | [**RawCustomOverride**](RawCustomOverride.md) |  | [optional] 
**execution** | [**AFM**](AFM.md) |  | 
**execution_settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested resulting file type. | 

## Example

```python
from gooddata_api_client.models.raw_export_request import RawExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of RawExportRequest from a JSON string
raw_export_request_instance = RawExportRequest.from_json(json)
# print the JSON string representation of the object
print(RawExportRequest.to_json())

# convert the object into a dict
raw_export_request_dict = raw_export_request_instance.to_dict()
# create an instance of RawExportRequest from a dict
raw_export_request_from_dict = RawExportRequest.from_dict(raw_export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


