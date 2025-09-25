# JsonApiWorkspaceOutMetaDataModel


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_count** | **int** | include the number of dataset of each workspace | 

## Example

```python
from gooddata_api_client.models.json_api_workspace_out_meta_data_model import JsonApiWorkspaceOutMetaDataModel

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceOutMetaDataModel from a JSON string
json_api_workspace_out_meta_data_model_instance = JsonApiWorkspaceOutMetaDataModel.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceOutMetaDataModel.to_json())

# convert the object into a dict
json_api_workspace_out_meta_data_model_dict = json_api_workspace_out_meta_data_model_instance.to_dict()
# create an instance of JsonApiWorkspaceOutMetaDataModel from a dict
json_api_workspace_out_meta_data_model_from_dict = JsonApiWorkspaceOutMetaDataModel.from_dict(json_api_workspace_out_meta_data_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


