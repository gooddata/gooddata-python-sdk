# JsonApiFilterContextOutIncludes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**meta** | [**JsonApiAttributeHierarchyOutMeta**](JsonApiAttributeHierarchyOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiLabelOutRelationships**](JsonApiLabelOutRelationships.md) |  | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 
**attributes** | [**JsonApiLabelOutAttributes**](JsonApiLabelOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | [optional] 
**type** | **str** | Object type | [optional]  if omitted the server will use the default value of "label"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


