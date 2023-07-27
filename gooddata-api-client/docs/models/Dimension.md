# gooddata_api_client.model.dimension.Dimension

Single dimension description.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Single dimension description. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[itemIdentifiers](#itemIdentifiers)** | list, tuple,  | tuple,  | List of items in current dimension. Can reference &#x27;localIdentifier&#x27; from &#x27;AttributeItem&#x27;, or special pseudo attribute \&quot;measureGroup\&quot; representing list of metrics. | 
**localIdentifier** | str,  | str,  | Dimension identification within requests. Other entities can reference this dimension by this value. | [optional] 
**[sorting](#sorting)** | list, tuple,  | tuple,  | List of sorting rules. From most relevant to least relevant (less relevant rule is applied, when more relevant rule compares items as equal). | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# itemIdentifiers

List of items in current dimension. Can reference 'localIdentifier' from 'AttributeItem', or special pseudo attribute \"measureGroup\" representing list of metrics.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of items in current dimension. Can reference &#x27;localIdentifier&#x27; from &#x27;AttributeItem&#x27;, or special pseudo attribute \&quot;measureGroup\&quot; representing list of metrics. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# sorting

List of sorting rules. From most relevant to least relevant (less relevant rule is applied, when more relevant rule compares items as equal).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of sorting rules. From most relevant to least relevant (less relevant rule is applied, when more relevant rule compares items as equal). | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**SortKey**](SortKey.md) | [**SortKey**](SortKey.md) | [**SortKey**](SortKey.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

