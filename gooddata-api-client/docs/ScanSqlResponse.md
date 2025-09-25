# ScanSqlResponse

Result of scanSql. Consists of array of query columns including type. Sql query result data preview can be attached optionally

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[SqlColumn]**](SqlColumn.md) | Array of columns with types. | 
**data_preview** | **List[List[Optional[str]]]** | Array of rows where each row is another array of string values. | [optional] 

## Example

```python
from gooddata_api_client.models.scan_sql_response import ScanSqlResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ScanSqlResponse from a JSON string
scan_sql_response_instance = ScanSqlResponse.from_json(json)
# print the JSON string representation of the object
print(ScanSqlResponse.to_json())

# convert the object into a dict
scan_sql_response_dict = scan_sql_response_instance.to_dict()
# create an instance of ScanSqlResponse from a dict
scan_sql_response_from_dict = ScanSqlResponse.from_dict(scan_sql_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


