# gooddata_api_client.model.dashboard_attribute_filter.DashboardAttributeFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributeFilter](#attributeFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributeFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**negativeSelection** | bool,  | BoolClass,  |  | 
**displayForm** | [**IdentifierRef**](IdentifierRef.md) | [**IdentifierRef**](IdentifierRef.md) |  | 
**attributeElements** | [**AttributeElements**](AttributeElements.md) | [**AttributeElements**](AttributeElements.md) |  | 
**[filterElementsBy](#filterElementsBy)** | list, tuple,  | tuple,  |  | [optional] 
**[filterElementsByDate](#filterElementsByDate)** | list, tuple,  | tuple,  |  | [optional] 
**localIdentifier** | str,  | str,  |  | [optional] 
**selectionMode** | str,  | str,  |  | [optional] must be one of ["single", "multi", ] 
**title** | str,  | str,  |  | [optional] 
**[validateElementsBy](#validateElementsBy)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filterElementsBy

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeFilterParent**](AttributeFilterParent.md) | [**AttributeFilterParent**](AttributeFilterParent.md) | [**AttributeFilterParent**](AttributeFilterParent.md) |  | 

# filterElementsByDate

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeFilterByDate**](AttributeFilterByDate.md) | [**AttributeFilterByDate**](AttributeFilterByDate.md) | [**AttributeFilterByDate**](AttributeFilterByDate.md) |  | 

# validateElementsBy

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**IdentifierRef**](IdentifierRef.md) | [**IdentifierRef**](IdentifierRef.md) | [**IdentifierRef**](IdentifierRef.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

