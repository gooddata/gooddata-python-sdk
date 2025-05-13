# ExecutionResultDataSourceMessage

A piece of extra information related to the results (e.g. debug information, warnings, etc.).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**correlation_id** | **str** | Id correlating different pieces of supplementary info together. | 
**source** | **str** | Information about what part of the system created this piece of supplementary info. | 
**type** | **str** | Type of the supplementary info instance. There are currently no well-known values for this, but there might be some in the future. | 
**data** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Data of this particular supplementary info item: a free-form JSON specific to the particular supplementary info item type. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


