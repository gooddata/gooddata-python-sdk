# gooddata_api_client.model.elements_request.ElementsRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**label** | str,  | str,  | Requested label. | 
**complementFilter** | bool,  | BoolClass,  | Inverse filters: * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items not matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; and &#x60;&#x60;&#x60;exactFilter&#x60;&#x60;&#x60; | [optional] if omitted the server will use the default value of False
**dataSamplingPercentage** | decimal.Decimal, int, float,  | decimal.Decimal,  | Specifies percentage of source table data scanned during the computation. This field is deprecated and is no longer used during the elements computation. | [optional] if omitted the server will use the default value of 100value must be a 32 bit float
**[exactFilter](#exactFilter)** | list, tuple,  | tuple,  | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title exactly matches one of &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60;. | [optional] 
**excludePrimaryLabel** | bool,  | BoolClass,  | Excludes items from the result that differ only by primary label * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items with distinct primary label * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items with distinct requested label | [optional] if omitted the server will use the default value of False
**filterBy** | [**FilterBy**](FilterBy.md) | [**FilterBy**](FilterBy.md) |  | [optional] 
**patternFilter** | str,  | str,  | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title case insensitively contains &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60; as substring. | [optional] 
**sortOrder** | str,  | str,  | Sort order of returned items. Items are sorted by &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title. If no sort order is specified then attribute&#x27;s &#x60;&#x60;&#x60;sortDirection&#x60;&#x60;&#x60; is used, which is ASC by default | [optional] must be one of ["ASC", "DESC", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# exactFilter

Return only items, whose ```label``` title exactly matches one of ```filter```.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title exactly matches one of &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60;. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title exactly matches one of &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60;. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

