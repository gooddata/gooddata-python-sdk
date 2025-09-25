# ScanSqlRequest

A request with SQL query to by analyzed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sql** | **str** | SQL query to be analyzed. | 

## Example

```python
from gooddata_api_client.models.scan_sql_request import ScanSqlRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ScanSqlRequest from a JSON string
scan_sql_request_instance = ScanSqlRequest.from_json(json)
# print the JSON string representation of the object
print(ScanSqlRequest.to_json())

# convert the object into a dict
scan_sql_request_dict = scan_sql_request_instance.to_dict()
# create an instance of ScanSqlRequest from a dict
scan_sql_request_from_dict = ScanSqlRequest.from_dict(scan_sql_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


