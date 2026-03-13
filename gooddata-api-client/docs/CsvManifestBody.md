# CsvManifestBody

Body of the CSV manifest.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_date_formats** | **{str: (str,)}** | Map of column names to date formats to use when parsing them as dates. | [optional] 
**convert** | [**CsvConvertOptions**](CsvConvertOptions.md) |  | [optional] 
**parse** | [**CsvParseOptions**](CsvParseOptions.md) |  | [optional] 
**read** | [**CsvReadOptions**](CsvReadOptions.md) |  | [optional] 
**read_method** | **str** | Method used to read the CSV file. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


