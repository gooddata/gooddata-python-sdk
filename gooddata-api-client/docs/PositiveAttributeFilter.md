# PositiveAttributeFilter

Filter able to limit element values by label and related selected elements.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**positive_attribute_filter** | [**PositiveAttributeFilterPositiveAttributeFilter**](PositiveAttributeFilterPositiveAttributeFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.positive_attribute_filter import PositiveAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of PositiveAttributeFilter from a JSON string
positive_attribute_filter_instance = PositiveAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(PositiveAttributeFilter.to_json())

# convert the object into a dict
positive_attribute_filter_dict = positive_attribute_filter_instance.to_dict()
# create an instance of PositiveAttributeFilter from a dict
positive_attribute_filter_from_dict = PositiveAttributeFilter.from_dict(positive_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


