# TestQueryDuration

A structure containing duration of the test queries run on a data source. It is omitted if an error happens.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**simple_select** | **int** | Field containing duration of a test select query on a data source. In milliseconds. | 
**create_cache_table** | **int** | Field containing duration of a test &#39;create table as select&#39; query on a datasource. In milliseconds. The field is omitted if a data source doesn&#39;t support caching. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


