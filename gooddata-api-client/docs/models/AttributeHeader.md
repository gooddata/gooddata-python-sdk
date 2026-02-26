# gooddata_api_client.model.attribute_header.AttributeHeader

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
**localIdentifier** | str,  | str,  | Local identifier of the attribute this header relates to. | 
**attributeName** | str,  | str,  | Attribute name. | 
**attribute** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**label** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**labelName** | str,  | str,  | Label name. | 
**format** | [**AttributeFormat**](AttributeFormat.md) | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**geoAreaConfig** | [**GeoAreaConfig**](GeoAreaConfig.md) | [**GeoAreaConfig**](GeoAreaConfig.md) |  | [optional] 
**granularity** | str,  | str,  | Date granularity of the attribute, only filled for date attributes. | [optional] must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_QUARTER", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", "FISCAL_MONTH", "FISCAL_QUARTER", "FISCAL_YEAR", ] 
**valueType** | str,  | str,  | Attribute value type. | [optional] must be one of ["TEXT", "HYPERLINK", "GEO", "GEO_LONGITUDE", "GEO_LATITUDE", "GEO_AREA", "IMAGE", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

