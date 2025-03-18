# RawExportRequest

Export request object describing the export properties and overrides for raw exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution** | [**AFM**](AFM.md) |  | 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested resulting file type. | 
**custom_override** | [**RawCustomOverride**](RawCustomOverride.md) |  | [optional] 
**execution_settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


