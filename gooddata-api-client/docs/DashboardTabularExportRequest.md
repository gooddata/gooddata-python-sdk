# DashboardTabularExportRequest

Export request object describing the export properties for dashboard tabular exports.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested tabular export type. | defaults to "XLSX"
**dashboard_filters_override** | [**[DashboardTabularExportRequestDashboardFiltersOverrideInner]**](DashboardTabularExportRequestDashboardFiltersOverrideInner.md) | List of filters that will be used instead of the default dashboard filters. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


