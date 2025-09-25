# AfmIdentifier

Reference to the attribute label to which the filter should be applied.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierIdentifier**](AfmObjectIdentifierIdentifier.md) |  | 
**local_identifier** | **str** |  | 

## Example

```python
from gooddata_api_client.models.afm_identifier import AfmIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of AfmIdentifier from a JSON string
afm_identifier_instance = AfmIdentifier.from_json(json)
# print the JSON string representation of the object
print(AfmIdentifier.to_json())

# convert the object into a dict
afm_identifier_dict = afm_identifier_instance.to_dict()
# create an instance of AfmIdentifier from a dict
afm_identifier_from_dict = AfmIdentifier.from_dict(afm_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


