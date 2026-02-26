# gooddata_api_client.model.declarative_attribute_hierarchy.DeclarativeAttributeHierarchy

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Attribute hierarchy object ID. | 
**title** | str,  | str,  | Attribute hierarchy object title. | 
**content** | [**JsonNode**](JsonNode.md) | [**JsonNode**](JsonNode.md) |  | 
**createdAt** | None, str,  | NoneClass, str,  | Time of the entity creation. | [optional] 
**createdBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | str,  | str,  | Attribute hierarchy object description. | [optional] 
**modifiedAt** | None, str,  | NoneClass, str,  | Time of the last entity modification. | [optional] 
**modifiedBy** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# tags

A list of tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | A list of tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

