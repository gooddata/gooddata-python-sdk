# AttributeElementsByValue


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**values** | **List[Optional[str]]** | List of attribute elements by value | 

## Example

```python
from gooddata_api_client.models.attribute_elements_by_value import AttributeElementsByValue

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeElementsByValue from a JSON string
attribute_elements_by_value_instance = AttributeElementsByValue.from_json(json)
# print the JSON string representation of the object
print(AttributeElementsByValue.to_json())

# convert the object into a dict
attribute_elements_by_value_dict = attribute_elements_by_value_instance.to_dict()
# create an instance of AttributeElementsByValue from a dict
attribute_elements_by_value_from_dict = AttributeElementsByValue.from_dict(attribute_elements_by_value_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


