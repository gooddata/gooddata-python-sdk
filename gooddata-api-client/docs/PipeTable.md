# PipeTable

Full details of a pipe-backed OLAP table

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**[ColumnInfo]**](ColumnInfo.md) | Inferred column schema | 
**database_name** | **str** | Database name | 
**distribution_config** | [**PipeTableDistributionConfig**](PipeTableDistributionConfig.md) |  | 
**key_config** | [**PipeTableKeyConfig**](PipeTableKeyConfig.md) |  | 
**partition_columns** | **[str]** | Hive partition columns detected from the path structure | 
**path_prefix** | **str** | Path prefix to the parquet files | 
**pipe_table_id** | **str** | Internal UUID of the pipe table record | 
**polling_interval_seconds** | **int** | How often (in seconds) the pipe polls for new files. 0 &#x3D; server default. | 
**source_storage_name** | **str** | Source ObjectStorage name | 
**table_name** | **str** | OLAP table name | 
**table_properties** | **{str: (str,)}** | CREATE TABLE PROPERTIES key-value pairs | 
**partition_config** | [**PipeTablePartitionConfig**](PipeTablePartitionConfig.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


