# SlidesExportRequest

Export request object describing the export properties and metadata for slides exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** | File name to be used for retrieving the pdf document. | 
**format** | **str** | Requested resulting file type. | 
**dashboard_id** | **str** | Dashboard identifier | [optional] 
**metadata** | [**JsonNode**](JsonNode.md) |  | [optional] 
**template_id** | **str, none_type** | Export template identifier. | [optional] 
**visualization_ids** | **[str]** | List of visualization ids to be exported. Note that only one visualization is currently supported. | [optional] 
**widget_ids** | **[str]** | List of widget identifiers to be exported. Note that only one widget is currently supported. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


