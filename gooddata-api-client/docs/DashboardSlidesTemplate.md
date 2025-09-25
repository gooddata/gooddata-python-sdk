# DashboardSlidesTemplate

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
from gooddata_api_client.models.dashboard_slides_template import DashboardSlidesTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardSlidesTemplate from a JSON string
dashboard_slides_template_instance = DashboardSlidesTemplate.from_json(json)
# print the JSON string representation of the object
print(DashboardSlidesTemplate.to_json())

# convert the object into a dict
dashboard_slides_template_dict = dashboard_slides_template_instance.to_dict()
# create an instance of DashboardSlidesTemplate from a dict
dashboard_slides_template_from_dict = DashboardSlidesTemplate.from_dict(dashboard_slides_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


