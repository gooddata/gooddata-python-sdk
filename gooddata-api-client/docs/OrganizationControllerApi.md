# gooddata_api_client.OrganizationControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_entity_cookie_security_configurations**](OrganizationControllerApi.md#get_entity_cookie_security_configurations) | **GET** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Get CookieSecurityConfiguration
[**get_entity_organizations**](OrganizationControllerApi.md#get_entity_organizations) | **GET** /api/v1/entities/admin/organizations/{id} | Get Organizations
[**patch_entity_cookie_security_configurations**](OrganizationControllerApi.md#patch_entity_cookie_security_configurations) | **PATCH** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Patch CookieSecurityConfiguration
[**patch_entity_organizations**](OrganizationControllerApi.md#patch_entity_organizations) | **PATCH** /api/v1/entities/admin/organizations/{id} | Patch Organization
[**update_entity_cookie_security_configurations**](OrganizationControllerApi.md#update_entity_cookie_security_configurations) | **PUT** /api/v1/entities/admin/cookieSecurityConfigurations/{id} | Put CookieSecurityConfiguration
[**update_entity_organizations**](OrganizationControllerApi.md#update_entity_organizations) | **PUT** /api/v1/entities/admin/organizations/{id} | Put Organization


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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id, filter=filter)
        print("The response of OrganizationControllerApi->get_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->get_entity_cookie_security_configurations: %s\n" % e)
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

# **get_entity_organizations**
> JsonApiOrganizationOutDocument get_entity_organizations(id, filter=filter, include=include, meta_include=meta_include)

Get Organizations

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_out_document import JsonApiOrganizationOutDocument
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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['bootstrapUser,bootstrapUserGroup,identityProvider'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id, filter=filter, include=include, meta_include=meta_include)
        print("The response of OrganizationControllerApi->get_entity_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->get_entity_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_cookie_security_configuration_patch_document = gooddata_api_client.JsonApiCookieSecurityConfigurationPatchDocument() # JsonApiCookieSecurityConfigurationPatchDocument | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document, filter=filter)
        print("The response of OrganizationControllerApi->patch_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->patch_entity_cookie_security_configurations: %s\n" % e)
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

# **patch_entity_organizations**
> JsonApiOrganizationOutDocument patch_entity_organizations(id, json_api_organization_patch_document, filter=filter, include=include)

Patch Organization

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_api_client.models.json_api_organization_patch_document import JsonApiOrganizationPatchDocument
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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_organization_patch_document = gooddata_api_client.JsonApiOrganizationPatchDocument() # JsonApiOrganizationPatchDocument | 
    filter = 'name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['bootstrapUser,bootstrapUserGroup,identityProvider'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document, filter=filter, include=include)
        print("The response of OrganizationControllerApi->patch_entity_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->patch_entity_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_organization_patch_document** | [**JsonApiOrganizationPatchDocument**](JsonApiOrganizationPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_cookie_security_configuration_in_document = gooddata_api_client.JsonApiCookieSecurityConfigurationInDocument() # JsonApiCookieSecurityConfigurationInDocument | 
    filter = 'lastRotation==InstantValue;rotationInterval==DurationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, filter=filter)
        print("The response of OrganizationControllerApi->update_entity_cookie_security_configurations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->update_entity_cookie_security_configurations: %s\n" % e)
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

# **update_entity_organizations**
> JsonApiOrganizationOutDocument update_entity_organizations(id, json_api_organization_in_document, filter=filter, include=include)

Put Organization

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_in_document import JsonApiOrganizationInDocument
from gooddata_api_client.models.json_api_organization_out_document import JsonApiOrganizationOutDocument
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
    api_instance = gooddata_api_client.OrganizationControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_organization_in_document = gooddata_api_client.JsonApiOrganizationInDocument() # JsonApiOrganizationInDocument | 
    filter = 'name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['bootstrapUser,bootstrapUserGroup,identityProvider'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document, filter=filter, include=include)
        print("The response of OrganizationControllerApi->update_entity_organizations:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationControllerApi->update_entity_organizations: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_organization_in_document** | [**JsonApiOrganizationInDocument**](JsonApiOrganizationInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

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

