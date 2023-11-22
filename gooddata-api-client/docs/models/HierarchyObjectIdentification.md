# gooddata_api_client.model.hierarchy_object_identification.HierarchyObjectIdentification

Represents objects with given ID and type in workspace hierarchy (more than one can exists in different workspaces).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Represents objects with given ID and type in workspace hierarchy (more than one can exists in different workspaces). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  |  | 
**type** | str,  | str,  |  | must be one of ["analyticalDashboard", "attribute", "dashboardPlugin", "dataset", "fact", "label", "metric", "prompt", "visualizationObject", "filterContext", "workspaceDataFilter", "workspaceDataFilterSettings", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

