# FlowTransformation

One transformation of a flow: an operation that runs over its inputs.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation** | **str** | Name of the operation, as the operation catalog lists it. | 
**id** | **str, none_type** | Identifier of the transformation. Give it when a later transformation refers to it. The identifier does not change the result. | [optional] 
**input_refs** | **{str: (str,)}** | Inputs of the operation by name. Each one refers to a flow input or to an earlier transformation. The primary input is named data. When data is not given, it refers to the previous transformation, or to the only flow input for the first transformation. | [optional] 
**parameters** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Parameters of the operation. They must match the parameter schema of the operation. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


