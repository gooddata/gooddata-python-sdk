# JsonApiAgentOutListMeta


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**page** | [**PageMetadata**](PageMetadata.md) |  | [optional] 
**restricted** | [**[RestrictedObject]**](RestrictedObject.md) | References withheld from &#x60;included&#x60; because the caller may not view them. Their &#x60;relationships&#x60; entries are kept, so a client can render a placeholder instead of treating the reference as missing. Empty when the caller may view every reference in the payload; absent entirely when no object-level permissions apply to the request. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


