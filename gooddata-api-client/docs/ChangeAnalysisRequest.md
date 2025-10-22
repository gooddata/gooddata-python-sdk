# ChangeAnalysisRequest

Request for change analysis computation

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analyzed_period** | **str** | The analyzed time period (e.g., &#39;2025-02&#39;) | 
**attribute_label_identifiers** | **[str]** | Label identifiers of attributes to analyze for significant changes. If empty, valid attributes will be automatically discovered. | 
**date_attribute_identifier** | **str** | The date attribute identifier to use for time period comparison | 
**filters** | [**[AttributeEqualityFilter]**](AttributeEqualityFilter.md) | Optional filters to apply. | 
**metric_identifier** | **str** | The metric identifier to analyze for changes | 
**reference_period** | **str** | The reference time period (e.g., &#39;2025-01&#39;) | 
**use_smart_attribute_selection** | **bool** | Whether to use smart attribute selection (LLM-based) instead of discovering all valid attributes. If true, GenAI will intelligently select the most relevant attributes for change analysis. If false or not set, all valid attributes will be discovered using Calcique. Smart attribute selection applies only when no attributes are provided. | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


