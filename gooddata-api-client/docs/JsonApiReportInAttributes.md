# JsonApiReportInAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Free-form report definition, stored verbatim - not parsed, validated or migrated. Maximum supported length is 250000 characters. | 
**period_end** | **date** | Last day of the reported period, inclusive. | 
**period_start** | **date** | First day of the reported period, inclusive. | 
**title** | **str** |  | 
**are_relations_valid** | **bool** |  | [optional] 
**description** | **str** |  | [optional] 
**tags** | **[str]** |  | [optional] 
**variable_values** | **bool, date, datetime, dict, float, int, list, str, none_type** | Values for the variables declared in the content, keyed by name. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


