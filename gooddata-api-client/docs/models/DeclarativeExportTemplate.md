# gooddata_api_client.model.declarative_export_template.DeclarativeExportTemplate

A declarative form of a particular export template.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A declarative form of a particular export template. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**name** | str,  | str,  | Name of an export template. | 
**id** | str,  | str,  | Identifier of an export template | 
**dashboardSlidesTemplate** | [**DashboardSlidesTemplate**](DashboardSlidesTemplate.md) | [**DashboardSlidesTemplate**](DashboardSlidesTemplate.md) |  | [optional] 
**widgetSlidesTemplate** | [**WidgetSlidesTemplate**](WidgetSlidesTemplate.md) | [**WidgetSlidesTemplate**](WidgetSlidesTemplate.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

