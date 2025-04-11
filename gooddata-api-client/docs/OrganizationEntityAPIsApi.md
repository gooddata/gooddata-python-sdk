# gooddata_api_client.OrganizationEntityAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_organization_settings**](OrganizationEntityAPIsApi.md#create_entity_organization_settings) | **POST** /api/v1/entities/organizationSettings | Post Organization Setting entities
[**delete_entity_organization_settings**](OrganizationEntityAPIsApi.md#delete_entity_organization_settings) | **DELETE** /api/v1/entities/organizationSettings/{id} | Delete Organization entity
[**get_all_entities_organization_settings**](OrganizationEntityAPIsApi.md#get_all_entities_organization_settings) | **GET** /api/v1/entities/organizationSettings | Get Organization entities
[**get_entity_organization_settings**](OrganizationEntityAPIsApi.md#get_entity_organization_settings) | **GET** /api/v1/entities/organizationSettings/{id} | Get Organization entity
[**get_entity_organizations**](OrganizationEntityAPIsApi.md#get_entity_organizations) | **GET** /api/v1/entities/admin/organizations/{id} | Get Organizations
[**get_organization**](OrganizationEntityAPIsApi.md#get_organization) | **GET** /api/v1/entities/organization | Get current organization info
[**patch_entity_organization_settings**](OrganizationEntityAPIsApi.md#patch_entity_organization_settings) | **PATCH** /api/v1/entities/organizationSettings/{id} | Patch Organization entity
[**patch_entity_organizations**](OrganizationEntityAPIsApi.md#patch_entity_organizations) | **PATCH** /api/v1/entities/admin/organizations/{id} | Patch Organization
[**update_entity_organization_settings**](OrganizationEntityAPIsApi.md#update_entity_organization_settings) | **PUT** /api/v1/entities/organizationSettings/{id} | Put Organization entity
[**update_entity_organizations**](OrganizationEntityAPIsApi.md#update_entity_organizations) | **PUT** /api/v1/entities/admin/organizations/{id} | Put Organization


# **create_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument create_entity_organization_settings(json_api_organization_setting_in_document)

Post Organization Setting entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    json_api_organization_setting_in_document = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingInDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Organization Setting entities
        api_response = api_instance.create_entity_organization_settings(json_api_organization_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->create_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_organization_setting_in_document** | [**JsonApiOrganizationSettingInDocument**](JsonApiOrganizationSettingInDocument.md)|  |

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

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

# **delete_entity_organization_settings**
> delete_entity_organization_settings(id)

Delete Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Organization entity
        api_instance.delete_entity_organization_settings(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->delete_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Organization entity
        api_instance.delete_entity_organization_settings(id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->delete_entity_organization_settings: %s\n" % e)
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

# **get_all_entities_organization_settings**
> JsonApiOrganizationSettingOutList get_all_entities_organization_settings()

Get Organization entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from gooddata_api_client.model.json_api_organization_setting_out_list import JsonApiOrganizationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    filter = "filter=content==JsonNodeValue;type==SettingTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organization entities
        api_response = api_instance.get_all_entities_organization_settings(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->get_all_entities_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiOrganizationSettingOutList**](JsonApiOrganizationSettingOutList.md)

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

# **get_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument get_entity_organization_settings(id)

Get Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->get_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->get_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

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
from gooddata_api_client.api import organization_entity_apis_api
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
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
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
        print("Exception when calling OrganizationEntityAPIsApi->get_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Organizations
        api_response = api_instance.get_entity_organizations(id, filter=filter, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->get_entity_organizations: %s\n" % e)
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

# **get_organization**
> get_organization()

Get current organization info

Gets a basic information about organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    meta_include = [
        "metaInclude=permissions",
    ] # [str] | Return list of permissions available to logged user. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get current organization info
        api_instance.get_organization(meta_include=meta_include)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->get_organization: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **meta_include** | **[str]**| Return list of permissions available to logged user. | [optional]

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
**302** | Redirect to entity URI. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument patch_entity_organization_settings(id, json_api_organization_setting_patch_document)

Patch Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from gooddata_api_client.model.json_api_organization_setting_patch_document import JsonApiOrganizationSettingPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_setting_patch_document = JsonApiOrganizationSettingPatchDocument(
        data=JsonApiOrganizationSettingPatch(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingPatchDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(id, json_api_organization_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->patch_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(id, json_api_organization_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->patch_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_setting_patch_document** | [**JsonApiOrganizationSettingPatchDocument**](JsonApiOrganizationSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

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
from gooddata_api_client.api import organization_entity_apis_api
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
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
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
        print("Exception when calling OrganizationEntityAPIsApi->patch_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Organization
        api_response = api_instance.patch_entity_organizations(id, json_api_organization_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->patch_entity_organizations: %s\n" % e)
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

# **update_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument update_entity_organization_settings(id, json_api_organization_setting_in_document)

Put Organization entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import organization_entity_apis_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_organization_setting_in_document = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    ) # JsonApiOrganizationSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingTypeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(id, json_api_organization_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->update_entity_organization_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(id, json_api_organization_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->update_entity_organization_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_setting_in_document** | [**JsonApiOrganizationSettingInDocument**](JsonApiOrganizationSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiOrganizationSettingOutDocument**](JsonApiOrganizationSettingOutDocument.md)

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
from gooddata_api_client.api import organization_entity_apis_api
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
    api_instance = organization_entity_apis_api.OrganizationEntityAPIsApi(api_client)
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
        print("Exception when calling OrganizationEntityAPIsApi->update_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Organization
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationEntityAPIsApi->update_entity_organizations: %s\n" % e)
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

