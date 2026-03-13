# CsvConvertOptions

Options for converting CSV files when reading.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_dict_encode** | **bool** | Whether to try to automatically dict-encode string / binary data. | [optional] 
**auto_dict_max_cardinality** | **int** | The maximum dictionary cardinality for autoDictEncode. | [optional] 
**check_utf8** | **bool** | Whether to check UTF8 validity of string columns. | [optional] 
**column_types** | [**[CsvConvertOptionsColumnType]**](CsvConvertOptionsColumnType.md) | Information about the column types in the table. | [optional] 
**decimal_point** | **str** | The character used as decimal point in floating-point and decimal data. | [optional] 
**false_values** | **[str]** | Sequence of strings that denote false Booleans in the data. | [optional] 
**include_columns** | **[str]** | The names of columns to include in the Table. If empty, the Table will include all columns from the CSV file. If not empty, only these columns will be included, in this order. | [optional] 
**include_missing_columns** | **bool** | If false, columns in includeColumns but not in the CSV file will error out. | [optional] 
**null_values** | **[str]** | Sequence of strings that denote nulls in the data. | [optional] 
**quoted_strings_can_be_null** | **bool** | Whether quoted values can be null. | [optional] 
**strings_can_be_null** | **bool** | Whether string / binary columns can have null values. | [optional] 
**timestamp_parsers** | **[str]** | Sequence of strptime()-compatible format strings, tried in order when attempting to infer or convert timestamp values. | [optional] 
**true_values** | **[str]** | Sequence of strings that denote true Booleans in the data. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


