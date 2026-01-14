# AacVisualization

AAC visualization definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the visualization. | 
**query** | [**AacQuery**](AacQuery.md) |  | 
**type** | **str** | Visualization type. | 
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**attribute** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Attribute bucket (for repeater). | [optional] 
**color** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Color bucket. | [optional] 
**columns** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Columns bucket (for tables). | [optional] 
**config** | [**JsonNode**](JsonNode.md) |  | [optional] 
**description** | **str** | Visualization description. | [optional] 
**is_hidden** | **bool** | Deprecated. Use showInAiResults instead. | [optional] 
**location** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Location bucket (for geo charts). | [optional] 
**metrics** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Metrics bucket. | [optional] 
**primary_measures** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Primary measures bucket. | [optional] 
**rows** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Rows bucket (for tables). | [optional] 
**secondary_measures** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Secondary measures bucket. | [optional] 
**segment_by** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Segment by attributes bucket. | [optional] 
**show_in_ai_results** | **bool** | Whether to show in AI results. | [optional] 
**size** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Size bucket. | [optional] 
**stack** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Stack bucket. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**trend** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Trend bucket. | [optional] 
**view_by** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | View by attributes bucket. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


