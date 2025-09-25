# PositiveAttributeFilterPositiveAttributeFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**var_in** | [**AttributeFilterElements**](AttributeFilterElements.md) |  | 
**label** | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**local_identifier** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.positive_attribute_filter_positive_attribute_filter import PositiveAttributeFilterPositiveAttributeFilter

# TODO update the JSON string below
json = "{}"
# create an instance of PositiveAttributeFilterPositiveAttributeFilter from a JSON string
positive_attribute_filter_positive_attribute_filter_instance = PositiveAttributeFilterPositiveAttributeFilter.from_json(json)
# print the JSON string representation of the object
print(PositiveAttributeFilterPositiveAttributeFilter.to_json())

# convert the object into a dict
positive_attribute_filter_positive_attribute_filter_dict = positive_attribute_filter_positive_attribute_filter_instance.to_dict()
# create an instance of PositiveAttributeFilterPositiveAttributeFilter from a dict
positive_attribute_filter_positive_attribute_filter_from_dict = PositiveAttributeFilterPositiveAttributeFilter.from_dict(positive_attribute_filter_positive_attribute_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


