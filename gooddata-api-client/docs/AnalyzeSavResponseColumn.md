# AnalyzeSavResponseColumn

Describes a column of an SPSS file.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Name of the column as specified in the file. | 
**type** | **str** | Type of the column (e.g. string, float64, date32). | 
**label** | **str** | Label of the column, in a survey file usually the question text. Null if there is none. | [optional] 
**value_labels** | [**[AnalyzeSavResponseValueLabel]**](AnalyzeSavResponseValueLabel.md) | Labels of the column values in file order. Null if there are none. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


