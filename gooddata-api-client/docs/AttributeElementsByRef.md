# AttributeElementsByRef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**uris** | **List[Optional[str]]** | List of attribute elements by reference | 

## Example

```python
from gooddata_api_client.models.attribute_elements_by_ref import AttributeElementsByRef

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeElementsByRef from a JSON string
attribute_elements_by_ref_instance = AttributeElementsByRef.from_json(json)
# print the JSON string representation of the object
print(AttributeElementsByRef.to_json())

# convert the object into a dict
attribute_elements_by_ref_dict = attribute_elements_by_ref_instance.to_dict()
# create an instance of AttributeElementsByRef from a dict
attribute_elements_by_ref_from_dict = AttributeElementsByRef.from_dict(attribute_elements_by_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


