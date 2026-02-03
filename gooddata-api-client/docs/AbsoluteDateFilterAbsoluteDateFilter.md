# AbsoluteDateFilterAbsoluteDateFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**_from** | **str** |  | 
**to** | **str** |  | 
**apply_on_result** | **bool** |  | [optional] 
**include_empty_values** | **bool** | If true, rows with undefined (NULL) date values will be included in the result. The filter becomes: (date_condition) OR (date IS NULL). If false or not set, standard behavior applies (NULLs excluded by the date condition). | [optional] 
**local_identifier** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


