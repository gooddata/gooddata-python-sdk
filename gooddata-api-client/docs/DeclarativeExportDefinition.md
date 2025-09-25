# DeclarativeExportDefinition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Export definition object description. | [optional] 
**id** | **str** | Export definition id. | 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**request_payload** | [**DeclarativeExportDefinitionRequestPayload**](DeclarativeExportDefinitionRequestPayload.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Export definition object title. | 

## Example

```python
from gooddata_api_client.models.declarative_export_definition import DeclarativeExportDefinition

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeExportDefinition from a JSON string
declarative_export_definition_instance = DeclarativeExportDefinition.from_json(json)
# print the JSON string representation of the object
print(DeclarativeExportDefinition.to_json())

# convert the object into a dict
declarative_export_definition_dict = declarative_export_definition_instance.to_dict()
# create an instance of DeclarativeExportDefinition from a dict
declarative_export_definition_from_dict = DeclarativeExportDefinition.from_dict(declarative_export_definition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


