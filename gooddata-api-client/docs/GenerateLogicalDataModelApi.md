# gooddata_api_client.GenerateLogicalDataModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_logical_model**](GenerateLogicalDataModelApi.md#generate_logical_model) | **POST** /api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate logical data model (LDM) from physical data model (PDM)


# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate logical data model (LDM) from physical data model (PDM)

Generate logical data model (LDM) from physical data model (PDM) stored in data source.

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_model import DeclarativeModel
from gooddata_api_client.models.generate_ldm_request import GenerateLdmRequest
from gooddata_api_client.rest import ApiException
from pprint import pprint

# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = gooddata_api_client.GenerateLogicalDataModelApi(api_client)
    data_source_id = 'data_source_id_example' # str | 
    generate_ldm_request = gooddata_api_client.GenerateLdmRequest() # GenerateLdmRequest | 

    try:
        # Generate logical data model (LDM) from physical data model (PDM)
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        print("The response of GenerateLogicalDataModelApi->generate_logical_model:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling GenerateLogicalDataModelApi->generate_logical_model: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  | 
 **generate_ldm_request** | [**GenerateLdmRequest**](GenerateLdmRequest.md)|  | 

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json

### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | LDM generated successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

