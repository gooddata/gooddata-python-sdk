# gooddata_api_client.model.identifier_duplications.IdentifierDuplications

Contains information about conflicting IDs in workspace hierarchy

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Contains information about conflicting IDs in workspace hierarchy | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[origins](#origins)** | list, tuple,  | tuple,  |  | 
**id** | str,  | str,  |  | 
**type** | str,  | str,  |  | must be one of ["analyticalDashboard", "attribute", "dashboardPlugin", "dataset", "fact", "label", "metric", "prompt", "visualizationObject", "filterContext", "workspaceDataFilter", "workspaceDataFilterSettings", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# origins

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

