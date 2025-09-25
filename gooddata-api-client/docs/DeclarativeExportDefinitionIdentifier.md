# DeclarativeExportDefinitionIdentifier

An export definition identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Export definition identifier. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_export_definition_identifier import DeclarativeExportDefinitionIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeExportDefinitionIdentifier from a JSON string
declarative_export_definition_identifier_instance = DeclarativeExportDefinitionIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeExportDefinitionIdentifier.to_json())

# convert the object into a dict
declarative_export_definition_identifier_dict = declarative_export_definition_identifier_instance.to_dict()
# create an instance of DeclarativeExportDefinitionIdentifier from a dict
declarative_export_definition_identifier_from_dict = DeclarativeExportDefinitionIdentifier.from_dict(declarative_export_definition_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


