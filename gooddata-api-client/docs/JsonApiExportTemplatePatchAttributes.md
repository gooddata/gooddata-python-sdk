# JsonApiExportTemplatePatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_slides_template** | [**JsonApiExportTemplateInAttributesDashboardSlidesTemplate**](JsonApiExportTemplateInAttributesDashboardSlidesTemplate.md) |  | [optional] 
**name** | **str** | User-facing name of the Slides template. | [optional] 
**widget_slides_template** | [**JsonApiExportTemplateInAttributesWidgetSlidesTemplate**](JsonApiExportTemplateInAttributesWidgetSlidesTemplate.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_template_patch_attributes import JsonApiExportTemplatePatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplatePatchAttributes from a JSON string
json_api_export_template_patch_attributes_instance = JsonApiExportTemplatePatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplatePatchAttributes.to_json())

# convert the object into a dict
json_api_export_template_patch_attributes_dict = json_api_export_template_patch_attributes_instance.to_dict()
# create an instance of JsonApiExportTemplatePatchAttributes from a dict
json_api_export_template_patch_attributes_from_dict = JsonApiExportTemplatePatchAttributes.from_dict(json_api_export_template_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


