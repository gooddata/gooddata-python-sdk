# AfmObjectIdentifierLabel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierLabelIdentifier**](AfmObjectIdentifierLabelIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_object_identifier_label import AfmObjectIdentifierLabel

# TODO update the JSON string below
json = "{}"
# create an instance of AfmObjectIdentifierLabel from a JSON string
afm_object_identifier_label_instance = AfmObjectIdentifierLabel.from_json(json)
# print the JSON string representation of the object
print(AfmObjectIdentifierLabel.to_json())

# convert the object into a dict
afm_object_identifier_label_dict = afm_object_identifier_label_instance.to_dict()
# create an instance of AfmObjectIdentifierLabel from a dict
afm_object_identifier_label_from_dict = AfmObjectIdentifierLabel.from_dict(afm_object_identifier_label_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


