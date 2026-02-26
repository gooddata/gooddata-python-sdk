# gooddata_api_client.model.aac_query_filter.AacQueryFilter

Layer filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Layer filters. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  | Filter type. | 
**[additionalProperties](#additionalProperties)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | [optional] 
**attribute** | str,  | str,  | Attribute for ranking filter (identifier or localId). | [optional] 
**bottom** | decimal.Decimal, int,  | decimal.Decimal,  | Bottom N for ranking filter. | [optional] value must be a 32 bit integer
**condition** | str,  | str,  | Condition for metric value filter. | [optional] 
**[dimensionality](#dimensionality)** | list, tuple,  | tuple,  | Dimensionality for metric value filter. | [optional] 
**display_as** | str,  | str,  | Display as label (attribute filter). | [optional] 
**[from](#from)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] 
**granularity** | str,  | str,  | Date granularity (date filter). | [optional] 
**null_values_as_zero** | bool,  | BoolClass,  | Null values are treated as zero (metric value filter). | [optional] 
**state** | [**AacFilterState**](AacFilterState.md) | [**AacFilterState**](AacFilterState.md) |  | [optional] 
**[to](#to)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] 
**top** | decimal.Decimal, int,  | decimal.Decimal,  | Top N for ranking filter. | [optional] value must be a 32 bit integer
**using** | str,  | str,  | Reference to attribute/label/date/metric/fact (type-prefixed id). | [optional] 
**value** | decimal.Decimal, int, float,  | decimal.Decimal,  | Value for metric value filter. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# additionalProperties

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**JsonNode**](JsonNode.md) | [**JsonNode**](JsonNode.md) | any string name can be used but the value must be the correct type | [optional] 

# dimensionality

Dimensionality for metric value filter.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Dimensionality for metric value filter. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Dimensionality for metric value filter. | 

# from

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[one_of_0](#one_of_0) | str,  | str,  |  | 
[one_of_1](#one_of_1) | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# one_of_0

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# one_of_1

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# to

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[one_of_0](#one_of_0) | str,  | str,  |  | 
[one_of_1](#one_of_1) | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# one_of_0

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# one_of_1

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

