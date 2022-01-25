# ElementsRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** | Requested label. | 
**sort_order** | **str** | Sort order of returned items. Items are sorted by &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title. | [optional]  if omitted the server will use the default value of "ASC"
**complement_filter** | **bool** | Inverse filters: * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items not matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; | [optional]  if omitted the server will use the default value of False
**pattern_filter** | **str** | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title case insensitively contains &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60; as substring. | [optional] 
**exact_filter** | **[str]** | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title exactly matches one of &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60;. | [optional] 
**data_sampling_percentage** | **float** | Specifies percentage of source table data scanned during the computation. | [optional]  if omitted the server will use the default value of 100
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


