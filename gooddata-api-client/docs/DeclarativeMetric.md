# DeclarativeMetric


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**JsonNode**](JsonNode.md) |  | 
**id** | **str** | Metric ID. | 
**title** | **str** | Metric title. | 
**certification** | **str** | Certification status of the entity. | [optional]  if omitted the server will use the default value of "CERTIFIED"
**certification_message** | **str, none_type** | Optional message associated with the certification. | [optional] 
**certified_at** | **str, none_type** | Time when the certification was set. | [optional] 
**certified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Metric description. | [optional] 
**is_hidden** | **bool** | If true, this metric is hidden from AI search results. | [optional] 
**is_hidden_from_kda** | **bool** | If true, this metric is hidden from key drive analysis. | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


