# SimpleMeasureDefinitionMeasure


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**item** | [**AfmObjectIdentifier**](AfmObjectIdentifier.md) |  | 
**aggregation** | **str** | Definition of aggregation type of the measure. | [optional] 
**compute_ratio** | **bool** | If true compute the percentage of given measure values (broken down by AFM attributes) to the total (not broken down). | [optional]  if omitted the server will use the default value of False
**filters** | [**[FilterDefinitionForSimpleMeasure]**](FilterDefinitionForSimpleMeasure.md) | Measure can be filtered by attribute filters with the same interface as ones for global AFM. Note that only one DateFilter is allowed. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


