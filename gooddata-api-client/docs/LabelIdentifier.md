# LabelIdentifier

A label identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Label ID. | 
**type** | **str** | A type of the label. | 

## Example

```python
from gooddata_api_client.models.label_identifier import LabelIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of LabelIdentifier from a JSON string
label_identifier_instance = LabelIdentifier.from_json(json)
# print the JSON string representation of the object
print(LabelIdentifier.to_json())

# convert the object into a dict
label_identifier_dict = label_identifier_instance.to_dict()
# create an instance of LabelIdentifier from a dict
label_identifier_from_dict = LabelIdentifier.from_dict(label_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


