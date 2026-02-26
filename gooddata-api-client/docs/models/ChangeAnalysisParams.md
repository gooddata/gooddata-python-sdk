# gooddata_api_client.model.change_analysis_params.ChangeAnalysisParams

Change analysis specification.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Change analysis specification. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**measureTitle** | str,  | str,  | The title of the measure being analyzed | 
**measure** | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 
**referencePeriod** | str,  | str,  | The reference time period | 
**[attributes](#attributes)** | list, tuple,  | tuple,  | Attributes to analyze for significant changes | 
**analyzedPeriod** | str,  | str,  | The analyzed time period | 
**[filters](#filters)** | list, tuple,  | tuple,  | Optional filters to apply | 
**useSmartAttributeSelection** | bool,  | BoolClass,  | Whether to use smart attribute selection | 
**dateAttribute** | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

Attributes to analyze for significant changes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Attributes to analyze for significant changes | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 

# filters

Optional filters to apply

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Optional filters to apply | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AbstractMeasureValueFilter](AbstractMeasureValueFilter.md) | [**AbstractMeasureValueFilter**](AbstractMeasureValueFilter.md) | [**AbstractMeasureValueFilter**](AbstractMeasureValueFilter.md) |  | 
[FilterDefinitionForSimpleMeasure](FilterDefinitionForSimpleMeasure.md) | [**FilterDefinitionForSimpleMeasure**](FilterDefinitionForSimpleMeasure.md) | [**FilterDefinitionForSimpleMeasure**](FilterDefinitionForSimpleMeasure.md) |  | 
[InlineFilterDefinition](InlineFilterDefinition.md) | [**InlineFilterDefinition**](InlineFilterDefinition.md) | [**InlineFilterDefinition**](InlineFilterDefinition.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

