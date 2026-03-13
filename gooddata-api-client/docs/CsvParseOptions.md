# CsvParseOptions

Options for parsing CSV files.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delimiter** | **str** | The character delimiting individual cells in the CSV data. | [optional] 
**double_quote** | **bool** | Whether two quotes in a quoted CSV value denote a single quote in the data. | [optional] 
**escape_char** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | The character used optionally for escaping special characters or false to disable escaping. | [optional] 
**ignore_empty_lines** | **bool** | Whether empty lines are ignored in CSV input. | [optional] 
**newlines_in_values** | **bool** | Whether newline characters are allowed in CSV values. | [optional] 
**quote_char** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | The character used optionally for quoting CSV values or false to disable quoting. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


