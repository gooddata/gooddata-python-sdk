# DependentEntitiesRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifiers** | [**[EntityIdentifier]**](EntityIdentifier.md) |  | 
**relation** | **str** | Entity relation for graph traversal from the entry points. DEPENDENTS returns entities that depend on the entry points. DEPENDENCIES returns entities that the entry points depend on. | [optional]  if omitted the server will use the default value of "DEPENDENTS"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


