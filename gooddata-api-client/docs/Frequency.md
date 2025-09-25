# Frequency


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buckets** | [**List[FrequencyBucket]**](FrequencyBucket.md) |  | 

## Example

```python
from gooddata_api_client.models.frequency import Frequency

# TODO update the JSON string below
json = "{}"
# create an instance of Frequency from a JSON string
frequency_instance = Frequency.from_json(json)
# print the JSON string representation of the object
print(Frequency.to_json())

# convert the object into a dict
frequency_dict = frequency_instance.to_dict()
# create an instance of Frequency from a dict
frequency_from_dict = Frequency.from_dict(frequency_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


