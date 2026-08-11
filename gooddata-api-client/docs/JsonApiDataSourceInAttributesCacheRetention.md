# JsonApiDataSourceInAttributesCacheRetention

Determines when the cached results coming from a particular data source expire. When unset, the cache is kept per cacheStrategy and invalidated only explicitly.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The cache retention type. | [optional]  if omitted the server will use the default value of "VALIDITY_PERIOD"
**schedule** | [**CacheRetentionSchedule**](CacheRetentionSchedule.md) |  | [optional] 
**validity_period** | **str** | How long the cached results stay valid after they were computed. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


