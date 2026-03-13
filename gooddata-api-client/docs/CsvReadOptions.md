# CsvReadOptions

Options for reading CSV files.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auto_generate_column_names** | **bool** | Whether to autogenerate column names if columnNames is empty. | [optional] 
**block_size** | **int** | How many bytes to process at a time from the input stream. | [optional] 
**column_names** | **[str]** | The column names of the target table. | [optional] 
**encoding** | **str** | The character encoding of the CSV data. | [optional] 
**skip_rows** | **int** | The number of rows to skip before the column names (if any) and the CSV data. | [optional] 
**skip_rows_after_names** | **int** | The number of rows to skip after the column names. | [optional] 
**use_threads** | **bool** | Whether to use multiple threads to accelerate reading. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


