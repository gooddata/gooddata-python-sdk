# JsonApiExportDefinitionInAttributesRequestPayload

JSON content to be used as export request payload for /export/tabular and /export/visual endpoints. 

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**metadata** | [**JsonNode**](JsonNode.md) |  | [optional] 
**timezone_id** | **str, none_type** | Time zone the export should be rendered in, as an IANA identifier (e.g. &#39;Asia/Kolkata&#39;) or a GMT offset (e.g. &#39;GMT+01:00&#39;). When omitted, the workspace time zone setting is used. | [optional] 
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**execution_settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**executions** | [**[TabularExportExecution]**](TabularExportExecution.md) | Pre-executed layers for multi-layer geo visualizations. When provided, this is the canonical source of the exported layers and takes precedence over the top-level executionResult and customOverride, which are ignored. Index 0 is the main layer; each layer carries its own executionResult and customOverride. | [optional] 
**related_dashboard_id** | **str** | Analytical dashboard identifier. Optional identifier, which informs the system that the export is related to a specific dashboard. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. | [optional] 
**visualization_object_custom_filters** | **[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. Those filters override the original filters defined in the visualization. | [optional] 
**visualization_object_custom_parameters** | [**[ParameterValue]**](ParameterValue.md) | Optional custom parameters to be applied when visualizationObject is given. Those parameters override the original parameters defined in the visualization. | [optional] 
**dashboard_id** | **str** | Dashboard identifier | [optional] 
**file_name** | **str** | Filename of downloaded file without extension. | [optional] 
**format** | **str** | Expected file format. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


