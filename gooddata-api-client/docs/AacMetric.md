# AacMetric

AAC metric definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the metric. | 
**maql** | **str** | MAQL expression defining the metric. | 
**type** | **str** | Metric type discriminator. | 
**description** | **str** | Metric description. | [optional] 
**format** | **str** | Default format for metric values. | [optional] 
**is_hidden** | **bool** | Deprecated. Use showInAiResults instead. | [optional] 
**is_hidden_from_kda** | **bool** | Whether to hide from key driver analysis. | [optional] 
**show_in_ai_results** | **bool** | Whether to show in AI results. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


