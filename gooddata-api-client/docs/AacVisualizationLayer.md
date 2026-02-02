# AacVisualizationLayer

Visualization data layers (for geo charts).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the layer. | 
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**config** | [**JsonNode**](JsonNode.md) |  | [optional] 
**filters** | [**{str: (AacQueryFilter,)}**](AacQueryFilter.md) | Layer filters. | [optional] 
**metrics** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Layer metrics. | [optional] 
**segment_by** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Layer segment by. | [optional] 
**sorts** | [**[JsonNode]**](JsonNode.md) | Layer sorting definitions. | [optional] 
**title** | **str** | Layer title. | [optional] 
**type** | **str** | Layer type. | [optional] 
**view_by** | [**[AacQueryFieldsValue]**](AacQueryFieldsValue.md) | Layer view by. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


