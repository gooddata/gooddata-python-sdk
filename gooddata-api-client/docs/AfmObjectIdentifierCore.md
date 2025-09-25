# AfmObjectIdentifierCore

Reference to the metric, fact or attribute object to use for the metric.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierCoreIdentifier**](AfmObjectIdentifierCoreIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_object_identifier_core import AfmObjectIdentifierCore

# TODO update the JSON string below
json = "{}"
# create an instance of AfmObjectIdentifierCore from a JSON string
afm_object_identifier_core_instance = AfmObjectIdentifierCore.from_json(json)
# print the JSON string representation of the object
print(AfmObjectIdentifierCore.to_json())

# convert the object into a dict
afm_object_identifier_core_dict = afm_object_identifier_core_instance.to_dict()
# create an instance of AfmObjectIdentifierCore from a dict
afm_object_identifier_core_from_dict = AfmObjectIdentifierCore.from_dict(afm_object_identifier_core_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


