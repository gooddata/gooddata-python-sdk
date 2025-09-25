# gooddata_api_client.CookieSecurityConfigurationApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_entity_cookie_security_configurations**](CookieSecurityConfigurationApi.md#get_entity_cookie_security_configurations) | **GET** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Get CookieSecurityConfiguration
[**patch_entity_cookie_security_configurations**](CookieSecurityConfigurationApi.md#patch_entity_cookie_security_configurations) | **PATCH** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Patch CookieSecurityConfiguration
[**update_entity_cookie_security_configurations**](CookieSecurityConfigurationApi.md#update_entity_cookie_security_configurations) | **PUT** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Put CookieSecurityConfiguration


# **get_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument get_entity_cookie_security_configurations(id, filter=filter)

Get CookieSecurityConfiguration

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
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
    api_instance = gooddata_api_client.CookieSecurityConfigurationApi(api_client)
    id = 'id_example' # str | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id, filter=filter)
        print("The response of CookieSecurityConfigurationApi->get_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CookieSecurityConfigurationApi->get_entity_cookie_security_configurations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

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

# **patch_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document, filter=filter)

Patch CookieSecurityConfiguration

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from gooddata_api_client.models.json_api_cookie_security_configuration_patch_document import JsonApiCookieSecurityConfigurationPatchDocument
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
    api_instance = gooddata_api_client.CookieSecurityConfigurationApi(api_client)
    id = 'id_example' # str | 
    json_api_cookie_security_configuration_patch_document = gooddata_api_client.JsonApiCookieSecurityConfigurationPatchDocument() # JsonApiCookieSecurityConfigurationPatchDocument | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document, filter=filter)
        print("The response of CookieSecurityConfigurationApi->patch_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CookieSecurityConfigurationApi->patch_entity_cookie_security_configurations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_cookie_security_configuration_patch_document** | [**JsonApiCookieSecurityConfigurationPatchDocument**](JsonApiCookieSecurityConfigurationPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

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

# **update_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, filter=filter)

Put CookieSecurityConfiguration

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_cookie_security_configuration_in_document import JsonApiCookieSecurityConfigurationInDocument
from gooddata_api_client.models.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
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
    api_instance = gooddata_api_client.CookieSecurityConfigurationApi(api_client)
    id = 'id_example' # str | 
    json_api_cookie_security_configuration_in_document = gooddata_api_client.JsonApiCookieSecurityConfigurationInDocument() # JsonApiCookieSecurityConfigurationInDocument | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, filter=filter)
        print("The response of CookieSecurityConfigurationApi->update_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling CookieSecurityConfigurationApi->update_entity_cookie_security_configurations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_cookie_security_configuration_in_document** | [**JsonApiCookieSecurityConfigurationInDocument**](JsonApiCookieSecurityConfigurationInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

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

