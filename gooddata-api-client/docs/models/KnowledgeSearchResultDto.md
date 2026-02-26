# gooddata_api_client.model.knowledge_search_result_dto.KnowledgeSearchResultDto

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**score** | decimal.Decimal, int, float,  | decimal.Decimal,  |  | value must be a 32 bit float
**filename** | str,  | str,  |  | 
**[pageNumbers](#pageNumbers)** | list, tuple,  | tuple,  |  | 
**totalChunks** | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer
**[scopes](#scopes)** | list, tuple,  | tuple,  |  | 
**chunkIndex** | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer
**content** | str,  | str,  |  | 
**title** | str,  | str,  |  | [optional] 
**workspaceId** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# pageNumbers

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | decimal.Decimal, int,  | decimal.Decimal,  |  | value must be a 32 bit integer

# scopes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

