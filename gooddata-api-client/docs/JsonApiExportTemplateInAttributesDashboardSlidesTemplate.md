# JsonApiExportTemplateInAttributesDashboardSlidesTemplate

Template for dashboard slides export. Available variables: {{currentPageNumber}}, {{dashboardDateFilters}}, {{dashboardDescription}}, {{dashboardFilters}}, {{dashboardId}}, {{dashboardName}}, {{dashboardTags}}, {{dashboardUrl}}, {{exportedAt}}, {{exportedBy}}, {{logo}}, {{totalPages}}, {{workspaceId}}, {{workspaceName}}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**applied_on** | **List[str]** | Export types this template applies to. | 
**content_slide** | [**ContentSlideTemplate**](ContentSlideTemplate.md) |  | [optional] 
**cover_slide** | [**CoverSlideTemplate**](CoverSlideTemplate.md) |  | [optional] 
**intro_slide** | [**IntroSlideTemplate**](IntroSlideTemplate.md) |  | [optional] 
**section_slide** | [**SectionSlideTemplate**](SectionSlideTemplate.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_template_in_attributes_dashboard_slides_template import JsonApiExportTemplateInAttributesDashboardSlidesTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplateInAttributesDashboardSlidesTemplate from a JSON string
json_api_export_template_in_attributes_dashboard_slides_template_instance = JsonApiExportTemplateInAttributesDashboardSlidesTemplate.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplateInAttributesDashboardSlidesTemplate.to_json())

# convert the object into a dict
json_api_export_template_in_attributes_dashboard_slides_template_dict = json_api_export_template_in_attributes_dashboard_slides_template_instance.to_dict()
# create an instance of JsonApiExportTemplateInAttributesDashboardSlidesTemplate from a dict
json_api_export_template_in_attributes_dashboard_slides_template_from_dict = JsonApiExportTemplateInAttributesDashboardSlidesTemplate.from_dict(json_api_export_template_in_attributes_dashboard_slides_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


