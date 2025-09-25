# NegativeAttributeFilterNegativeAttributeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**label** | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**local_identifier** | **str** |  | [optional] 
**not_in** | [**AttributeFilterElements**](AttributeFilterElements.md) |  | 

## Example

```python
from gooddata_api_client.models.negative_attribute_filter_negative_attribute_filter import NegativeAttributeFilterNegativeAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of NegativeAttributeFilterNegativeAttributeFilter from a JSON string
negative_attribute_filter_negative_attribute_filter_instance = NegativeAttributeFilterNegativeAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(NegativeAttributeFilterNegativeAttributeFilter.to_json())

# convert the object into a dict
negative_attribute_filter_negative_attribute_filter_dict = negative_attribute_filter_negative_attribute_filter_instance.to_dict()
# create an instance of NegativeAttributeFilterNegativeAttributeFilter from a dict
negative_attribute_filter_negative_attribute_filter_from_dict = NegativeAttributeFilterNegativeAttributeFilter.from_dict(negative_attribute_filter_negative_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


