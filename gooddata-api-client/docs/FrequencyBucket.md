# FrequencyBucket


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** |  | 
**value** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.frequency_bucket import FrequencyBucket

# TODO update the JSON string below
json = "{}"
# create an instance of FrequencyBucket from a JSON string
frequency_bucket_instance = FrequencyBucket.from_json(json)
# print the JSON string representation of the object
print(FrequencyBucket.to_json())

# convert the object into a dict
frequency_bucket_dict = frequency_bucket_instance.to_dict()
# create an instance of FrequencyBucket from a dict
frequency_bucket_from_dict = FrequencyBucket.from_dict(frequency_bucket_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


