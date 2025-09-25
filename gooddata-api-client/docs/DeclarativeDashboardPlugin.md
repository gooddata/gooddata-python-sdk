# DeclarativeDashboardPlugin


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Dashboard plugin description. | [optional] 
**id** | **str** | Dashboard plugin object ID. | 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Dashboard plugin object title. | 

## Example

```python
from gooddata_api_client.models.declarative_dashboard_plugin import DeclarativeDashboardPlugin

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDashboardPlugin from a JSON string
declarative_dashboard_plugin_instance = DeclarativeDashboardPlugin.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDashboardPlugin.to_json())

# convert the object into a dict
declarative_dashboard_plugin_dict = declarative_dashboard_plugin_instance.to_dict()
# create an instance of DeclarativeDashboardPlugin from a dict
declarative_dashboard_plugin_from_dict = DeclarativeDashboardPlugin.from_dict(declarative_dashboard_plugin_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


