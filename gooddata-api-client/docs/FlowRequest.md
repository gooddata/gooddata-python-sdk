# FlowRequest

A flow: named inputs and the transformations that run over them.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**inputs** | [**{str: (FlowInput,)}**](FlowInput.md) | Inputs of the flow by name. A transformation refers to an input by its name. | 
**transformations** | [**[FlowTransformation]**](FlowTransformation.md) | Transformations in the order they run. The result of the last transformation is the result of the flow. Without transformations, the result is the only input. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


