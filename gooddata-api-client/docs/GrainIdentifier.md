# GrainIdentifier

A grain identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Grain ID. | 
**type** | **str** | A type of the grain. | 

## Example

```python
from gooddata_api_client.models.grain_identifier import GrainIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of GrainIdentifier from a JSON string
grain_identifier_instance = GrainIdentifier.from_json(json)
# print the JSON string representation of the object
print(GrainIdentifier.to_json())

# convert the object into a dict
grain_identifier_dict = grain_identifier_instance.to_dict()
# create an instance of GrainIdentifier from a dict
grain_identifier_from_dict = GrainIdentifier.from_dict(grain_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


