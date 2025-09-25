# DeclarativeExportTemplates

Export templates.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_templates** | [**List[DeclarativeExportTemplate]**](DeclarativeExportTemplate.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_export_templates import DeclarativeExportTemplates

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeExportTemplates from a JSON string
declarative_export_templates_instance = DeclarativeExportTemplates.from_json(json)
# print the JSON string representation of the object
print(DeclarativeExportTemplates.to_json())

# convert the object into a dict
declarative_export_templates_dict = declarative_export_templates_instance.to_dict()
# create an instance of DeclarativeExportTemplates from a dict
declarative_export_templates_from_dict = DeclarativeExportTemplates.from_dict(declarative_export_templates_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


