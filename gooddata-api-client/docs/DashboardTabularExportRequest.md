# DashboardTabularExportRequest

Export request object describing the export properties for dashboard tabular exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested tabular export type. | 
**dashboard_filters_override** | [**[DashboardFilter]**](DashboardFilter.md) | List of filters that will be used instead of the default dashboard filters. | [optional] 
**dashboard_parameters_override** | [**[DashboardParameterValue]**](DashboardParameterValue.md) | Parameter value overrides applied to the export&#39;s executions. Each entry carries the parameter id (used as an AFM execution override) plus the FE-supplied title for the info sheet. Applied uniformly across all tabs; use dashboardTabsParametersOverrides for tab-scoped overrides. | [optional] 
**dashboard_tabs_filters_overrides** | **{str: ([DashboardFilter],)}** | Map of tab-specific filter overrides. Key is tabId, value is list of filters for that tab. | [optional] 
**dashboard_tabs_parameters_overrides** | **{str: ([DashboardParameterValue],)}** | Map of tab-specific parameter overrides. Key is tabId, value is a list of (id, value, title) entries that override the dashboard-level parameters for that tab only. Mirrors dashboardTabsFiltersOverrides. When a tab is present in this map, its entries take precedence over dashboardParametersOverride for that tab&#39;s executions and info-sheet display. | [optional] 
**settings** | [**DashboardExportSettings**](DashboardExportSettings.md) |  | [optional] 
**widget_ids** | **[str]** | List of widget identifiers to be exported. Note that only one widget is currently supported. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


