# ReferenceIdentifier

A reference identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Reference ID. | 
**type** | **str** | A type of the reference. | 

## Example

```python
from gooddata_api_client.models.reference_identifier import ReferenceIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of ReferenceIdentifier from a JSON string
reference_identifier_instance = ReferenceIdentifier.from_json(json)
# print the JSON string representation of the object
print(ReferenceIdentifier.to_json())

# convert the object into a dict
reference_identifier_dict = reference_identifier_instance.to_dict()
# create an instance of ReferenceIdentifier from a dict
reference_identifier_from_dict = ReferenceIdentifier.from_dict(reference_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


