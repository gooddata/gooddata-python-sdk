# UserContext

User context with ambient UI state (view) and explicitly referenced objects.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**active_object** | [**ActiveObjectIdentification**](ActiveObjectIdentification.md) |  | [optional] 
**referenced_objects** | [**[ObjectReferenceGroup]**](ObjectReferenceGroup.md) | Groups of explicitly referenced objects, each optionally scoped by a context (e.g. a dashboard context with widget references). | [optional] 
**view** | [**UIContext**](UIContext.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


