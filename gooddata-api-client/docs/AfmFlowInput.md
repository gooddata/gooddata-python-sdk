# AfmFlowInput

Computes an AFM as /afm/execute does, and reads its rows as a table. It has a column for each attribute and each measure of the AFM, named by its local identifier, the attributes first. Each attribute must use a label of its own.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution** | [**AFM**](AFM.md) |  | 
**type** | **str** | Type of the input. | defaults to "afm"
**settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


