# AacDashboard

AAC dashboard definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique identifier of the dashboard. | 
**type** | **str** | Dashboard type discriminator. | 
**active_tab_id** | **str** | Active tab ID for tabbed dashboards. | [optional] 
**cross_filtering** | **bool** | Whether cross filtering is enabled. | [optional] 
**description** | **str** | Dashboard description. | [optional] 
**enable_section_headers** | **bool** | Whether section headers are enabled. | [optional] 
**filter_views** | **bool** | Whether filter views are enabled. | [optional] 
**filters** | [**{str: (AacDashboardFilter,)}**](AacDashboardFilter.md) | Dashboard filters. | [optional] 
**permissions** | [**AacDashboardPermissions**](AacDashboardPermissions.md) |  | [optional] 
**plugins** | [**[AacDashboardPluginLink]**](AacDashboardPluginLink.md) | Dashboard plugins. | [optional] 
**sections** | [**[AacSection]**](AacSection.md) | Dashboard sections (for non-tabbed dashboards). | [optional] 
**tabs** | [**[AacTab]**](AacTab.md) | Dashboard tabs (for tabbed dashboards). | [optional] 
**tags** | **[str]** | Metadata tags. | [optional] 
**title** | **str** | Human readable title. | [optional] 
**user_filters_reset** | **bool** | Whether user can reset custom filters. | [optional] 
**user_filters_save** | **bool** | Whether user filter settings are stored. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


