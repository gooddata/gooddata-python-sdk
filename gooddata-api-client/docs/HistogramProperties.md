# HistogramProperties


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bucket_count** | **int** |  | 

## Example

```python
from gooddata_api_client.models.histogram_properties import HistogramProperties

# TODO update the JSON string below
json = "{}"
# create an instance of HistogramProperties from a JSON string
histogram_properties_instance = HistogramProperties.from_json(json)
# print the JSON string representation of the object
print(HistogramProperties.to_json())

# convert the object into a dict
histogram_properties_dict = histogram_properties_instance.to_dict()
# create an instance of HistogramProperties from a dict
histogram_properties_from_dict = HistogramProperties.from_dict(histogram_properties_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


