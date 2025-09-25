# AttributeElements


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uris** | **List[Optional[str]]** | List of attribute elements by reference | 
**values** | **List[Optional[str]]** | List of attribute elements by value | 

## Example

```python
from gooddata_api_client.models.attribute_elements import AttributeElements

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeElements from a JSON string
attribute_elements_instance = AttributeElements.from_json(json)
# print the JSON string representation of the object
print(AttributeElements.to_json())

# convert the object into a dict
attribute_elements_dict = attribute_elements_instance.to_dict()
# create an instance of AttributeElements from a dict
attribute_elements_from_dict = AttributeElements.from_dict(attribute_elements_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


