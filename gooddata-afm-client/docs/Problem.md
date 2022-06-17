# Problem

Contains information about the error.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**status** | [**StatusType**](StatusType.md) |  | 
**trace_id** | **str** | Unique trace id used in open-tracing (semantics of transactions in distributed systems). Can be used to correlate client error with concrete request processing in the system. | 
**type** | **str** | An relative URI that identifies the problem type. When dereferenced, it should provide human-readable documentation for the problem type (e.g., using HTML). | 
**detail** | **str** | A human readable explanation specific to this occurrence of the problem. | [optional] 
**instance** | **str** | An relative URI that identifies the specific occurrence of the problem. It may yield further information if dereferenced. | [optional] 
**title** | **str** | A short, summary of the problem type. Written in english and readable for engineers (usually not suited for non technical stakeholders and not localized). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


