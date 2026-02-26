# gooddata_api_client.model.aac_attribute_hierarchy.AacAttributeHierarchy

AAC attribute hierarchy definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC attribute hierarchy definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributes](#attributes)** | list, tuple,  | tuple,  | Ordered list of attribute identifiers (first is top level). | 
**id** | str,  | str,  | Unique identifier of the attribute hierarchy. | 
**type** | str,  | str,  | Attribute hierarchy type discriminator. | 
**description** | str,  | str,  | Attribute hierarchy description. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

Ordered list of attribute identifiers (first is top level).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Ordered list of attribute identifiers (first is top level). | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Ordered list of attribute identifiers (first is top level). | 

# tags

Metadata tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metadata tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Metadata tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

