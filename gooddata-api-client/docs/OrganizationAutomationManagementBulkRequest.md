# OrganizationAutomationManagementBulkRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**automations** | [**List[OrganizationAutomationIdentifier]**](OrganizationAutomationIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.organization_automation_management_bulk_request import OrganizationAutomationManagementBulkRequest

# TODO update the JSON string below
json = "{}"
# create an instance of OrganizationAutomationManagementBulkRequest from a JSON string
organization_automation_management_bulk_request_instance = OrganizationAutomationManagementBulkRequest.from_json(json)
# print the JSON string representation of the object
print(OrganizationAutomationManagementBulkRequest.to_json())

# convert the object into a dict
organization_automation_management_bulk_request_dict = organization_automation_management_bulk_request_instance.to_dict()
# create an instance of OrganizationAutomationManagementBulkRequest from a dict
organization_automation_management_bulk_request_from_dict = OrganizationAutomationManagementBulkRequest.from_dict(organization_automation_management_bulk_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


