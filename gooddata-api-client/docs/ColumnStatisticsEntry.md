# ColumnStatisticsEntry


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** |  | 
**data_size** | **int** | Total data size of the column in bytes. | [optional] 
**max** | **str** | Maximum value in the column (string-encoded). | [optional] 
**min** | **str** | Minimum value in the column (string-encoded). | [optional] 
**ndv** | **int** | NDV (Number of Distinct Values) — approximate cardinality of the column. | [optional] 
**null_count** | **int** | Number of NULL values in the column. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


