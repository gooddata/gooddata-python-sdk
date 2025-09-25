# FoundObjects

List of objects found by similarity search and post-processed by LLM.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**objects** | [**List[SearchResultObject]**](SearchResultObject.md) | List of objects found with a similarity search. | 
**reasoning** | **str** | Reasoning from LLM. Description of how and why the answer was generated. | 

## Example

```python
from gooddata_api_client.models.found_objects import FoundObjects

# TODO update the JSON string below
json = "{}"
# create an instance of FoundObjects from a JSON string
found_objects_instance = FoundObjects.from_json(json)
# print the JSON string representation of the object
print(FoundObjects.to_json())

# convert the object into a dict
found_objects_dict = found_objects_instance.to_dict()
# create an instance of FoundObjects from a dict
found_objects_from_dict = FoundObjects.from_dict(found_objects_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


