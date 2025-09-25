# JsonApiWorkspaceOutMetaConfig


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**approximate_count_available** | **bool** | is approximate count enabled - based on type of data-source connected to this workspace | [optional] [default to False]
**data_sampling_available** | **bool** | is sampling enabled - based on type of data-source connected to this workspace | [optional] [default to False]
**show_all_values_on_dates_available** | **bool** | is &#39;show all values&#39; displayed for dates - based on type of data-source connected to this workspace | [optional] [default to False]

## Example

```python
from gooddata_api_client.models.json_api_workspace_out_meta_config import JsonApiWorkspaceOutMetaConfig

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOutMetaConfig from a JSON string
json_api_workspace_out_meta_config_instance = JsonApiWorkspaceOutMetaConfig.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOutMetaConfig.to_json())

# convert the object into a dict
json_api_workspace_out_meta_config_dict = json_api_workspace_out_meta_config_instance.to_dict()
# create an instance of JsonApiWorkspaceOutMetaConfig from a dict
json_api_workspace_out_meta_config_from_dict = JsonApiWorkspaceOutMetaConfig.from_dict(json_api_workspace_out_meta_config_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


