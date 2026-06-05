# ExecutionResultMetadata

Additional metadata for the particular execution result.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_messages** | [**[ExecutionResultDataSourceMessage]**](ExecutionResultDataSourceMessage.md) | Additional information sent by the underlying data source. | 
**limit_breaks** | [**[ExecutionResultLimitBreak]**](ExecutionResultLimitBreak.md) | Limits that were broken during result computation, causing the result to be partial. Absent when the result is complete. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


