# AfmObjectIdentifier

ObjectIdentifier with `identifier` wrapper. This serves to distinguish MD object identifiers in AFM request from local identifiers.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierIdentifier**](AfmObjectIdentifierIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_object_identifier import AfmObjectIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of AfmObjectIdentifier from a JSON string
afm_object_identifier_instance = AfmObjectIdentifier.from_json(json)
# print the JSON string representation of the object
print(AfmObjectIdentifier.to_json())

# convert the object into a dict
afm_object_identifier_dict = afm_object_identifier_instance.to_dict()
# create an instance of AfmObjectIdentifier from a dict
afm_object_identifier_from_dict = AfmObjectIdentifier.from_dict(afm_object_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


