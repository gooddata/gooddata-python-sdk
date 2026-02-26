# JsonApiAnalyticalDashboardOutAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Free-form JSON content. Maximum supported length is 250000 characters. | 
**are_relations_valid** | **bool** |  | [optional] 
**certification** | **str** | Certification status of the entity. | [optional]  if omitted the server will use the default value of "CERTIFIED"
**certification_message** | **str, none_type** | Optional message associated with the certification. | [optional] 
**certified_at** | **datetime, none_type** | Time when the certification was set. | [optional] 
**created_at** | **datetime, none_type** | Time of the entity creation. | [optional] 
**description** | **str** |  | [optional] 
**modified_at** | **datetime, none_type** | Time of the last entity modification. | [optional] 
**summary** | **str** | AI-generated summary of the dashboard content | [optional] 
**tags** | **[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


