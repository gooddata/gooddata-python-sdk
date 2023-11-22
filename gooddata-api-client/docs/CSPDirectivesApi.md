# gooddata_api_client.CSPDirectivesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_csp_directives**](CSPDirectivesApi.md#create_entity_csp_directives) | **POST** /api/v1/entities/cspDirectives | Post CSP Directives
[**delete_entity_csp_directives**](CSPDirectivesApi.md#delete_entity_csp_directives) | **DELETE** /api/v1/entities/cspDirectives/{id} | Delete CSP Directives
[**get_all_entities_csp_directives**](CSPDirectivesApi.md#get_all_entities_csp_directives) | **GET** /api/v1/entities/cspDirectives | Get CSP Directives
[**get_entity_csp_directives**](CSPDirectivesApi.md#get_entity_csp_directives) | **GET** /api/v1/entities/cspDirectives/{id} | Get CSP Directives
[**patch_entity_csp_directives**](CSPDirectivesApi.md#patch_entity_csp_directives) | **PATCH** /api/v1/entities/cspDirectives/{id} | Patch CSP Directives
[**update_entity_csp_directives**](CSPDirectivesApi.md#update_entity_csp_directives) | **PUT** /api/v1/entities/cspDirectives/{id} | Put CSP Directives


# **create_entity_csp_directives**
> JsonApiCspDirectiveOutDocument create_entity_csp_directives(json_api_csp_directive_in_document)

Post CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    json_api_csp_directive_in_document = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=JsonApiCspDirectiveInAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectiveInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post CSP Directives
        api_response = api_instance.create_entity_csp_directives(json_api_csp_directive_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->create_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  |

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_csp_directives**
> delete_entity_csp_directives(id)

Delete CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->delete_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->delete_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Successfully deleted |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_all_entities_csp_directives**
> JsonApiCspDirectiveOutList get_all_entities_csp_directives()

Get CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from gooddata_api_client.model.json_api_csp_directive_out_list import JsonApiCspDirectiveOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CSP Directives
        api_response = api_instance.get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->get_all_entities_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]

### Return type

[**JsonApiCspDirectiveOutList**](JsonApiCspDirectiveOutList.md)

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

# **get_entity_csp_directives**
> JsonApiCspDirectiveOutDocument get_entity_csp_directives(id)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->get_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->get_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

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

# **patch_entity_csp_directives**
> JsonApiCspDirectiveOutDocument patch_entity_csp_directives(id, json_api_csp_directive_patch_document)

Patch CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_csp_directive_patch_document = JsonApiCspDirectivePatchDocument(
        data=JsonApiCspDirectivePatch(
            attributes=JsonApiCspDirectivePatchAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectivePatchDocument | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->patch_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->patch_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_csp_directive_patch_document** | [**JsonApiCspDirectivePatchDocument**](JsonApiCspDirectivePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_csp_directives**
> JsonApiCspDirectiveOutDocument update_entity_csp_directives(id, json_api_csp_directive_in_document)

Put CSP Directives

 Context Security Police Directive

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import csp_directives_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = csp_directives_api.CSPDirectivesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_csp_directive_in_document = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=JsonApiCspDirectiveInAttributes(
                sources=[
                    "sources_example",
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    ) # JsonApiCspDirectiveInDocument | 
    filter = "filter=sources==v1,v2,v3" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->update_entity_csp_directives: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling CSPDirectivesApi->update_entity_csp_directives: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_csp_directive_in_document** | [**JsonApiCspDirectiveInDocument**](JsonApiCspDirectiveInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCspDirectiveOutDocument**](JsonApiCspDirectiveOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/vnd.gooddata.api+json
 - **Accept**: application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

