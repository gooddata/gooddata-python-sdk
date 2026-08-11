# AbsoluteGranularityDateFilter

An absolute date range filter defined at a specific granularity. The 'from'/'to' literals must match the format of the chosen granularity (e.g. '2020' for YEAR, '2012-05' for MONTH, '2012-3' for QUARTER, '1996-01' for WEEK, '2010-10-30' for DAY, or a plain ordinal like '6' for periodical granularities such as MONTH_OF_YEAR). At least one of 'from'/'to' must be provided; specifying only one yields an open-ended range.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**absolute_granularity_date_filter** | [**AbsoluteGranularityDateFilterAbsoluteGranularityDateFilter**](AbsoluteGranularityDateFilterAbsoluteGranularityDateFilter.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


