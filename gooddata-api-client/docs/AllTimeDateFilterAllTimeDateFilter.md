# AllTimeDateFilterAllTimeDateFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**apply_on_result** | **bool** |  | [optional] 
**empty_value_handling** | **str** | Specifies how rows with empty (null/missing) date values should be handled. INCLUDE means no filtering effect (default), EXCLUDE removes rows with null dates, ONLY keeps only rows with null dates. | [optional]  if omitted the server will use the default value of "INCLUDE"
**granularity** | **str** | Date granularity used to resolve the date attribute label for null value checks. Defaults to DAY if not specified. | [optional]  if omitted the server will use the default value of "DAY"
**local_identifier** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


