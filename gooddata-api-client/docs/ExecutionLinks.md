# ExecutionLinks

Links to the execution result.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution_result** | **str** | Link to the result data. | 

## Example

```python
from gooddata_api_client.models.execution_links import ExecutionLinks

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionLinks from a JSON string
execution_links_instance = ExecutionLinks.from_json(json)
# print the JSON string representation of the object
print(ExecutionLinks.to_json())

# convert the object into a dict
execution_links_dict = execution_links_instance.to_dict()
# create an instance of ExecutionLinks from a dict
execution_links_from_dict = ExecutionLinks.from_dict(execution_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


