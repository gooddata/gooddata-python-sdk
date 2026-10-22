# AnalyzeSavResponse

Describes the results of an analysis of a single SPSS (.sav) file.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**[AnalyzeSavResponseColumn]**](AnalyzeSavResponseColumn.md) | List of column metadata. | 
**location** | **str** | Location of the analyzed file in the source data source. | 
**preview_data** | **[[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]]** | Preview of the first N rows of the file. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


