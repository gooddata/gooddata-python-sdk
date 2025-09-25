# ChatHistoryResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**interactions** | [**List[ChatHistoryInteraction]**](ChatHistoryInteraction.md) | List of chat history interactions. | 
**thread_id** | **str** | The conversation thread ID. | 

## Example

```python
from gooddata_api_client.models.chat_history_result import ChatHistoryResult

# TODO update the JSON string below
json = "{}"
# create an instance of ChatHistoryResult from a JSON string
chat_history_result_instance = ChatHistoryResult.from_json(json)
# print the JSON string representation of the object
print(ChatHistoryResult.to_json())

# convert the object into a dict
chat_history_result_dict = chat_history_result_instance.to_dict()
# create an instance of ChatHistoryResult from a dict
chat_history_result_from_dict = ChatHistoryResult.from_dict(chat_history_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


