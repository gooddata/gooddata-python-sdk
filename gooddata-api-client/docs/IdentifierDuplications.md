# IdentifierDuplications

Contains information about conflicting IDs in workspace hierarchy

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**origins** | **List[str]** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.identifier_duplications import IdentifierDuplications

# TODO update the JSON string below
json = "{}"
# create an instance of IdentifierDuplications from a JSON string
identifier_duplications_instance = IdentifierDuplications.from_json(json)
# print the JSON string representation of the object
print(IdentifierDuplications.to_json())

# convert the object into a dict
identifier_duplications_dict = identifier_duplications_instance.to_dict()
# create an instance of IdentifierDuplications from a dict
identifier_duplications_from_dict = IdentifierDuplications.from_dict(identifier_duplications_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


