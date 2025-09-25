# Histogram


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**buckets** | [**List[HistogramBucket]**](HistogramBucket.md) |  | 

## Example

```python
from gooddata_api_client.models.histogram import Histogram

# TODO update the JSON string below
json = "{}"
# create an instance of Histogram from a JSON string
histogram_instance = Histogram.from_json(json)
# print the JSON string representation of the object
print(Histogram.to_json())

# convert the object into a dict
histogram_dict = histogram_instance.to_dict()
# create an instance of Histogram from a dict
histogram_from_dict = Histogram.from_dict(histogram_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


