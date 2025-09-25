# JsonApiAutomationInRelationshipsRecipients


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiUserLinkage]**](JsonApiUserLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_relationships_recipients import JsonApiAutomationInRelationshipsRecipients

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInRelationshipsRecipients from a JSON string
json_api_automation_in_relationships_recipients_instance = JsonApiAutomationInRelationshipsRecipients.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInRelationshipsRecipients.to_json())

# convert the object into a dict
json_api_automation_in_relationships_recipients_dict = json_api_automation_in_relationships_recipients_instance.to_dict()
# create an instance of JsonApiAutomationInRelationshipsRecipients from a dict
json_api_automation_in_relationships_recipients_from_dict = JsonApiAutomationInRelationshipsRecipients.from_dict(json_api_automation_in_relationships_recipients_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


