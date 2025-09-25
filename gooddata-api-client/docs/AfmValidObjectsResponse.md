# AfmValidObjectsResponse

All objects of specified types valid with respect to given AFM.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**items** | [**List[RestApiIdentifier]**](RestApiIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_valid_objects_response import AfmValidObjectsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AfmValidObjectsResponse from a JSON string
afm_valid_objects_response_instance = AfmValidObjectsResponse.from_json(json)
# print the JSON string representation of the object
print(AfmValidObjectsResponse.to_json())

# convert the object into a dict
afm_valid_objects_response_dict = afm_valid_objects_response_instance.to_dict()
# create an instance of AfmValidObjectsResponse from a dict
afm_valid_objects_response_from_dict = AfmValidObjectsResponse.from_dict(afm_valid_objects_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


