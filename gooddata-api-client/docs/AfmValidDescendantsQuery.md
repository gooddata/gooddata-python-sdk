# AfmValidDescendantsQuery

Entity describing the valid descendants request.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**List[AfmObjectIdentifierAttribute]**](AfmObjectIdentifierAttribute.md) | List of identifiers of the attributes to get the valid descendants for. | 

## Example

```python
from gooddata_api_client.models.afm_valid_descendants_query import AfmValidDescendantsQuery

# TODO update the JSON string below
json = "{}"
# create an instance of AfmValidDescendantsQuery from a JSON string
afm_valid_descendants_query_instance = AfmValidDescendantsQuery.from_json(json)
# print the JSON string representation of the object
print(AfmValidDescendantsQuery.to_json())

# convert the object into a dict
afm_valid_descendants_query_dict = afm_valid_descendants_query_instance.to_dict()
# create an instance of AfmValidDescendantsQuery from a dict
afm_valid_descendants_query_from_dict = AfmValidDescendantsQuery.from_dict(afm_valid_descendants_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


