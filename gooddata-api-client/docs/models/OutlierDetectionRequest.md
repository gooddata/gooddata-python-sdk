# gooddata_api_client.model.outlier_detection_request.OutlierDetectionRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[measures](#measures)** | list, tuple,  | tuple,  |  | 
**granularity** | str,  | str,  | Date granularity for anomaly detection. Only time-based granularities are supported (HOUR, DAY, WEEK, MONTH, QUARTER, YEAR). | must be one of ["HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", ] 
**[attributes](#attributes)** | list, tuple,  | tuple,  | Attributes to be used in the computation. | 
**[filters](#filters)** | list, tuple,  | tuple,  | Various filter types to filter the execution result. | 
**sensitivity** | str,  | str,  | Sensitivity level for outlier detection | must be one of ["LOW", "MEDIUM", "HIGH", ] 
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

Various filter types to filter the execution result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Various filter types to filter the execution result. | 

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

# measures

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

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

