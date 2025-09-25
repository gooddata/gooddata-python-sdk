# ExecutionResultDataSourceMessage

A piece of extra information related to the results (e.g. debug information, warnings, etc.).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**correlation_id** | **str** | Id correlating different pieces of supplementary info together. | 
**data** | **object** | Data of this particular supplementary info item: a free-form JSON specific to the particular supplementary info item type. | [optional] 
**source** | **str** | Information about what part of the system created this piece of supplementary info. | 
**type** | **str** | Type of the supplementary info instance. There are currently no well-known values for this, but there might be some in the future. | 

## Example

```python
from gooddata_api_client.models.execution_result_data_source_message import ExecutionResultDataSourceMessage

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResultDataSourceMessage from a JSON string
execution_result_data_source_message_instance = ExecutionResultDataSourceMessage.from_json(json)
# print the JSON string representation of the object
print(ExecutionResultDataSourceMessage.to_json())

# convert the object into a dict
execution_result_data_source_message_dict = execution_result_data_source_message_instance.to_dict()
# create an instance of ExecutionResultDataSourceMessage from a dict
execution_result_data_source_message_from_dict = ExecutionResultDataSourceMessage.from_dict(execution_result_data_source_message_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


