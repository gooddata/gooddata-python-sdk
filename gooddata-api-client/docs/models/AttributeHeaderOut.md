# gooddata_api_client.model.attribute_header_out.AttributeHeaderOut

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributeHeader](#attributeHeader)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributeHeader

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**primaryLabel** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**localIdentifier** | str,  | str,  |  | 
**attributeName** | str,  | str,  |  | 
**attribute** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**label** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**labelName** | str,  | str,  |  | 
**format** | [**AttributeFormat**](AttributeFormat.md) | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | str,  | str,  |  | [optional] must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

