# CacheRetention

Determines when the cached results coming from a particular data source expire. The shape is selected by the `type` property.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The cache retention type. | [optional]  if omitted the server will use the default value of "SCHEDULE"
**validity_period** | **str** | How long the cached results stay valid after they were computed. | [optional] 
**schedule** | [**CacheRetentionSchedule**](CacheRetentionSchedule.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


