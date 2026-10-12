# FlowOperationDescriptor

An operation that a transformation can run.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | What the operation does. | 
**inputs** | [**[FlowOperationInput]**](FlowOperationInput.md) | Inputs of the operation. The first one is the primary input, named data. | 
**name** | **str** | Name of the operation. A transformation gives it as its operation. | 
**output** | [**FlowOperationOutput**](FlowOperationOutput.md) |  | 
**parameters** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | JSON Schema of the parameters of the operation. | 
**pure** | **bool** | True when the result depends only on the inputs and the parameters. The result of an impure operation is never reused. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


