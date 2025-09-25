# AfmValidDescendantsResponse

Entity describing the valid descendants response.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**valid_descendants** | **Dict[str, List[AfmObjectIdentifierAttribute]]** | Map of attribute identifiers to list of valid descendants identifiers. | 

## Example

```python
from gooddata_api_client.models.afm_valid_descendants_response import AfmValidDescendantsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AfmValidDescendantsResponse from a JSON string
afm_valid_descendants_response_instance = AfmValidDescendantsResponse.from_json(json)
# print the JSON string representation of the object
print(AfmValidDescendantsResponse.to_json())

# convert the object into a dict
afm_valid_descendants_response_dict = afm_valid_descendants_response_instance.to_dict()
# create an instance of AfmValidDescendantsResponse from a dict
afm_valid_descendants_response_from_dict = AfmValidDescendantsResponse.from_dict(afm_valid_descendants_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


