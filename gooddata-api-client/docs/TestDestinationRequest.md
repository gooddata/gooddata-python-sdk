# TestDestinationRequest

Request body with notification channel destination to test.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**destination** | [**DeclarativeNotificationChannelDestination**](DeclarativeNotificationChannelDestination.md) |  | 
**external_recipients** | [**List[AutomationExternalRecipient]**](AutomationExternalRecipient.md) | External recipients of the test result. | [optional] 

## Example

```python
from gooddata_api_client.models.test_destination_request import TestDestinationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TestDestinationRequest from a JSON string
test_destination_request_instance = TestDestinationRequest.from_json(json)
# print the JSON string representation of the object
print(TestDestinationRequest.to_json())

# convert the object into a dict
test_destination_request_dict = test_destination_request_instance.to_dict()
# create an instance of TestDestinationRequest from a dict
test_destination_request_from_dict = TestDestinationRequest.from_dict(test_destination_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


