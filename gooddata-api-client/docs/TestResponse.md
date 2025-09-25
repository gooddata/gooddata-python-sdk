# TestResponse

Response from data source testing.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**error** | **str** | Field containing more details in case of a failure. Details are available to a privileged user only. | [optional] 
**query_duration_millis** | [**TestQueryDuration**](TestQueryDuration.md) |  | [optional] 
**successful** | **bool** | A flag indicating whether test passed or not. | 

## Example

```python
from gooddata_api_client.models.test_response import TestResponse

# TODO update the JSON string below
json = "{}"
# create an instance of TestResponse from a JSON string
test_response_instance = TestResponse.from_json(json)
# print the JSON string representation of the object
print(TestResponse.to_json())

# convert the object into a dict
test_response_dict = test_response_instance.to_dict()
# create an instance of TestResponse from a dict
test_response_from_dict = TestResponse.from_dict(test_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


