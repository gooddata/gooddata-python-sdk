# gooddata_api_client.model.scan_request.ScanRequest

A request containing all information critical to model scanning.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A request containing all information critical to model scanning. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**scanViews** | bool,  | BoolClass,  | A flag indicating whether the views should be scanned. | 
**scanTables** | bool,  | BoolClass,  | A flag indicating whether the tables should be scanned. | 
**separator** | str,  | str,  | A separator between prefixes and the names. | 
**[schemata](#schemata)** | list, tuple,  | tuple,  | What schemata will be scanned. | [optional] 
**tablePrefix** | str,  | str,  | Tables starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the table prefix is &#x60;out_table&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_table__customers&#x60; will be scanned. | [optional] 
**viewPrefix** | str,  | str,  | Views starting with this prefix will be scanned. The prefix is then followed by the value of &#x60;separator&#x60; parameter. Given the view prefix is &#x60;out_view&#x60; and separator is &#x60;__&#x60;, the table with name like &#x60;out_view__us_customers&#x60; will be scanned. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# schemata

What schemata will be scanned.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | What schemata will be scanned. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

