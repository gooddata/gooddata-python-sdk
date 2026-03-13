# AnalyzeCsvRequestItemConfig

CSV analysis request config.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**delimiters** | **[str]** | Possible column delimiters. | [optional] 
**header_detect_max_rows** | **int** | Maximum number of rows to work with during header detection. | [optional] 
**header_row_count** | **int** | Number of rows to consider as header, if null, header will be detected. | [optional] 
**result_rows** | **int** | Number of rows to return in the flight that represents analysis result. If 0, no rows are returned, if less than 0, all rows that were in the sample are returned. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


