# JsonApiAutomationInRelationshipsExportDefinitions


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiExportDefinitionLinkage]**](JsonApiExportDefinitionLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_relationships_export_definitions import JsonApiAutomationInRelationshipsExportDefinitions

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInRelationshipsExportDefinitions from a JSON string
json_api_automation_in_relationships_export_definitions_instance = JsonApiAutomationInRelationshipsExportDefinitions.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInRelationshipsExportDefinitions.to_json())

# convert the object into a dict
json_api_automation_in_relationships_export_definitions_dict = json_api_automation_in_relationships_export_definitions_instance.to_dict()
# create an instance of JsonApiAutomationInRelationshipsExportDefinitions from a dict
json_api_automation_in_relationships_export_definitions_from_dict = JsonApiAutomationInRelationshipsExportDefinitions.from_dict(json_api_automation_in_relationships_export_definitions_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


