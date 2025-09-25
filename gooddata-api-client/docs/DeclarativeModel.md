# DeclarativeModel

A data model structured as a set of its attributes.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ldm** | [**DeclarativeLdm**](DeclarativeLdm.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_model import DeclarativeModel

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeModel from a JSON string
declarative_model_instance = DeclarativeModel.from_json(json)
# print the JSON string representation of the object
print(DeclarativeModel.to_json())

# convert the object into a dict
declarative_model_dict = declarative_model_instance.to_dict()
# create an instance of DeclarativeModel from a dict
declarative_model_from_dict = DeclarativeModel.from_dict(declarative_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


