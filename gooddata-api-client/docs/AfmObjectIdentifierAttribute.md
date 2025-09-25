# AfmObjectIdentifierAttribute

Reference to the date attribute to use.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierAttributeIdentifier**](AfmObjectIdentifierAttributeIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_object_identifier_attribute import AfmObjectIdentifierAttribute

# TODO update the JSON string below
json = "{}"
# create an instance of AfmObjectIdentifierAttribute from a JSON string
afm_object_identifier_attribute_instance = AfmObjectIdentifierAttribute.from_json(json)
# print the JSON string representation of the object
print(AfmObjectIdentifierAttribute.to_json())

# convert the object into a dict
afm_object_identifier_attribute_dict = afm_object_identifier_attribute_instance.to_dict()
# create an instance of AfmObjectIdentifierAttribute from a dict
afm_object_identifier_attribute_from_dict = AfmObjectIdentifierAttribute.from_dict(afm_object_identifier_attribute_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


