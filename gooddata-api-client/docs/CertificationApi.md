# gooddata_api_client.CertificationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**set_certification**](CertificationApi.md#set_certification) | **POST** /api/v1/actions/workspaces/{workspaceId}/setCertification | Set Certification


# **set_certification**
> set_certification(workspace_id, set_certification_request)

Set Certification

Set or clear the certification (e.g. CERTIFIED) of a workspace entity. Requires MANAGE permission.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import certification_api
from gooddata_api_client.model.set_certification_request import SetCertificationRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = certification_api.CertificationApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    set_certification_request = SetCertificationRequest(
        id="total-sales",
        message="message_example",
        status="CERTIFIED",
        type="metric",
    ) # SetCertificationRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Set Certification
        api_instance.set_certification(workspace_id, set_certification_request)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CertificationApi->set_certification: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **set_certification_request** | [**SetCertificationRequest**](SetCertificationRequest.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

