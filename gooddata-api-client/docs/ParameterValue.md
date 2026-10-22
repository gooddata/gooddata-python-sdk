# ParameterValue

Parameter value override applied to the export. The (id, value) pair drives the execution; the title is FE-supplied for info-sheet display.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the workspace parameter (matches the parameter entity id). | 
**title** | **str** | Display title of the parameter as the client wants it rendered on the info sheet. | 
**value** | **str** | Value to use for this parameter when executing the export. | 
**value_title** | **str** | Human-readable form of &#x60;value&#x60; (e.g. a constrained string&#39;s allowedValues title). Never used to drive execution. Falls back to &#x60;value&#x60; when absent. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


