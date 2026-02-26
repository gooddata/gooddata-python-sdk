# gooddata_api_client.model.change_analysis_request.ChangeAnalysisRequest

Request for change analysis computation

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Request for change analysis computation | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**measure** | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 
**referencePeriod** | str,  | str,  | The reference time period (e.g., &#x27;2025-01&#x27;) | 
**analyzedPeriod** | str,  | str,  | The analyzed time period (e.g., &#x27;2025-02&#x27;) | 
**dateAttribute** | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 
**[attributes](#attributes)** | list, tuple,  | tuple,  | Attributes to analyze for significant changes. If empty, valid attributes will be automatically discovered. | [optional] 
**[auxMeasures](#auxMeasures)** | list, tuple,  | tuple,  | Auxiliary measures | [optional] 
**[excludeTags](#excludeTags)** | list, tuple,  | tuple,  | Exclude attributes with any of these tags. This filter applies to both auto-discovered and explicitly provided attributes. | [optional] 
**[filters](#filters)** | list, tuple,  | tuple,  | Optional filters to apply. | [optional] 
**[includeTags](#includeTags)** | list, tuple,  | tuple,  | Only include attributes with at least one of these tags. If empty, no inclusion filter is applied. This filter applies to both auto-discovered and explicitly provided attributes. | [optional] 
**useSmartAttributeSelection** | bool,  | BoolClass,  | Whether to use smart attribute selection (LLM-based) instead of discovering all valid attributes. If true, GenAI will intelligently select the most relevant attributes for change analysis. If false or not set, all valid attributes will be discovered using Calcique. Smart attribute selection applies only when no attributes are provided. | [optional] if omitted the server will use the default value of False
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

Attributes to analyze for significant changes. If empty, valid attributes will be automatically discovered.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Attributes to analyze for significant changes. If empty, valid attributes will be automatically discovered. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 

# auxMeasures

Auxiliary measures

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Auxiliary measures | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

# excludeTags

Exclude attributes with any of these tags. This filter applies to both auto-discovered and explicitly provided attributes.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Exclude attributes with any of these tags. This filter applies to both auto-discovered and explicitly provided attributes. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Exclude attributes with any of these tags. This filter applies to both auto-discovered and explicitly provided attributes. | 

# filters

Optional filters to apply.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Optional filters to apply. | 

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

# includeTags

Only include attributes with at least one of these tags. If empty, no inclusion filter is applied. This filter applies to both auto-discovered and explicitly provided attributes.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Only include attributes with at least one of these tags. If empty, no inclusion filter is applied. This filter applies to both auto-discovered and explicitly provided attributes. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Only include attributes with at least one of these tags. If empty, no inclusion filter is applied. This filter applies to both auto-discovered and explicitly provided attributes. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

