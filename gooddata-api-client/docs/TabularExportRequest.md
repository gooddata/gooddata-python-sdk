# TabularExportRequest

Export request object describing the export properties and overrides for tabular exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution_result** | **str** | Execution result identifier. | 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Expected file format. | defaults to "CSV"
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


