# ElementsRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**label** | **str** | Requested label. | 
**cache_id** | **str** | If specified, the element data will be taken from the result with the same cacheId if it is available. | [optional] 
**complement_filter** | **bool** | Inverse filters: * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items not matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; | [optional]  if omitted the server will use the default value of False
**data_sampling_percentage** | **float** | Specifies percentage of source table data scanned during the computation. This field is deprecated and is no longer used during the elements computation. | [optional]  if omitted the server will use the default value of 100.0
**depends_on** | [**[ElementsRequestDependsOnInner]**](ElementsRequestDependsOnInner.md) | Return only items that are not filtered-out by the parent filters. | [optional] 
**exact_filter** | **[str, none_type]** | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title exactly matches one of &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60;. | [optional] 
**exclude_primary_label** | **bool** | Excludes items from the result that differ only by primary label * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items with distinct primary label * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items with distinct requested label | [optional]  if omitted the server will use the default value of False
**filter_by** | [**FilterBy**](FilterBy.md) |  | [optional] 
**pattern_filter** | **str** | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title case insensitively contains &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60; as substring. | [optional] 
**sort_order** | **str** | Sort order of returned items. Items are sorted by &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title. If no sort order is specified then attribute&#39;s &#x60;&#x60;&#x60;sortDirection&#x60;&#x60;&#x60; is used, which is ASC by default | [optional] 
**validate_by** | [**[ValidateByItem]**](ValidateByItem.md) | Return only items that are computable on metric. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


