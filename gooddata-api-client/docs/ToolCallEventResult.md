# ToolCallEventResult

Tool call events emitted during the agentic loop (only present when GEN_AI_YIELD_TOOL_CALL_EVENTS is enabled).

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function_arguments** | **str** | JSON-encoded arguments passed to the tool function. | 
**function_name** | **str** | Name of the tool function that was called. | 
**result** | **str** | Result returned by the tool function. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


