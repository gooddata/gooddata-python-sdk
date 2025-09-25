# DashboardTabularExportRequestV2

Export request object describing the export properties for dashboard tabular exports (v2 with dashboardId).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_filters_override** | [**List[DashboardFilter]**](DashboardFilter.md) | List of filters that will be used instead of the default dashboard filters. | [optional] 
**dashboard_id** | **str** | Dashboard identifier | 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Requested tabular export type. | 
**settings** | [**DashboardExportSettings**](DashboardExportSettings.md) |  | [optional] 
**widget_ids** | **List[str]** | List of widget identifiers to be exported. Note that only one widget is currently supported. | [optional] 

## Example

```python
from gooddata_api_client.models.dashboard_tabular_export_request_v2 import DashboardTabularExportRequestV2

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardTabularExportRequestV2 from a JSON string
dashboard_tabular_export_request_v2_instance = DashboardTabularExportRequestV2.from_json(json)
# print the JSON string representation of the object
print(DashboardTabularExportRequestV2.to_json())

# convert the object into a dict
dashboard_tabular_export_request_v2_dict = dashboard_tabular_export_request_v2_instance.to_dict()
# create an instance of DashboardTabularExportRequestV2 from a dict
dashboard_tabular_export_request_v2_from_dict = DashboardTabularExportRequestV2.from_dict(dashboard_tabular_export_request_v2_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


