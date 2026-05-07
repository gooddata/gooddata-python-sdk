# ObjectStorageInfo

Descriptor of a registered ObjectStorage. Provider credentials are stripped — only fields useful for identifying the storage are returned.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Human-readable name. Use this as &#x60;sourceStorageName&#x60; in CreatePipeTable, or pass &#x60;storageId&#x60; to ProvisionDatabase.storageIds. | 
**storage_config** | **{str: (str,)}** | Provider-specific descriptors (e.g. bucket, region, endpoint, container). Credential references (any keys ending in &#x60;_env&#x60;) are stripped server-side. | 
**storage_id** | **str** | Stable identifier of the storage configuration (UUID). | 
**storage_type** | **str** | Provider type. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


