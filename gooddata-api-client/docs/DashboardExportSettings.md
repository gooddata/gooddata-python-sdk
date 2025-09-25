# DashboardExportSettings

Additional settings.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_info** | **bool** | If true, the export will contain the information about the export – exported date, dashboard filters, etc. | [optional]  if omitted the server will use the default value of False
**merge_headers** | **bool** | Merge equal headers in neighbouring cells. Used for [XLSX] format only. | [optional]  if omitted the server will use the default value of False
**page_orientation** | **str** | Set page orientation. (PDF) | [optional]  if omitted the server will use the default value of "PORTRAIT"
**page_size** | **str** | Set page size. (PDF) | [optional]  if omitted the server will use the default value of "A4"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


