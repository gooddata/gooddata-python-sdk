# DeclarativeWorkspaceModel

A declarative form of a model and analytics for a workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytics** | [**DeclarativeAnalyticsLayer**](DeclarativeAnalyticsLayer.md) |  | [optional] 
**ldm** | [**DeclarativeLdm**](DeclarativeLdm.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_workspace_model import DeclarativeWorkspaceModel

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceModel from a JSON string
declarative_workspace_model_instance = DeclarativeWorkspaceModel.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceModel.to_json())

# convert the object into a dict
declarative_workspace_model_dict = declarative_workspace_model_instance.to_dict()
# create an instance of DeclarativeWorkspaceModel from a dict
declarative_workspace_model_from_dict = DeclarativeWorkspaceModel.from_dict(declarative_workspace_model_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


