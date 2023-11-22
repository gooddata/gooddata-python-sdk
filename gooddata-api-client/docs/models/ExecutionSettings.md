# gooddata_api_client.model.execution_settings.ExecutionSettings

Various settings affecting the process of AFM execution or its result

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Various settings affecting the process of AFM execution or its result | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**dataSamplingPercentage** | decimal.Decimal, int, float,  | decimal.Decimal,  | Specifies the percentage of rows from fact datasets to use during computation. This feature is available only for workspaces that use a Vertica Data Source without table views. | [optional] value must be a 32 bit float
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

