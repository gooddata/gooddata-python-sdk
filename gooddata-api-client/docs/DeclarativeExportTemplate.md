# DeclarativeExportTemplate

A declarative form of a particular export template.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_slides_template** | [**DashboardSlidesTemplate**](DashboardSlidesTemplate.md) |  | [optional] 
**id** | **str** | Identifier of an export template | 
**name** | **str** | Name of an export template. | 
**widget_slides_template** | [**WidgetSlidesTemplate**](WidgetSlidesTemplate.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_export_template import DeclarativeExportTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeExportTemplate from a JSON string
declarative_export_template_instance = DeclarativeExportTemplate.from_json(json)
# print the JSON string representation of the object
print(DeclarativeExportTemplate.to_json())

# convert the object into a dict
declarative_export_template_dict = declarative_export_template_instance.to_dict()
# create an instance of DeclarativeExportTemplate from a dict
declarative_export_template_from_dict = DeclarativeExportTemplate.from_dict(declarative_export_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


