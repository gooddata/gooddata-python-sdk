# DeclarativeReport


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**JsonNode**](JsonNode.md) |  | 
**id** | **str** | Report ID. | 
**period_end** | **date** | Last day of the reported period, inclusive. | 
**period_start** | **date** | First day of the reported period, inclusive. | 
**title** | **str** | Report title. | 
**description** | **str** | Report description. | [optional] 
**tags** | **[str]** |  | [optional] 
**variable_values** | **{str: (str,)}** | Values for the variables declared in the content, keyed by name. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


