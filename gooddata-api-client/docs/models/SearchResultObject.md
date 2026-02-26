# gooddata_api_client.model.search_result_object.SearchResultObject

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Object ID. | 
**title** | str,  | str,  | Object title. | 
**type** | str,  | str,  | Object type, e.g. dashboard. | 
**workspaceId** | str,  | str,  | Workspace ID. | 
**createdAt** | str, datetime,  | str,  | Timestamp when object was created. | [optional] value must conform to RFC-3339 date-time
**description** | str,  | str,  | Object description. | [optional] 
**isHidden** | bool,  | BoolClass,  | If true, this object is hidden from AI search results by default. | [optional] 
**modifiedAt** | str, datetime,  | str,  | Timestamp when object was last modified. | [optional] value must conform to RFC-3339 date-time
**score** | decimal.Decimal, int, float,  | decimal.Decimal,  | Result score calculated by a similarity search algorithm (cosine_distance). | [optional] value must be a 32 bit float
**scoreDescriptor** | decimal.Decimal, int, float,  | decimal.Decimal,  | Result score for descriptor containing(now) description and tags. | [optional] value must be a 32 bit float
**scoreExactMatch** | decimal.Decimal, int,  | decimal.Decimal,  | Result score for exact match(id/title). 1/1000. Other scores are multiplied by this. | [optional] value must be a 32 bit integer
**scoreTitle** | decimal.Decimal, int, float,  | decimal.Decimal,  | Result score for object title. | [optional] value must be a 32 bit float
**[tags](#tags)** | list, tuple,  | tuple,  |  | [optional] 
**visualizationUrl** | str,  | str,  | If the object is visualization, this field defines the type of visualization. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# tags

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | List of tags assigned to the object. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

