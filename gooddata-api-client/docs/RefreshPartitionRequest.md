# RefreshPartitionRequest

Request to refresh a specific Hive partition in a pipe-backed OLAP table

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**partition_spec** | **{str: (str,)}** | Partition column values identifying the partition to refresh. Keys must match the table&#39;s partition_columns exactly. Example: {\&quot;date\&quot;: \&quot;2026-01-01\&quot;} | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


