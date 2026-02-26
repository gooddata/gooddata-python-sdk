# AbsoluteDateFilterAbsoluteDateFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**_from** | **str** |  | 
**to** | **str** |  | 
**apply_on_result** | **bool** |  | [optional] 
**empty_value_handling** | **str** | Specifies how rows with empty (null/missing) date values should be handled. INCLUDE includes empty dates in addition to the date range restriction, EXCLUDE removes rows with empty dates (default), ONLY keeps only rows with empty dates. | [optional]  if omitted the server will use the default value of "EXCLUDE"
**local_identifier** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


