# RelativeDateFilter

A date filter specifying a time interval that is relative to the current date. For example, last week, next month, and so on. Field dataset is representing qualifier of date dimension. The 'from' and 'to' properties mark the boundaries of the interval. If 'from' is omitted, all values earlier than 'to' are included. If 'to' is omitted, all values later than 'from' are included. It is not allowed to omit both.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**relative_date_filter** | [**RelativeDateFilterRelativeDateFilter**](RelativeDateFilterRelativeDateFilter.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


