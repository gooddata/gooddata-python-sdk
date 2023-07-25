# gooddata_api_client.model.afm.AFM

Top level executable entity. Combination of [A]ttributes, [F]ilters & [M]etrics.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Top level executable entity. Combination of [A]ttributes, [F]ilters &amp; [M]etrics. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[measures](#measures)** | list, tuple,  | tuple,  | Metrics to be computed. | 
**[attributes](#attributes)** | list, tuple,  | tuple,  | Attributes to be used in the computation. | 
**[filters](#filters)** | list, tuple,  | tuple,  | Various filter types to filter execution result. | 
**[auxMeasures](#auxMeasures)** | list, tuple,  | tuple,  | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

Attributes to be used in the computation.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Attributes to be used in the computation. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 

# filters

Various filter types to filter execution result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Various filter types to filter execution result. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**FilterDefinition**](FilterDefinition.md) | [**FilterDefinition**](FilterDefinition.md) | [**FilterDefinition**](FilterDefinition.md) |  | 

# measures

Metrics to be computed.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metrics to be computed. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

# auxMeasures

Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

