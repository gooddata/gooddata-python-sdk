# WidgetSlidesTemplate

Template for widget slides export. Available variables: {{currentPageNumber}}, {{dashboardDateFilters}}, {{dashboardDescription}}, {{dashboardFilters}}, {{dashboardId}}, {{dashboardName}}, {{dashboardTags}}, {{dashboardUrl}}, {{exportedAt}}, {{exportedBy}}, {{logo}}, {{totalPages}}, {{workspaceId}}, {{workspaceName}}

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**applied_on** | **List[str]** | Export types this template applies to. | 
**content_slide** | [**ContentSlideTemplate**](ContentSlideTemplate.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.widget_slides_template import WidgetSlidesTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of WidgetSlidesTemplate from a JSON string
widget_slides_template_instance = WidgetSlidesTemplate.from_json(json)
# print the JSON string representation of the object
print(WidgetSlidesTemplate.to_json())

# convert the object into a dict
widget_slides_template_dict = widget_slides_template_instance.to_dict()
# create an instance of WidgetSlidesTemplate from a dict
widget_slides_template_from_dict = WidgetSlidesTemplate.from_dict(widget_slides_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


