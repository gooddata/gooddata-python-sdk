# IdentifierRef


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**IdentifierRefIdentifier**](IdentifierRefIdentifier.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.identifier_ref import IdentifierRef

# TODO update the JSON string below
json = "{}"
# create an instance of IdentifierRef from a JSON string
identifier_ref_instance = IdentifierRef.from_json(json)
# print the JSON string representation of the object
print(IdentifierRef.to_json())

# convert the object into a dict
identifier_ref_dict = identifier_ref_instance.to_dict()
# create an instance of IdentifierRef from a dict
identifier_ref_from_dict = IdentifierRef.from_dict(identifier_ref_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


