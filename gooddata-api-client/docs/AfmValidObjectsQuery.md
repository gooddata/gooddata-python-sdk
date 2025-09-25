# AfmValidObjectsQuery

Entity holding AFM and list of object types whose validity should be computed.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**afm** | [**AFM**](AFM.md) |  | 
**types** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.afm_valid_objects_query import AfmValidObjectsQuery

# TODO update the JSON string below
json = "{}"
# create an instance of AfmValidObjectsQuery from a JSON string
afm_valid_objects_query_instance = AfmValidObjectsQuery.from_json(json)
# print the JSON string representation of the object
print(AfmValidObjectsQuery.to_json())

# convert the object into a dict
afm_valid_objects_query_dict = afm_valid_objects_query_instance.to_dict()
# create an instance of AfmValidObjectsQuery from a dict
afm_valid_objects_query_from_dict = AfmValidObjectsQuery.from_dict(afm_valid_objects_query_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


