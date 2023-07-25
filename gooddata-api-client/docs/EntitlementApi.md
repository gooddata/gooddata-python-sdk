# gooddata_api_client.EntitlementApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_entities_entitlements**](EntitlementApi.md#get_all_entities_entitlements) | **GET** /api/v1/entities/entitlements | Get Entitlements
[**get_entity_entitlements**](EntitlementApi.md#get_entity_entitlements) | **GET** /api/v1/entities/entitlements/{id} | Get Entitlement
[**resolve_all_entitlements**](EntitlementApi.md#resolve_all_entitlements) | **GET** /api/v1/actions/resolveEntitlements | Values for all public entitlements.
[**resolve_requested_entitlements**](EntitlementApi.md#resolve_requested_entitlements) | **POST** /api/v1/actions/resolveEntitlements | Values for requested public entitlements.


# **get_all_entities_entitlements**
> JsonApiEntitlementOutList get_all_entities_entitlements()

Get Entitlements

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entitlement_api
from gooddata_api_client.model.json_api_entitlement_out_list import JsonApiEntitlementOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entitlement_api.EntitlementApi(api_client)
    filter = "filter=value==someString;expiry==LocalDateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Entitlements
        api_response = api_instance.get_all_entities_entitlements(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitlementApi->get_all_entities_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiEntitlementOutList**](JsonApiEntitlementOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_entitlements**
> JsonApiEntitlementOutDocument get_entity_entitlements(id)

Get Entitlement

Space of the shared interest

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entitlement_api
from gooddata_api_client.model.json_api_entitlement_out_document import JsonApiEntitlementOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entitlement_api.EntitlementApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=value==someString;expiry==LocalDateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitlementApi->get_entity_entitlements: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitlementApi->get_entity_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiEntitlementOutDocument**](JsonApiEntitlementOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_entitlements**
> [ApiEntitlement] resolve_all_entitlements()

Values for all public entitlements.

Resolves values of available entitlements for the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entitlement_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entitlement_api.EntitlementApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all public entitlements.
        api_response = api_instance.resolve_all_entitlements()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitlementApi->resolve_all_entitlements: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_requested_entitlements**
> [ApiEntitlement] resolve_requested_entitlements(entitlements_request)

Values for requested public entitlements.

Resolves values for requested entitlements in the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import entitlement_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from gooddata_api_client.model.entitlements_request import EntitlementsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = entitlement_api.EntitlementApi(api_client)
    entitlements_request = EntitlementsRequest(
        entitlements_name=[
            "CacheStrategy",
        ],
    ) # EntitlementsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for requested public entitlements.
        api_response = api_instance.resolve_requested_entitlements(entitlements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling EntitlementApi->resolve_requested_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entitlements_request** | [**EntitlementsRequest**](EntitlementsRequest.md)|  |

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

