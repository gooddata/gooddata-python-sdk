# AacQuery

Query definition.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**fields** | [**{str: (AacQueryFieldsValue,)}**](AacQueryFieldsValue.md) | Query fields map: localId -&gt; field definition (identifier string or structured object). | 
**filter_by** | [**{str: (AacQueryFilter,)}**](AacQueryFilter.md) | Query filters map: localId -&gt; filter definition. | [optional] 
**sort_by** | [**[JsonNode]**](JsonNode.md) | Sorting definitions. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


