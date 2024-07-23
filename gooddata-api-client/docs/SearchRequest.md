# SearchRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**question** | **str** | Keyword/sentence is input for search. | 
**deep_search** | **bool** | Turn on deep search. If true, content of complex objects will be searched as well, e.g. metrics in visualizations. | [optional]  if omitted the server will use the default value of False
**object_types** | **[str]** | List of object types to search for. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


