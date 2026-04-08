# CreatePipeTableRequest

Request to create a new pipe-backed OLAP table in the AI Lake

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**path_prefix** | **str** | Path prefix to the parquet files (e.g. &#39;my-dataset/year&#x3D;2024/&#39;). All parquet files must be at a uniform depth under the prefix — either all directly under the prefix, or all under a consistent Hive partition hierarchy (e.g. year&#x3D;2024/month&#x3D;01/). Mixed layouts (files at multiple depths) are not supported. | 
**source_storage_name** | **str** | Name of the pre-configured S3/MinIO ObjectStorage source | 
**table_name** | **str** | Name of the OLAP table to create. Must match ^[a-z][a-z0-9_]{0,62}$ | 
**column_overrides** | **{str: (str,)}** | Override inferred column types. Maps column names to SQL type strings (e.g. {\&quot;year\&quot;: \&quot;INT\&quot;, \&quot;event_date\&quot;: \&quot;DATE\&quot;}). Applied after parquet schema inference. | [optional] 
**distribution_config** | [**DistributionConfig**](DistributionConfig.md) |  | [optional] 
**key_config** | [**KeyConfig**](KeyConfig.md) |  | [optional] 
**max_varchar_length** | **int** | Cap VARCHAR(N) to this length when N exceeds it. 0 &#x3D; no cap. | [optional] 
**partition_config** | [**PartitionConfig**](PartitionConfig.md) |  | [optional] 
**polling_interval_seconds** | **int** | How often (in seconds) the pipe polls for new files. 0 or null &#x3D; use server default. | [optional] 
**table_properties** | **{str: (str,)}** | CREATE TABLE PROPERTIES key-value pairs. Defaults to {\&quot;replication_num\&quot;: \&quot;1\&quot;}. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


