# CacheRetentionSchedule

A schedule determining when the cached results of a data source expire.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron** | **str** | Cron expression determining when the cached results expire. | 
**timezone** | **str, none_type** | Timezone the cron expression is evaluated in. Defaults to UTC when not set. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


