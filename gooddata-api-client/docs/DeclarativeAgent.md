# DeclarativeAgent

A declarative form of an AI agent configuration.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of an agent. | 
**ai_knowledge** | **bool** | Whether AI knowledge is enabled. | [optional] 
**available_to_all** | **bool** | Whether the agent is available to all users. | [optional] 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**custom_skills** | **[str]** | List of custom skills when skillsMode is CUSTOM. | [optional] 
**description** | **str** | Description of the agent. | [optional] 
**enabled** | **bool** | Whether the agent is enabled. | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**name** | **str** | Name of the agent. | [optional] 
**personality** | **str** | Personality instructions for the agent. | [optional] 
**skills_mode** | **str** | Skills mode: ALL or CUSTOM. | [optional] 
**user_groups** | [**[DeclarativeUserGroupIdentifier]**](DeclarativeUserGroupIdentifier.md) | User groups this agent is assigned to. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


