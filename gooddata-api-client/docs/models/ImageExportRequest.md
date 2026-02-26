# gooddata_api_client.model.image_export_request.ImageExportRequest

Export request object describing the export properties and metadata for image exports.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Export request object describing the export properties and metadata for image exports. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**fileName** | str,  | str,  | File name to be used for retrieving the image document. | 
**dashboardId** | str,  | str,  | Dashboard identifier | 
**[widgetIds](#widgetIds)** | list, tuple,  | tuple,  | List of widget identifiers to be exported. Note that only one widget is currently supported. | 
**format** | str,  | str,  | Requested resulting file type. | must be one of ["PNG", ] 
**metadata** | [**JsonNode**](JsonNode.md) | [**JsonNode**](JsonNode.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

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

