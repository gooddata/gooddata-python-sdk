# gooddata_api_client.model.declarative_setting.DeclarativeSetting

Setting and its value.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Setting and its value. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Setting ID. | 
**[content](#content)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom setting content in JSON format. | [optional] 
**type** | str,  | str,  | Type of the setting. | [optional] must be one of ["TIMEZONE", "ACTIVE_THEME", "ACTIVE_COLOR_PALETTE", "WHITE_LABELING", "LOCALE", "FORMAT_LOCALE", "MAPBOX_TOKEN", "WEEK_START", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# content

Custom setting content in JSON format.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom setting content in JSON format. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

