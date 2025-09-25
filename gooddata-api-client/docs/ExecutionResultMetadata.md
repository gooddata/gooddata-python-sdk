# ExecutionResultMetadata

Additional metadata for the particular execution result.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_messages** | [**List[ExecutionResultDataSourceMessage]**](ExecutionResultDataSourceMessage.md) | Additional information sent by the underlying data source. | 

## Example

```python
from gooddata_api_client.models.execution_result_metadata import ExecutionResultMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResultMetadata from a JSON string
execution_result_metadata_instance = ExecutionResultMetadata.from_json(json)
# print the JSON string representation of the object
print(ExecutionResultMetadata.to_json())

# convert the object into a dict
execution_result_metadata_dict = execution_result_metadata_instance.to_dict()
# create an instance of ExecutionResultMetadata from a dict
execution_result_metadata_from_dict = ExecutionResultMetadata.from_dict(execution_result_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


