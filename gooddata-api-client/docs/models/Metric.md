# gooddata_api_client.model.metric.Metric

List of metrics to be used in the new visualization

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of metrics to be used in the new visualization | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | ID of the object | 
**title** | str,  | str,  | Title of metric. | 
**type** | str,  | str,  | Object type | must be one of ["metric", "fact", "attribute", ] 
**aggFunction** | str,  | str,  | Agg function. Empty if a stored metric is used. | [optional] must be one of ["COUNT", "SUM", "MIN", "MAX", "AVG", "MEDIAN", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

