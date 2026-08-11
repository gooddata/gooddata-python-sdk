# ExecutionSettings

Various settings affecting the process of AFM execution or its result

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sampling_percentage** | **float** | Specifies the percentage of rows from fact datasets to use during computation. This feature is available only for workspaces that use a Vertica Data Source without table views. | [optional] 
**timestamp** | **datetime** | Specifies the timestamp of the execution from which relative filters are resolved. If not set, the current time is used. | [optional] 
**timezone** | **str** | Specifies the time zone used to resolve relative date filters and to convert time-zone-aware date/time values in the result. Expects an IANA time zone id (e.g. \&quot;Europe/Prague\&quot;) or a fixed GMT offset (e.g. \&quot;GMT+02:00\&quot;). If not set, the time zone from the workspace/user settings is used. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


