# EntityIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Object identifier. | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.entity_identifier import EntityIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of EntityIdentifier from a JSON string
entity_identifier_instance = EntityIdentifier.from_json(json)
# print the JSON string representation of the object
print(EntityIdentifier.to_json())

# convert the object into a dict
entity_identifier_dict = entity_identifier_instance.to_dict()
# create an instance of EntityIdentifier from a dict
entity_identifier_from_dict = EntityIdentifier.from_dict(entity_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


