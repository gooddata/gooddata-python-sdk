# gooddata_api_client.model.test_query_duration.TestQueryDuration

A structure containing duration of the test queries run on a data source. It is omitted if an error happens.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A structure containing duration of the test queries run on a data source. It is omitted if an error happens. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**simpleSelect** | decimal.Decimal, int,  | decimal.Decimal,  | Field containing duration of a test select query on a data source. In milliseconds. | value must be a 32 bit integer
**createCacheTable** | decimal.Decimal, int,  | decimal.Decimal,  | Field containing duration of a test &#x27;create table as select&#x27; query on a datasource. In milliseconds. The field is omitted if a data source doesn&#x27;t support caching. | [optional] value must be a 32 bit integer
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

