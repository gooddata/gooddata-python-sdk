# VisualExportRequest

Export request object describing the export properties and metadata for dashboard PDF exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_id** | **str** | Dashboard identifier | 
**file_name** | **str** | File name to be used for retrieving the pdf document. | 
**metadata** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Metadata definition in free-form JSON format. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


