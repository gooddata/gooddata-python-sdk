# gooddata_api_client.model.dashboard_tabular_export_request.DashboardTabularExportRequest

Export request object describing the export properties for dashboard tabular exports.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Export request object describing the export properties for dashboard tabular exports. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**fileName** | str,  | str,  | Filename of downloaded file without extension. | 
**format** | str,  | str,  | Requested tabular export type. | must be one of ["XLSX", "PDF", ] 
**[dashboardFiltersOverride](#dashboardFiltersOverride)** | list, tuple,  | tuple,  | List of filters that will be used instead of the default dashboard filters. | [optional] 
**[dashboardTabsFiltersOverrides](#dashboardTabsFiltersOverrides)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of tab-specific filter overrides. Key is tabId, value is list of filters for that tab. | [optional] 
**settings** | [**DashboardExportSettings**](DashboardExportSettings.md) | [**DashboardExportSettings**](DashboardExportSettings.md) |  | [optional] 
**[widgetIds](#widgetIds)** | list, tuple,  | tuple,  | List of widget identifiers to be exported. Note that only one widget is currently supported. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dashboardFiltersOverride

List of filters that will be used instead of the default dashboard filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of filters that will be used instead of the default dashboard filters. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DashboardFilter**](DashboardFilter.md) | [**DashboardFilter**](DashboardFilter.md) | [**DashboardFilter**](DashboardFilter.md) |  | 

# dashboardTabsFiltersOverrides

Map of tab-specific filter overrides. Key is tabId, value is list of filters for that tab.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of tab-specific filter overrides. Key is tabId, value is list of filters for that tab. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[any_string_name](#any_string_name)** | list, tuple,  | tuple,  | any string name can be used but the value must be the correct type | [optional] 

# any_string_name

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DashboardFilter**](DashboardFilter.md) | [**DashboardFilter**](DashboardFilter.md) | [**DashboardFilter**](DashboardFilter.md) |  | 

# widgetIds

List of widget identifiers to be exported. Note that only one widget is currently supported.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of widget identifiers to be exported. Note that only one widget is currently supported. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

