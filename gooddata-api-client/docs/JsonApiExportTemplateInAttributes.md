# JsonApiExportTemplateInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_slides_template** | [**JsonApiExportTemplateInAttributesDashboardSlidesTemplate**](JsonApiExportTemplateInAttributesDashboardSlidesTemplate.md) |  | [optional] 
**name** | **str** | User-facing name of the Slides template. | 
**widget_slides_template** | [**JsonApiExportTemplateInAttributesWidgetSlidesTemplate**](JsonApiExportTemplateInAttributesWidgetSlidesTemplate.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_template_in_attributes import JsonApiExportTemplateInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplateInAttributes from a JSON string
json_api_export_template_in_attributes_instance = JsonApiExportTemplateInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplateInAttributes.to_json())

# convert the object into a dict
json_api_export_template_in_attributes_dict = json_api_export_template_in_attributes_instance.to_dict()
# create an instance of JsonApiExportTemplateInAttributes from a dict
json_api_export_template_in_attributes_from_dict = JsonApiExportTemplateInAttributes.from_dict(json_api_export_template_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


