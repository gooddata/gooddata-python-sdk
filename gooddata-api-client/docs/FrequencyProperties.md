# FrequencyProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**value_limit** | **int** | The maximum number of distinct values to return. | [optional] [default to 10]

## Example

```python
from gooddata_api_client.models.frequency_properties import FrequencyProperties

# TODO update the JSON string below
json = "{}"
# create an instance of FrequencyProperties from a JSON string
frequency_properties_instance = FrequencyProperties.from_json(json)
# print the JSON string representation of the object
print(FrequencyProperties.to_json())

# convert the object into a dict
frequency_properties_dict = frequency_properties_instance.to_dict()
# create an instance of FrequencyProperties from a dict
frequency_properties_from_dict = FrequencyProperties.from_dict(frequency_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


