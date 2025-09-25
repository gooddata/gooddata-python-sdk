# AfmExecution


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution** | [**AFM**](AFM.md) |  | 
**result_spec** | [**ResultSpec**](ResultSpec.md) |  | 
**settings** | [**ExecutionSettings**](ExecutionSettings.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.afm_execution import AfmExecution

# TODO update the JSON string below
json = "{}"
# create an instance of AfmExecution from a JSON string
afm_execution_instance = AfmExecution.from_json(json)
# print the JSON string representation of the object
print(AfmExecution.to_json())

# convert the object into a dict
afm_execution_dict = afm_execution_instance.to_dict()
# create an instance of AfmExecution from a dict
afm_execution_from_dict = AfmExecution.from_dict(afm_execution_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


