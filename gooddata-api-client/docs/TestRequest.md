# TestRequest

A request containing all information for testing existing data source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** | Id for client based authentication for data sources which supports it. | [optional] 
**client_secret** | **str** | Secret for client based authentication for data sources which supports it. | [optional] 
**parameters** | [**List[DataSourceParameter]**](DataSourceParameter.md) |  | [optional] 
**password** | **str** | Database user password. | [optional] 
**private_key** | **str** | Private key for data sources which supports key-pair authentication. | [optional] 
**private_key_passphrase** | **str** | Passphrase for a encrypted version of a private key. | [optional] 
**var_schema** | **str** | Database schema. | [optional] 
**token** | **str** | Secret for token based authentication for data sources which supports it. | [optional] 
**url** | **str** | URL to database in JDBC format, where test should connect to. | [optional] 
**username** | **str** | Database user name. | [optional] 

## Example

```python
from gooddata_api_client.models.test_request import TestRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TestRequest from a JSON string
test_request_instance = TestRequest.from_json(json)
# print the JSON string representation of the object
print(TestRequest.to_json())

# convert the object into a dict
test_request_dict = test_request_instance.to_dict()
# create an instance of TestRequest from a dict
test_request_from_dict = TestRequest.from_dict(test_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


