# JsonApiPublisherDocumentInAttributesPeriod

The period the document covers, absolute or relative to today.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Type of the period. | defaults to "relative"
**_from** | **int** | Start of the period, in units relative to the current one. | [optional] 
**granularity** | **str** | Date granularity of the period. | [optional] 
**to** | **int** | End of the period, in units relative to the current one. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


