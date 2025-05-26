# VisibleFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_all_time_date_filter** | **bool** | Indicates if the filter is an all-time date filter. Such a filter is not included in report computation, so there is no filter with the same &#39;localIdentifier&#39; to be found. In such cases, this flag is used to inform the server to not search for the filter in the definitions and include it anyways. | [optional]  if omitted the server will use the default value of False
**local_identifier** | **str** |  | [optional] 
**title** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


