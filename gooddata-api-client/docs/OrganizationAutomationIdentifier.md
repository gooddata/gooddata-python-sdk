# OrganizationAutomationIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**workspace_id** | **str** |  | 

## Example

```python
from gooddata_api_client.models.organization_automation_identifier import OrganizationAutomationIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationAutomationIdentifier from a JSON string
organization_automation_identifier_instance = OrganizationAutomationIdentifier.from_json(json)
# print the JSON string representation of the object
print(OrganizationAutomationIdentifier.to_json())

# convert the object into a dict
organization_automation_identifier_dict = organization_automation_identifier_instance.to_dict()
# create an instance of OrganizationAutomationIdentifier from a dict
organization_automation_identifier_from_dict = OrganizationAutomationIdentifier.from_dict(organization_automation_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


