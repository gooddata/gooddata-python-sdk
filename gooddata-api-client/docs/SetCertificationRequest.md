# SetCertificationRequest

Request to set or clear the certification of a workspace entity.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | ID of the entity. | 
**type** | **str** | Type of the entity. | 
**message** | **str, none_type** | Optional message associated with the certification. | [optional] 
**status** | **str, none_type** | Certification status of the entity. | [optional]  if omitted the server will use the default value of "CERTIFIED"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


