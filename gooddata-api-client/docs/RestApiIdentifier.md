# RestApiIdentifier

Object identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.rest_api_identifier import RestApiIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of RestApiIdentifier from a JSON string
rest_api_identifier_instance = RestApiIdentifier.from_json(json)
# print the JSON string representation of the object
print(RestApiIdentifier.to_json())

# convert the object into a dict
rest_api_identifier_dict = rest_api_identifier_instance.to_dict()
# create an instance of RestApiIdentifier from a dict
rest_api_identifier_from_dict = RestApiIdentifier.from_dict(rest_api_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


