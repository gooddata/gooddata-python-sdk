# ChangeAnalysisRequest

Request for change analysis computation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analyzed_period** | **str** | The analyzed time period (e.g., &#39;2025-02&#39;) | 
**date_attribute** | [**AttributeItem**](AttributeItem.md) |  | 
**measure** | [**MeasureItem**](MeasureItem.md) |  | 
**reference_period** | **str** | The reference time period (e.g., &#39;2025-01&#39;) | 
**attributes** | [**[AttributeItem]**](AttributeItem.md) | Attributes to analyze for significant changes. If empty, valid attributes will be automatically discovered. | [optional] 
**aux_measures** | [**[MeasureItem]**](MeasureItem.md) | Auxiliary measures | [optional] 
**filters** | [**[ChangeAnalysisParamsFiltersInner]**](ChangeAnalysisParamsFiltersInner.md) | Optional filters to apply. | [optional] 
**use_smart_attribute_selection** | **bool** | Whether to use smart attribute selection (LLM-based) instead of discovering all valid attributes. If true, GenAI will intelligently select the most relevant attributes for change analysis. If false or not set, all valid attributes will be discovered using Calcique. Smart attribute selection applies only when no attributes are provided. | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


