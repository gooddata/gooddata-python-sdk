# DeclarativeExportDefinitionRequestPayload


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**metadata** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Metadata definition in free-form JSON format. | [optional] 
**related_dashboard_id** | **str** | Analytical dashboard identifier. Optional identifier, which informs the system that the export is related to a specific dashboard. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. | [optional] 
**visualization_object_custom_filters** | **[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. | [optional] 
**file_name** | **str** | File name to be used for retrieving the pdf document. | [optional] 
**format** | **str** | Expected file format. | [optional] 
**dashboard_id** | **str** | Dashboard identifier | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


