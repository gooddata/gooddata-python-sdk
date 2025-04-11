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
> JsonApiCookieSecurityConfigurationOutDocument get_entity_cookie_security_configurations(id)

Get CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get CookieSecurityConfiguration
        api_response = api_instance.get_entity_cookie_security_configurations(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiOrganizationOutDocument get_entity_organizations(id)

Get Organizations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=permissions,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

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
> JsonApiCookieSecurityConfigurationOutDocument patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document)

Patch CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from gooddata_api_client.model.json_api_cookie_security_configuration_patch_document import JsonApiCookieSecurityConfigurationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_cookie_security_configuration_patch_document = JsonApiCookieSecurityConfigurationPatchDocument(
        data=JsonApiCookieSecurityConfigurationPatch(
            attributes=JsonApiCookieSecurityConfigurationInAttributes(
                last_rotation=dateutil_parser('1970-01-01T00:00:00.00Z'),
                rotation_interval="P30D",
            ),
            id="id1",
            type="cookieSecurityConfiguration",
        ),
    ) # JsonApiCookieSecurityConfigurationPatchDocument | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->patch_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch CookieSecurityConfiguration
        api_response = api_instance.patch_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiOrganizationOutDocument patch_entity_organizations(id, json_api_organization_patch_document)

Patch Organization

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_api_client.model.json_api_organization_patch_document import JsonApiOrganizationPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_patch_document = JsonApiOrganizationPatchDocument(
        data=JsonApiOrganizationPatch(
            attributes=JsonApiOrganizationInAttributes(
                allowed_origins=[
                    "allowed_origins_example",
                ],
                early_access="early_access_example",
                early_access_values=[
                    "early_access_values_example",
                ],
                hostname="hostname_example",
                name="name_example",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes={
                    "key": "key_example",
                },
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example",
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
            ),
            id="id1",
            type="organization",
        ),
    ) # JsonApiOrganizationPatchDocument | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->patch_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->patch_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_patch_document** | [**JsonApiOrganizationPatchDocument**](JsonApiOrganizationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

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
> JsonApiCookieSecurityConfigurationOutDocument update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)

Put CookieSecurityConfiguration

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_cookie_security_configuration_in_document import JsonApiCookieSecurityConfigurationInDocument
from gooddata_api_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_cookie_security_configuration_in_document = JsonApiCookieSecurityConfigurationInDocument(
        data=JsonApiCookieSecurityConfigurationIn(
            attributes=JsonApiCookieSecurityConfigurationInAttributes(
                last_rotation=dateutil_parser('1970-01-01T00:00:00.00Z'),
                rotation_interval="P30D",
            ),
            id="id1",
            type="cookieSecurityConfiguration",
        ),
    ) # JsonApiCookieSecurityConfigurationInDocument | 
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put CookieSecurityConfiguration
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
> JsonApiOrganizationOutDocument update_entity_organizations(id, json_api_organization_in_document)

Put Organization

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_controller_api
from gooddata_api_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from gooddata_api_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_in_document = JsonApiOrganizationInDocument(
        data=JsonApiOrganizationIn(
            attributes=JsonApiOrganizationInAttributes(
                allowed_origins=[
                    "allowed_origins_example",
                ],
                early_access="early_access_example",
                early_access_values=[
                    "early_access_values_example",
                ],
                hostname="hostname_example",
                name="name_example",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
                oauth_custom_auth_attributes={
                    "key": "key_example",
                },
                oauth_custom_scopes=[
                    "oauth_custom_scopes_example",
                ],
                oauth_issuer_id="myOidcProvider",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_subject_id_claim="oid",
            ),
            id="id1",
            type="organization",
        ),
    ) # JsonApiOrganizationInDocument | 
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_in_document** | [**JsonApiOrganizationInDocument**](JsonApiOrganizationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

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

