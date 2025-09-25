# ExecutionResultPaging

A paging information related to the data presented in the execution result. These paging information are multi-dimensional.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **List[int]** | A count of the returned results in every dimension. | 
**offset** | **List[int]** | The offset of the results returned in every dimension. | 
**total** | **List[int]** | A total count of the results in every dimension. | 

## Example

```python
from gooddata_api_client.models.execution_result_paging import ExecutionResultPaging

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResultPaging from a JSON string
execution_result_paging_instance = ExecutionResultPaging.from_json(json)
# print the JSON string representation of the object
print(ExecutionResultPaging.to_json())

# convert the object into a dict
execution_result_paging_dict = execution_result_paging_instance.to_dict()
# create an instance of ExecutionResultPaging from a dict
execution_result_paging_from_dict = ExecutionResultPaging.from_dict(execution_result_paging_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


