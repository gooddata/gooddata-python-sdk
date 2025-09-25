# SortKeyAttributeAttribute


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_identifier** | **str** | Item reference (to &#39;itemIdentifiers&#39;) referencing, which item should be used for sorting. Only references to attributes are allowed. | 
**direction** | **str** | Sorting elements - ascending/descending order. | [optional] 
**sort_type** | **str** | Mechanism by which this attribute should be sorted. Available options are: - DEFAULT: sorting based on default rules (using sort column if defined, otherwise this label)  - LABEL: sorting by this label values  - ATTRIBUTE: sorting by values of this label&#39;s attribute (or rather the primary label)  - ATTRIBUTE: sorting by values of this label&#39;s attribute (or rather the primary label)- AREA: sorting by area (total or subtotal) corresponding to each attribute value. The area is computed by summing up all metric values in all other dimensions. | [optional] [default to 'DEFAULT']

## Example

```python
from gooddata_api_client.models.sort_key_attribute_attribute import SortKeyAttributeAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of SortKeyAttributeAttribute from a JSON string
sort_key_attribute_attribute_instance = SortKeyAttributeAttribute.from_json(json)
# print the JSON string representation of the object
print(SortKeyAttributeAttribute.to_json())

# convert the object into a dict
sort_key_attribute_attribute_dict = sort_key_attribute_attribute_instance.to_dict()
# create an instance of SortKeyAttributeAttribute from a dict
sort_key_attribute_attribute_from_dict = SortKeyAttributeAttribute.from_dict(sort_key_attribute_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


