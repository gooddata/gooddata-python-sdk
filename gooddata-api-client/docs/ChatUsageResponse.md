# ChatUsageResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interaction_count** | **int** | Number of interactions in the time window | 
**interaction_limit** | **int** | Maximum number of interactions in the time window any user can do in the workspace | 
**time_window_hours** | **int** | Time window in hours | 

## Example

```python
from gooddata_api_client.models.chat_usage_response import ChatUsageResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ChatUsageResponse from a JSON string
chat_usage_response_instance = ChatUsageResponse.from_json(json)
# print the JSON string representation of the object
print(ChatUsageResponse.to_json())

# convert the object into a dict
chat_usage_response_dict = chat_usage_response_instance.to_dict()
# create an instance of ChatUsageResponse from a dict
chat_usage_response_from_dict = ChatUsageResponse.from_dict(chat_usage_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


