# AiUsageMetadataItem

AI usage metadata returned after the interaction (e.g. current query count vs. entitlement limit).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**counter_type** | **str** | Type of usage counter, e.g. AI_QUERIES. | 
**current_value** | **int** | Current usage value after this request. | 
**limit** | **int** | Entitlement limit. 0 means unlimited. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


