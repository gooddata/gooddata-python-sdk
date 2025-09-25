# AttributeFilterElements

Filter on specific set of label values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | **List[Optional[str]]** | Set of label values. | 

## Example

```python
from gooddata_api_client.models.attribute_filter_elements import AttributeFilterElements

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeFilterElements from a JSON string
attribute_filter_elements_instance = AttributeFilterElements.from_json(json)
# print the JSON string representation of the object
print(AttributeFilterElements.to_json())

# convert the object into a dict
attribute_filter_elements_dict = attribute_filter_elements_instance.to_dict()
# create an instance of AttributeFilterElements from a dict
attribute_filter_elements_from_dict = AttributeFilterElements.from_dict(attribute_filter_elements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


