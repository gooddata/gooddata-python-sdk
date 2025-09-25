# JsonApiAutomationOutRelationshipsAutomationResults


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAutomationResultLinkage]**](JsonApiAutomationResultLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_automation_out_relationships_automation_results import JsonApiAutomationOutRelationshipsAutomationResults

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationOutRelationshipsAutomationResults from a JSON string
json_api_automation_out_relationships_automation_results_instance = JsonApiAutomationOutRelationshipsAutomationResults.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationOutRelationshipsAutomationResults.to_json())

# convert the object into a dict
json_api_automation_out_relationships_automation_results_dict = json_api_automation_out_relationships_automation_results_instance.to_dict()
# create an instance of JsonApiAutomationOutRelationshipsAutomationResults from a dict
json_api_automation_out_relationships_automation_results_from_dict = JsonApiAutomationOutRelationshipsAutomationResults.from_dict(json_api_automation_out_relationships_automation_results_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


