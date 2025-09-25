# ExecutionSettings

Various settings affecting the process of AFM execution or its result

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sampling_percentage** | **float** | Specifies the percentage of rows from fact datasets to use during computation. This feature is available only for workspaces that use a Vertica Data Source without table views. | [optional] 
**timestamp** | **datetime** | Specifies the timestamp of the execution from which relative filters are resolved. If not set, the current time is used. | [optional] 

## Example

```python
from gooddata_api_client.models.execution_settings import ExecutionSettings

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionSettings from a JSON string
execution_settings_instance = ExecutionSettings.from_json(json)
# print the JSON string representation of the object
print(ExecutionSettings.to_json())

# convert the object into a dict
execution_settings_dict = execution_settings_instance.to_dict()
# create an instance of ExecutionSettings from a dict
execution_settings_from_dict = ExecutionSettings.from_dict(execution_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


