# TestQueryDuration

A structure containing duration of the test queries run on a data source. It is omitted if an error happens.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**create_cache_table** | **int** | Field containing duration of a test &#39;create table as select&#39; query on a datasource. In milliseconds. The field is omitted if a data source doesn&#39;t support caching. | [optional] 
**simple_select** | **int** | Field containing duration of a test select query on a data source. In milliseconds. | 

## Example

```python
from gooddata_api_client.models.test_query_duration import TestQueryDuration

# TODO update the JSON string below
json = "{}"
# create an instance of TestQueryDuration from a JSON string
test_query_duration_instance = TestQueryDuration.from_json(json)
# print the JSON string representation of the object
print(TestQueryDuration.to_json())

# convert the object into a dict
test_query_duration_dict = test_query_duration_instance.to_dict()
# create an instance of TestQueryDuration from a dict
test_query_duration_from_dict = TestQueryDuration.from_dict(test_query_duration_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


