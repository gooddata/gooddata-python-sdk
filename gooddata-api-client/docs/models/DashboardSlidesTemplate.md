# gooddata_api_client.model.dashboard_slides_template.DashboardSlidesTemplate

Template for dashboard slides export. Available variables: {{currentPageNumber}}, {{dashboardDateFilters}}, {{dashboardDescription}}, {{dashboardFilters}}, {{dashboardId}}, {{dashboardName}}, {{dashboardTags}}, {{dashboardUrl}}, {{exportedAt}}, {{exportedBy}}, {{logo}}, {{totalPages}}, {{workspaceId}}, {{workspaceName}}

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, None,  | frozendict.frozendict, NoneClass,  | Template for dashboard slides export. Available variables: {{currentPageNumber}}, {{dashboardDateFilters}}, {{dashboardDescription}}, {{dashboardFilters}}, {{dashboardId}}, {{dashboardName}}, {{dashboardTags}}, {{dashboardUrl}}, {{exportedAt}}, {{exportedBy}}, {{logo}}, {{totalPages}}, {{workspaceId}}, {{workspaceName}} | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[appliedOn](#appliedOn)** | list, tuple,  | tuple,  | Export types this template applies to. | 
**contentSlide** | [**ContentSlideTemplate**](ContentSlideTemplate.md) | [**ContentSlideTemplate**](ContentSlideTemplate.md) |  | [optional] 
**coverSlide** | [**CoverSlideTemplate**](CoverSlideTemplate.md) | [**CoverSlideTemplate**](CoverSlideTemplate.md) |  | [optional] 
**introSlide** | [**IntroSlideTemplate**](IntroSlideTemplate.md) | [**IntroSlideTemplate**](IntroSlideTemplate.md) |  | [optional] 
**sectionSlide** | [**SectionSlideTemplate**](SectionSlideTemplate.md) | [**SectionSlideTemplate**](SectionSlideTemplate.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# appliedOn

Export types this template applies to.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Export types this template applies to. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["PDF", "PPTX", ] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

