# JsonApiKnowledgeRecommendationPatchAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard_title** | **str** | Human-readable title of the analytical dashboard (denormalized for display) | [optional] 
**analyzed_period** | **str** | Analyzed time period (e.g., &#39;2023-07&#39; or &#39;July 2023&#39;) | [optional] 
**analyzed_value** | **bool, date, datetime, dict, float, int, list, str, none_type** | Metric value in the analyzed period (the observed value that triggered the anomaly) | [optional] 
**are_relations_valid** | **bool** |  | [optional] 
**comparison_type** | **str** | Time period for comparison | [optional] 
**confidence** | **bool, date, datetime, dict, float, int, list, str, none_type** | Confidence score (0.0 to 1.0) | [optional] 
**description** | **str** | Description of the recommendation | [optional] 
**direction** | **str** | Direction of the metric change | [optional] 
**metric_title** | **str** | Human-readable title of the metric (denormalized for display) | [optional] 
**recommendations** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Structured recommendations data as JSON | [optional] 
**reference_period** | **str** | Reference time period for comparison (e.g., &#39;2023-06&#39; or &#39;Jun 2023&#39;) | [optional] 
**reference_value** | **bool, date, datetime, dict, float, int, list, str, none_type** | Metric value in the reference period | [optional] 
**source_count** | **int** | Number of source documents used for generation | [optional] 
**tags** | **[str]** |  | [optional] 
**title** | **str** | Human-readable title for the recommendation, e.g. &#39;Revenue decreased vs last month&#39; | [optional] 
**widget_id** | **str** | ID of the widget where the anomaly was detected | [optional] 
**widget_name** | **str** | Name of the widget where the anomaly was detected | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


