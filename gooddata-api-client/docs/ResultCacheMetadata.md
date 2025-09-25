# ResultCacheMetadata

All execution result's metadata used for calculation including ExecutionResponse

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**afm** | [**AFM**](AFM.md) |  | 
**execution_response** | [**ExecutionResponse**](ExecutionResponse.md) |  | 
**result_size** | **int** |  | 
**result_spec** | [**ResultSpec**](ResultSpec.md) |  | 

## Example

```python
from gooddata_api_client.models.result_cache_metadata import ResultCacheMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of ResultCacheMetadata from a JSON string
result_cache_metadata_instance = ResultCacheMetadata.from_json(json)
# print the JSON string representation of the object
print(ResultCacheMetadata.to_json())

# convert the object into a dict
result_cache_metadata_dict = result_cache_metadata_instance.to_dict()
# create an instance of ResultCacheMetadata from a dict
result_cache_metadata_from_dict = ResultCacheMetadata.from_dict(result_cache_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


