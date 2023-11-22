# gooddata_api_client.model.elements_response.ElementsResponse

Entity holding list of sorted & filtered label elements, related primary label of attribute owning requested label and paging.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Entity holding list of sorted &amp; filtered label elements, related primary label of attribute owning requested label and paging. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**primaryLabel** | [**RestApiIdentifier**](RestApiIdentifier.md) | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 
**[elements](#elements)** | list, tuple,  | tuple,  | List of returned elements. | 
**paging** | [**Paging**](Paging.md) | [**Paging**](Paging.md) |  | 
**format** | [**AttributeFormat**](AttributeFormat.md) | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | str,  | str,  | Granularity of requested label in case of date attribute | [optional] must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# elements

List of returned elements.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of returned elements. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Element**](Element.md) | [**Element**](Element.md) | [**Element**](Element.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

