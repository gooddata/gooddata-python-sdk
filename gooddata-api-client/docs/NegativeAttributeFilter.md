# NegativeAttributeFilter

Filter able to limit element values by label and related selected negated elements.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**negative_attribute_filter** | [**NegativeAttributeFilterNegativeAttributeFilter**](NegativeAttributeFilterNegativeAttributeFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.negative_attribute_filter import NegativeAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of NegativeAttributeFilter from a JSON string
negative_attribute_filter_instance = NegativeAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(NegativeAttributeFilter.to_json())

# convert the object into a dict
negative_attribute_filter_dict = negative_attribute_filter_instance.to_dict()
# create an instance of NegativeAttributeFilter from a dict
negative_attribute_filter_from_dict = NegativeAttributeFilter.from_dict(negative_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


