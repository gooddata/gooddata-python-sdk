# AacVisualizationBubbleBuckets


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the visualization. | 
**query** | [**AacQuery**](AacQuery.md) |  | 
**type** | **str** |  | defaults to "bubble_chart"
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**attributes** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Attributes bucket (for scatter). | [optional] 
**columns** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Columns bucket (for tables). | [optional] 
**config** | [**JsonNode**](JsonNode.md) |  | [optional] 
**description** | **str** | Visualization description. | [optional] 
**_from** | [**JsonNode**](JsonNode.md) |  | [optional] 
**is_hidden** | **bool** | Deprecated. Use showInAiResults instead. | [optional] 
**layers** | [**[AacVisualizationLayer]**](AacVisualizationLayer.md) | Visualization data layers (for geo charts). | [optional] 
**metrics** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Metrics bucket. | [optional] 
**rows** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Rows bucket (for tables). | [optional] 
**segment_by** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Segment by attributes bucket. | [optional] 
**show_in_ai_results** | **bool** | Whether to show in AI results. | [optional] 
**size_by** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Size by metrics bucket. | [optional] 
**stack_by** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Stack by attributes bucket. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**to** | [**JsonNode**](JsonNode.md) |  | [optional] 
**trend_by** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | Trend by attributes bucket. | [optional] 
**view_by** | **[bool, date, datetime, dict, float, int, list, str, none_type]** | View by attributes bucket. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


