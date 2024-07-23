# JsonApiExportDefinitionInAttributesRequestPayload

JSON content to be used as export request payload for /export/tabular and /export/visual endpoints. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Metadata definition in free-form JSON format. | [optional] 
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. (HTML/PDF only) | [optional] 
**visualization_object_custom_filters** | **[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. (HTML/PDF only) | [optional] 
**dashboard_id** | **str** | Dashboard identifier | [optional] 
**file_name** | **str** | Filename of downloaded file without extension. | [optional] 
**format** | **str** | Expected file format. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


