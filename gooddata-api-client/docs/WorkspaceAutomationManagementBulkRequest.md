# WorkspaceAutomationManagementBulkRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**automations** | [**List[WorkspaceAutomationIdentifier]**](WorkspaceAutomationIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.workspace_automation_management_bulk_request import WorkspaceAutomationManagementBulkRequest

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceAutomationManagementBulkRequest from a JSON string
workspace_automation_management_bulk_request_instance = WorkspaceAutomationManagementBulkRequest.from_json(json)
# print the JSON string representation of the object
print(WorkspaceAutomationManagementBulkRequest.to_json())

# convert the object into a dict
workspace_automation_management_bulk_request_dict = workspace_automation_management_bulk_request_instance.to_dict()
# create an instance of WorkspaceAutomationManagementBulkRequest from a dict
workspace_automation_management_bulk_request_from_dict = WorkspaceAutomationManagementBulkRequest.from_dict(workspace_automation_management_bulk_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


