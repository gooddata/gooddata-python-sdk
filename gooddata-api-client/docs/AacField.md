# AacField

AAC field definition (attribute, fact, or aggregated_fact).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Field type. | 
**aggregated_as** | **str** | Aggregation method. | [optional] 
**assigned_to** | **str** | Source fact ID for aggregated fact. | [optional] 
**data_type** | **str** | Data type of the column. | [optional] 
**default_view** | **str** | Default view label ID. | [optional] 
**description** | **str** | Field description. | [optional] 
**is_hidden** | **bool** | Deprecated. Use showInAiResults instead. | [optional] 
**labels** | [**{str: (AacLabel,)}**](AacLabel.md) | Attribute labels. | [optional] 
**locale** | **str** | Locale for sorting. | [optional] 
**show_in_ai_results** | **bool** | Whether to show in AI results. | [optional] 
**sort_column** | **str** | Sort column name. | [optional] 
**sort_direction** | **str** | Sort direction. | [optional] 
**source_column** | **str** | Source column in the physical database. | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


