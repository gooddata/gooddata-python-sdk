# JsonApiMetricInAttributesContent


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**maql** | **str** |  | 
**format** | **str, none_type** | Excel-like format string with optional dynamic tokens. Filter value tokens: [$FILTER:&lt;label_id&gt;] for raw filter value passthrough. Currency tokens: [$CURRENCY:&lt;label_id&gt;] for currency symbol, with optional forms :symbol, :narrow, :code, :name. Locale abbreviations: [$K], [$M], [$B], [$T] for locale-specific scale abbreviations. Tokens are resolved at execution time based on AFM filters and user&#39;s format locale. Single-value filters only; multi-value filters use fallback values. | [optional] 
**metric_type** | **str** | Categorizes metric semantics (e.g., currency). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


