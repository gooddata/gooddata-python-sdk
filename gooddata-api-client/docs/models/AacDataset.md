# gooddata_api_client.model.aac_dataset.AacDataset

AAC dataset definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC dataset definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique identifier of the dataset. | 
**type** | str,  | str,  | Dataset type discriminator. | 
**data_source** | str,  | str,  | Data source ID. | [optional] 
**description** | str,  | str,  | Dataset description. | [optional] 
**[fields](#fields)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Dataset fields (attributes, facts, aggregated facts). | [optional] 
**precedence** | decimal.Decimal, int,  | decimal.Decimal,  | Precedence value for aggregate awareness. | [optional] value must be a 32 bit integer
**[primary_key](#primary_key)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Primary key column(s). Accepts either a single string or an array of strings. | [optional] 
**[references](#references)** | list, tuple,  | tuple,  | References to other datasets. | [optional] 
**sql** | str,  | str,  | SQL statement defining this dataset. | [optional] 
**table_path** | str,  | str,  | Table path in the data source. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
**[workspace_data_filters](#workspace_data_filters)** | list, tuple,  | tuple,  | Workspace data filters. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# fields

Dataset fields (attributes, facts, aggregated facts).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Dataset fields (attributes, facts, aggregated facts). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**AacField**](AacField.md) | [**AacField**](AacField.md) | any string name can be used but the value must be the correct type | [optional] 

# primary_key

Primary key column(s). Accepts either a single string or an array of strings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Primary key column(s). Accepts either a single string or an array of strings. | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[one_of_0](#one_of_0) | str,  | str,  |  | 
[one_of_1](#one_of_1) | list, tuple,  | tuple,  |  | 
[one_of_2](#one_of_2) | None,  | NoneClass,  |  | 

# one_of_0

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# one_of_1

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# one_of_2

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
None,  | NoneClass,  |  | 

# references

References to other datasets.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | References to other datasets. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacReference**](AacReference.md) | [**AacReference**](AacReference.md) | [**AacReference**](AacReference.md) |  | 

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

# workspace_data_filters

Workspace data filters.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Workspace data filters. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacWorkspaceDataFilter**](AacWorkspaceDataFilter.md) | [**AacWorkspaceDataFilter**](AacWorkspaceDataFilter.md) | [**AacWorkspaceDataFilter**](AacWorkspaceDataFilter.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

