# JsonApiFactOut

JSON:API representation of fact entity.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | defaults to "fact"
**attributes** | [**JsonApiFactOutAttributes**](JsonApiFactOutAttributes.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiFactOutRelationships**](JsonApiFactOutRelationships.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


