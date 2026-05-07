# JsonApiCustomUserApplicationSettingInAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_name** | **str** |  | 
**content** | **{str: (bool, date, datetime, dict, float, int, list, str, none_type)}** | Free-form JSON content. Maximum supported length is 250000 characters. | 
**workspace_id** | **str, none_type** | Workspace scope for this setting. Must reference an existing workspace the caller has at least VIEW access to. Null means user-level (no workspace scope). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


