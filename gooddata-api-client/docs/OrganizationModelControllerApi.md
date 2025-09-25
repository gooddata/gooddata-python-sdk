# gooddata_api_client.OrganizationModelControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_color_palettes**](OrganizationModelControllerApi.md#create_entity_color_palettes) | **POST** /api/v1/entities/colorPalettes | Post Color Pallettes
[**create_entity_csp_directives**](OrganizationModelControllerApi.md#create_entity_csp_directives) | **POST** /api/v1/entities/cspDirectives | Post CSP Directives
[**create_entity_data_sources**](OrganizationModelControllerApi.md#create_entity_data_sources) | **POST** /api/v1/entities/dataSources | Post Data Sources
[**create_entity_export_templates**](OrganizationModelControllerApi.md#create_entity_export_templates) | **POST** /api/v1/entities/exportTemplates | Post Export Template entities
[**create_entity_identity_providers**](OrganizationModelControllerApi.md#create_entity_identity_providers) | **POST** /api/v1/entities/identityProviders | Post Identity Providers
[**create_entity_jwks**](OrganizationModelControllerApi.md#create_entity_jwks) | **POST** /api/v1/entities/jwks | Post Jwks
[**create_entity_llm_endpoints**](OrganizationModelControllerApi.md#create_entity_llm_endpoints) | **POST** /api/v1/entities/llmEndpoints | Post LLM endpoint entities
[**create_entity_notification_channels**](OrganizationModelControllerApi.md#create_entity_notification_channels) | **POST** /api/v1/entities/notificationChannels | Post Notification Channel entities
[**create_entity_organization_settings**](OrganizationModelControllerApi.md#create_entity_organization_settings) | **POST** /api/v1/entities/organizationSettings | Post Organization Setting entities
[**create_entity_themes**](OrganizationModelControllerApi.md#create_entity_themes) | **POST** /api/v1/entities/themes | Post Theming
[**create_entity_user_groups**](OrganizationModelControllerApi.md#create_entity_user_groups) | **POST** /api/v1/entities/userGroups | Post User Group entities
[**create_entity_users**](OrganizationModelControllerApi.md#create_entity_users) | **POST** /api/v1/entities/users | Post User entities
[**create_entity_workspaces**](OrganizationModelControllerApi.md#create_entity_workspaces) | **POST** /api/v1/entities/workspaces | Post Workspace entities
[**delete_entity_color_palettes**](OrganizationModelControllerApi.md#delete_entity_color_palettes) | **DELETE** /api/v1/entities/colorPalettes/{id} | Delete a Color Pallette
[**delete_entity_csp_directives**](OrganizationModelControllerApi.md#delete_entity_csp_directives) | **DELETE** /api/v1/entities/cspDirectives/{id} | Delete CSP Directives
[**delete_entity_data_sources**](OrganizationModelControllerApi.md#delete_entity_data_sources) | **DELETE** /api/v1/entities/dataSources/{id} | Delete Data Source entity
[**delete_entity_export_templates**](OrganizationModelControllerApi.md#delete_entity_export_templates) | **DELETE** /api/v1/entities/exportTemplates/{id} | Delete Export Template entity
[**delete_entity_identity_providers**](OrganizationModelControllerApi.md#delete_entity_identity_providers) | **DELETE** /api/v1/entities/identityProviders/{id} | Delete Identity Provider
[**delete_entity_jwks**](OrganizationModelControllerApi.md#delete_entity_jwks) | **DELETE** /api/v1/entities/jwks/{id} | Delete Jwk
[**delete_entity_llm_endpoints**](OrganizationModelControllerApi.md#delete_entity_llm_endpoints) | **DELETE** /api/v1/entities/llmEndpoints/{id} | 
[**delete_entity_notification_channels**](OrganizationModelControllerApi.md#delete_entity_notification_channels) | **DELETE** /api/v1/entities/notificationChannels/{id} | Delete Notification Channel entity
[**delete_entity_organization_settings**](OrganizationModelControllerApi.md#delete_entity_organization_settings) | **DELETE** /api/v1/entities/organizationSettings/{id} | Delete Organization entity
[**delete_entity_themes**](OrganizationModelControllerApi.md#delete_entity_themes) | **DELETE** /api/v1/entities/themes/{id} | Delete Theming
[**delete_entity_user_groups**](OrganizationModelControllerApi.md#delete_entity_user_groups) | **DELETE** /api/v1/entities/userGroups/{id} | Delete UserGroup entity
[**delete_entity_users**](OrganizationModelControllerApi.md#delete_entity_users) | **DELETE** /api/v1/entities/users/{id} | Delete User entity
[**delete_entity_workspaces**](OrganizationModelControllerApi.md#delete_entity_workspaces) | **DELETE** /api/v1/entities/workspaces/{id} | Delete Workspace entity
[**get_all_entities_color_palettes**](OrganizationModelControllerApi.md#get_all_entities_color_palettes) | **GET** /api/v1/entities/colorPalettes | Get all Color Pallettes
[**get_all_entities_csp_directives**](OrganizationModelControllerApi.md#get_all_entities_csp_directives) | **GET** /api/v1/entities/cspDirectives | Get CSP Directives
[**get_all_entities_data_source_identifiers**](OrganizationModelControllerApi.md#get_all_entities_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers | Get all Data Source Identifiers
[**get_all_entities_data_sources**](OrganizationModelControllerApi.md#get_all_entities_data_sources) | **GET** /api/v1/entities/dataSources | Get Data Source entities
[**get_all_entities_entitlements**](OrganizationModelControllerApi.md#get_all_entities_entitlements) | **GET** /api/v1/entities/entitlements | Get Entitlements
[**get_all_entities_export_templates**](OrganizationModelControllerApi.md#get_all_entities_export_templates) | **GET** /api/v1/entities/exportTemplates | GET all Export Template entities
[**get_all_entities_identity_providers**](OrganizationModelControllerApi.md#get_all_entities_identity_providers) | **GET** /api/v1/entities/identityProviders | Get all Identity Providers
[**get_all_entities_jwks**](OrganizationModelControllerApi.md#get_all_entities_jwks) | **GET** /api/v1/entities/jwks | Get all Jwks
[**get_all_entities_llm_endpoints**](OrganizationModelControllerApi.md#get_all_entities_llm_endpoints) | **GET** /api/v1/entities/llmEndpoints | Get all LLM endpoint entities
[**get_all_entities_notification_channel_identifiers**](OrganizationModelControllerApi.md#get_all_entities_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers | 
[**get_all_entities_notification_channels**](OrganizationModelControllerApi.md#get_all_entities_notification_channels) | **GET** /api/v1/entities/notificationChannels | Get all Notification Channel entities
[**get_all_entities_organization_settings**](OrganizationModelControllerApi.md#get_all_entities_organization_settings) | **GET** /api/v1/entities/organizationSettings | Get Organization entities
[**get_all_entities_themes**](OrganizationModelControllerApi.md#get_all_entities_themes) | **GET** /api/v1/entities/themes | Get all Theming entities
[**get_all_entities_user_groups**](OrganizationModelControllerApi.md#get_all_entities_user_groups) | **GET** /api/v1/entities/userGroups | Get UserGroup entities
[**get_all_entities_user_identifiers**](OrganizationModelControllerApi.md#get_all_entities_user_identifiers) | **GET** /api/v1/entities/userIdentifiers | Get UserIdentifier entities
[**get_all_entities_users**](OrganizationModelControllerApi.md#get_all_entities_users) | **GET** /api/v1/entities/users | Get User entities
[**get_all_entities_workspaces**](OrganizationModelControllerApi.md#get_all_entities_workspaces) | **GET** /api/v1/entities/workspaces | Get Workspace entities
[**get_entity_color_palettes**](OrganizationModelControllerApi.md#get_entity_color_palettes) | **GET** /api/v1/entities/colorPalettes/{id} | Get Color Pallette
[**get_entity_csp_directives**](OrganizationModelControllerApi.md#get_entity_csp_directives) | **GET** /api/v1/entities/cspDirectives/{id} | Get CSP Directives
[**get_entity_data_source_identifiers**](OrganizationModelControllerApi.md#get_entity_data_source_identifiers) | **GET** /api/v1/entities/dataSourceIdentifiers/{id} | Get Data Source Identifier
[**get_entity_data_sources**](OrganizationModelControllerApi.md#get_entity_data_sources) | **GET** /api/v1/entities/dataSources/{id} | Get Data Source entity
[**get_entity_entitlements**](OrganizationModelControllerApi.md#get_entity_entitlements) | **GET** /api/v1/entities/entitlements/{id} | Get Entitlement
[**get_entity_export_templates**](OrganizationModelControllerApi.md#get_entity_export_templates) | **GET** /api/v1/entities/exportTemplates/{id} | GET Export Template entity
[**get_entity_identity_providers**](OrganizationModelControllerApi.md#get_entity_identity_providers) | **GET** /api/v1/entities/identityProviders/{id} | Get Identity Provider
[**get_entity_jwks**](OrganizationModelControllerApi.md#get_entity_jwks) | **GET** /api/v1/entities/jwks/{id} | Get Jwk
[**get_entity_llm_endpoints**](OrganizationModelControllerApi.md#get_entity_llm_endpoints) | **GET** /api/v1/entities/llmEndpoints/{id} | Get LLM endpoint entity
[**get_entity_notification_channel_identifiers**](OrganizationModelControllerApi.md#get_entity_notification_channel_identifiers) | **GET** /api/v1/entities/notificationChannelIdentifiers/{id} | 
[**get_entity_notification_channels**](OrganizationModelControllerApi.md#get_entity_notification_channels) | **GET** /api/v1/entities/notificationChannels/{id} | Get Notification Channel entity
[**get_entity_organization_settings**](OrganizationModelControllerApi.md#get_entity_organization_settings) | **GET** /api/v1/entities/organizationSettings/{id} | Get Organization entity
[**get_entity_themes**](OrganizationModelControllerApi.md#get_entity_themes) | **GET** /api/v1/entities/themes/{id} | Get Theming
[**get_entity_user_groups**](OrganizationModelControllerApi.md#get_entity_user_groups) | **GET** /api/v1/entities/userGroups/{id} | Get UserGroup entity
[**get_entity_user_identifiers**](OrganizationModelControllerApi.md#get_entity_user_identifiers) | **GET** /api/v1/entities/userIdentifiers/{id} | Get UserIdentifier entity
[**get_entity_users**](OrganizationModelControllerApi.md#get_entity_users) | **GET** /api/v1/entities/users/{id} | Get User entity
[**get_entity_workspaces**](OrganizationModelControllerApi.md#get_entity_workspaces) | **GET** /api/v1/entities/workspaces/{id} | Get Workspace entity
[**patch_entity_color_palettes**](OrganizationModelControllerApi.md#patch_entity_color_palettes) | **PATCH** /api/v1/entities/colorPalettes/{id} | Patch Color Pallette
[**patch_entity_csp_directives**](OrganizationModelControllerApi.md#patch_entity_csp_directives) | **PATCH** /api/v1/entities/cspDirectives/{id} | Patch CSP Directives
[**patch_entity_data_sources**](OrganizationModelControllerApi.md#patch_entity_data_sources) | **PATCH** /api/v1/entities/dataSources/{id} | Patch Data Source entity
[**patch_entity_export_templates**](OrganizationModelControllerApi.md#patch_entity_export_templates) | **PATCH** /api/v1/entities/exportTemplates/{id} | Patch Export Template entity
[**patch_entity_identity_providers**](OrganizationModelControllerApi.md#patch_entity_identity_providers) | **PATCH** /api/v1/entities/identityProviders/{id} | Patch Identity Provider
[**patch_entity_jwks**](OrganizationModelControllerApi.md#patch_entity_jwks) | **PATCH** /api/v1/entities/jwks/{id} | Patch Jwk
[**patch_entity_llm_endpoints**](OrganizationModelControllerApi.md#patch_entity_llm_endpoints) | **PATCH** /api/v1/entities/llmEndpoints/{id} | Patch LLM endpoint entity
[**patch_entity_notification_channels**](OrganizationModelControllerApi.md#patch_entity_notification_channels) | **PATCH** /api/v1/entities/notificationChannels/{id} | Patch Notification Channel entity
[**patch_entity_organization_settings**](OrganizationModelControllerApi.md#patch_entity_organization_settings) | **PATCH** /api/v1/entities/organizationSettings/{id} | Patch Organization entity
[**patch_entity_themes**](OrganizationModelControllerApi.md#patch_entity_themes) | **PATCH** /api/v1/entities/themes/{id} | Patch Theming
[**patch_entity_user_groups**](OrganizationModelControllerApi.md#patch_entity_user_groups) | **PATCH** /api/v1/entities/userGroups/{id} | Patch UserGroup entity
[**patch_entity_users**](OrganizationModelControllerApi.md#patch_entity_users) | **PATCH** /api/v1/entities/users/{id} | Patch User entity
[**patch_entity_workspaces**](OrganizationModelControllerApi.md#patch_entity_workspaces) | **PATCH** /api/v1/entities/workspaces/{id} | Patch Workspace entity
[**update_entity_color_palettes**](OrganizationModelControllerApi.md#update_entity_color_palettes) | **PUT** /api/v1/entities/colorPalettes/{id} | Put Color Pallette
[**update_entity_csp_directives**](OrganizationModelControllerApi.md#update_entity_csp_directives) | **PUT** /api/v1/entities/cspDirectives/{id} | Put CSP Directives
[**update_entity_data_sources**](OrganizationModelControllerApi.md#update_entity_data_sources) | **PUT** /api/v1/entities/dataSources/{id} | Put Data Source entity
[**update_entity_export_templates**](OrganizationModelControllerApi.md#update_entity_export_templates) | **PUT** /api/v1/entities/exportTemplates/{id} | PUT Export Template entity
[**update_entity_identity_providers**](OrganizationModelControllerApi.md#update_entity_identity_providers) | **PUT** /api/v1/entities/identityProviders/{id} | Put Identity Provider
[**update_entity_jwks**](OrganizationModelControllerApi.md#update_entity_jwks) | **PUT** /api/v1/entities/jwks/{id} | Put Jwk
[**update_entity_llm_endpoints**](OrganizationModelControllerApi.md#update_entity_llm_endpoints) | **PUT** /api/v1/entities/llmEndpoints/{id} | PUT LLM endpoint entity
[**update_entity_notification_channels**](OrganizationModelControllerApi.md#update_entity_notification_channels) | **PUT** /api/v1/entities/notificationChannels/{id} | Put Notification Channel entity
[**update_entity_organization_settings**](OrganizationModelControllerApi.md#update_entity_organization_settings) | **PUT** /api/v1/entities/organizationSettings/{id} | Put Organization entity
[**update_entity_themes**](OrganizationModelControllerApi.md#update_entity_themes) | **PUT** /api/v1/entities/themes/{id} | Put Theming
[**update_entity_user_groups**](OrganizationModelControllerApi.md#update_entity_user_groups) | **PUT** /api/v1/entities/userGroups/{id} | Put UserGroup entity
[**update_entity_users**](OrganizationModelControllerApi.md#update_entity_users) | **PUT** /api/v1/entities/users/{id} | Put User entity
[**update_entity_workspaces**](OrganizationModelControllerApi.md#update_entity_workspaces) | **PUT** /api/v1/entities/workspaces/{id} | Put Workspace entity


# **create_entity_color_palettes**
> JsonApiColorPaletteOutDocument create_entity_color_palettes(json_api_color_palette_in_document)

Post Color Pallettes

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.models.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_color_palette_in_document = gooddata_api_client.JsonApiColorPaletteInDocument() # JsonApiColorPaletteInDocument | 

    try:
        # Post Color Pallettes
        api_response = api_instance.create_entity_color_palettes(json_api_color_palette_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_color_palettes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_color_palettes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_color_palette_in_document** | [**JsonApiColorPaletteInDocument**](JsonApiColorPaletteInDocument.md)|  | 

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

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

# **create_entity_csp_directives**
> JsonApiCspDirectiveOutDocument create_entity_csp_directives(json_api_csp_directive_in_document)

Post CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_csp_directive_in_document = gooddata_api_client.JsonApiCspDirectiveInDocument() # JsonApiCspDirectiveInDocument | 

    try:
        # Post CSP Directives
        api_response = api_instance.create_entity_csp_directives(json_api_csp_directive_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_csp_directives: %s\n" % e)
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

# **create_entity_data_sources**
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document, meta_include=meta_include)

Post Data Sources

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_data_source_in_document = gooddata_api_client.JsonApiDataSourceInDocument() # JsonApiDataSourceInDocument | 
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(json_api_data_source_in_document, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->create_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  | 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **create_entity_export_templates**
> JsonApiExportTemplateOutDocument create_entity_export_templates(json_api_export_template_post_optional_id_document)

Post Export Template entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.models.json_api_export_template_post_optional_id_document import JsonApiExportTemplatePostOptionalIdDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_export_template_post_optional_id_document = gooddata_api_client.JsonApiExportTemplatePostOptionalIdDocument() # JsonApiExportTemplatePostOptionalIdDocument | 

    try:
        # Post Export Template entities
        api_response = api_instance.create_entity_export_templates(json_api_export_template_post_optional_id_document)
        print("The response of OrganizationModelControllerApi->create_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_export_template_post_optional_id_document** | [**JsonApiExportTemplatePostOptionalIdDocument**](JsonApiExportTemplatePostOptionalIdDocument.md)|  | 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **create_entity_identity_providers**
> JsonApiIdentityProviderOutDocument create_entity_identity_providers(json_api_identity_provider_in_document)

Post Identity Providers

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from gooddata_api_client.models.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_identity_provider_in_document = gooddata_api_client.JsonApiIdentityProviderInDocument() # JsonApiIdentityProviderInDocument | 

    try:
        # Post Identity Providers
        api_response = api_instance.create_entity_identity_providers(json_api_identity_provider_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_identity_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_identity_provider_in_document** | [**JsonApiIdentityProviderInDocument**](JsonApiIdentityProviderInDocument.md)|  | 

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **create_entity_jwks**
> JsonApiJwkOutDocument create_entity_jwks(json_api_jwk_in_document)

Post Jwks

Creates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_jwk_in_document = gooddata_api_client.JsonApiJwkInDocument() # JsonApiJwkInDocument | 

    try:
        # Post Jwks
        api_response = api_instance.create_entity_jwks(json_api_jwk_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  | 

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **create_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument create_entity_llm_endpoints(json_api_llm_endpoint_in_document)

Post LLM endpoint entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_llm_endpoint_in_document = gooddata_api_client.JsonApiLlmEndpointInDocument() # JsonApiLlmEndpointInDocument | 

    try:
        # Post LLM endpoint entities
        api_response = api_instance.create_entity_llm_endpoints(json_api_llm_endpoint_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_llm_endpoint_in_document** | [**JsonApiLlmEndpointInDocument**](JsonApiLlmEndpointInDocument.md)|  | 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **create_entity_notification_channels**
> JsonApiNotificationChannelOutDocument create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)

Post Notification Channel entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.models.json_api_notification_channel_post_optional_id_document import JsonApiNotificationChannelPostOptionalIdDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_notification_channel_post_optional_id_document = gooddata_api_client.JsonApiNotificationChannelPostOptionalIdDocument() # JsonApiNotificationChannelPostOptionalIdDocument | 

    try:
        # Post Notification Channel entities
        api_response = api_instance.create_entity_notification_channels(json_api_notification_channel_post_optional_id_document)
        print("The response of OrganizationModelControllerApi->create_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_notification_channel_post_optional_id_document** | [**JsonApiNotificationChannelPostOptionalIdDocument**](JsonApiNotificationChannelPostOptionalIdDocument.md)|  | 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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

# **create_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument create_entity_organization_settings(json_api_organization_setting_in_document)

Post Organization Setting entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.models.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_organization_setting_in_document = gooddata_api_client.JsonApiOrganizationSettingInDocument() # JsonApiOrganizationSettingInDocument | 

    try:
        # Post Organization Setting entities
        api_response = api_instance.create_entity_organization_settings(json_api_organization_setting_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_organization_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_organization_settings: %s\n" % e)
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

# **create_entity_themes**
> JsonApiThemeOutDocument create_entity_themes(json_api_theme_in_document)

Post Theming

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.models.json_api_theme_out_document import JsonApiThemeOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_theme_in_document = gooddata_api_client.JsonApiThemeInDocument() # JsonApiThemeInDocument | 

    try:
        # Post Theming
        api_response = api_instance.create_entity_themes(json_api_theme_in_document)
        print("The response of OrganizationModelControllerApi->create_entity_themes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_themes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_theme_in_document** | [**JsonApiThemeInDocument**](JsonApiThemeInDocument.md)|  | 

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

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

# **create_entity_user_groups**
> JsonApiUserGroupOutDocument create_entity_user_groups(json_api_user_group_in_document, include=include)

Post User Group entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.models.json_api_user_group_out_document import JsonApiUserGroupOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_user_group_in_document = gooddata_api_client.JsonApiUserGroupInDocument() # JsonApiUserGroupInDocument | 
    include = ['parents'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(json_api_user_group_in_document, include=include)
        print("The response of OrganizationModelControllerApi->create_entity_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **create_entity_users**
> JsonApiUserOutDocument create_entity_users(json_api_user_in_document, include=include)

Post User entities

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.models.json_api_user_out_document import JsonApiUserOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_user_in_document = gooddata_api_client.JsonApiUserInDocument() # JsonApiUserInDocument | 
    include = ['userGroups'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Post User entities
        api_response = api_instance.create_entity_users(json_api_user_in_document, include=include)
        print("The response of OrganizationModelControllerApi->create_entity_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **create_entity_workspaces**
> JsonApiWorkspaceOutDocument create_entity_workspaces(json_api_workspace_in_document, include=include, meta_include=meta_include)

Post Workspace entities

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_api_client.models.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    json_api_workspace_in_document = gooddata_api_client.JsonApiWorkspaceInDocument() # JsonApiWorkspaceInDocument | 
    include = ['parent'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = ['metaInclude=config,permissions,hierarchy,dataModelDatasets,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(json_api_workspace_in_document, include=include, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->create_entity_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **delete_entity_color_palettes**
> delete_entity_color_palettes(id, filter=filter)

Delete a Color Pallette

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete a Color Pallette
        api_instance.delete_entity_color_palettes(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_color_palettes: %s\n" % e)
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

# **delete_entity_csp_directives**
> delete_entity_csp_directives(id, filter=filter)

Delete CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete CSP Directives
        api_instance.delete_entity_csp_directives(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_csp_directives: %s\n" % e)
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

# **delete_entity_data_sources**
> delete_entity_data_sources(id, filter=filter)

Delete Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Data Source entity
        api_instance.delete_entity_data_sources(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_data_sources: %s\n" % e)
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

# **delete_entity_export_templates**
> delete_entity_export_templates(id, filter=filter)

Delete Export Template entity

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Export Template entity
        api_instance.delete_entity_export_templates(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_export_templates: %s\n" % e)
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

# **delete_entity_identity_providers**
> delete_entity_identity_providers(id, filter=filter)

Delete Identity Provider

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'identifiers==v1,v2,v3;customClaimMapping==MapValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Identity Provider
        api_instance.delete_entity_identity_providers(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_identity_providers: %s\n" % e)
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

# **delete_entity_jwks**
> delete_entity_jwks(id, filter=filter)

Delete Jwk

Deletes JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Jwk
        api_instance.delete_entity_jwks(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_jwks: %s\n" % e)
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

# **delete_entity_llm_endpoints**
> delete_entity_llm_endpoints(id, filter=filter)



### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        api_instance.delete_entity_llm_endpoints(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_llm_endpoints: %s\n" % e)
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

# **delete_entity_notification_channels**
> delete_entity_notification_channels(id, filter=filter)

Delete Notification Channel entity

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Notification Channel entity
        api_instance.delete_entity_notification_channels(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_notification_channels: %s\n" % e)
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

# **delete_entity_organization_settings**
> delete_entity_organization_settings(id, filter=filter)

Delete Organization entity

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JsonNodeValue;type==SettingTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Organization entity
        api_instance.delete_entity_organization_settings(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_organization_settings: %s\n" % e)
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

# **delete_entity_themes**
> delete_entity_themes(id, filter=filter)

Delete Theming

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Theming
        api_instance.delete_entity_themes(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_themes: %s\n" % e)
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

# **delete_entity_user_groups**
> delete_entity_user_groups(id, filter=filter)

Delete UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete UserGroup entity
        api_instance.delete_entity_user_groups(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_user_groups: %s\n" % e)
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

# **delete_entity_users**
> delete_entity_users(id, filter=filter)

Delete User entity

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'authenticationId==someString;firstname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete User entity
        api_instance.delete_entity_users(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_users: %s\n" % e)
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

# **delete_entity_workspaces**
> delete_entity_workspaces(id, filter=filter)

Delete Workspace entity

Space of the shared interest

### Example


```python
import gooddata_api_client
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;earlyAccess==someString;parent.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Workspace entity
        api_instance.delete_entity_workspaces(id, filter=filter)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_workspaces: %s\n" % e)
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

# **get_all_entities_color_palettes**
> JsonApiColorPaletteOutList get_all_entities_color_palettes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Color Pallettes

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_color_palette_out_list import JsonApiColorPaletteOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Color Pallettes
        api_response = api_instance.get_all_entities_color_palettes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_color_palettes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_color_palettes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiColorPaletteOutList**](JsonApiColorPaletteOutList.md)

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

# **get_all_entities_csp_directives**
> JsonApiCspDirectiveOutList get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_list import JsonApiCspDirectiveOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get CSP Directives
        api_response = api_instance.get_all_entities_csp_directives(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_csp_directives: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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

# **get_all_entities_data_source_identifiers**
> JsonApiDataSourceIdentifierOutList get_all_entities_data_source_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Data Source Identifiers

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;schema==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=permissions,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Data Source Identifiers
        api_response = api_instance.get_all_entities_data_source_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_data_source_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_data_source_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceIdentifierOutList**](JsonApiDataSourceIdentifierOutList.md)

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

# **get_all_entities_data_sources**
> JsonApiDataSourceOutList get_all_entities_data_sources(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get Data Source entities

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_list import JsonApiDataSourceOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=permissions,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source entities
        api_response = api_instance.get_all_entities_data_sources(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceOutList**](JsonApiDataSourceOutList.md)

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

# **get_all_entities_entitlements**
> JsonApiEntitlementOutList get_all_entities_entitlements(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get Entitlements

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_entitlement_out_list import JsonApiEntitlementOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'value==someString;expiry==LocalDateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Entitlements
        api_response = api_instance.get_all_entities_entitlements(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_entitlements: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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

# **get_all_entities_export_templates**
> JsonApiExportTemplateOutList get_all_entities_export_templates(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

GET all Export Template entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_list import JsonApiExportTemplateOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # GET all Export Template entities
        api_response = api_instance.get_all_entities_export_templates(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiExportTemplateOutList**](JsonApiExportTemplateOutList.md)

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

# **get_all_entities_identity_providers**
> JsonApiIdentityProviderOutList get_all_entities_identity_providers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Identity Providers

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_identity_provider_out_list import JsonApiIdentityProviderOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'identifiers==v1,v2,v3;customClaimMapping==MapValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Identity Providers
        api_response = api_instance.get_all_entities_identity_providers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_identity_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiIdentityProviderOutList**](JsonApiIdentityProviderOutList.md)

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

# **get_all_entities_jwks**
> JsonApiJwkOutList get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Jwks

Returns all JSON web keys - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_list import JsonApiJwkOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Jwks
        api_response = api_instance.get_all_entities_jwks(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiJwkOutList**](JsonApiJwkOutList.md)

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

# **get_all_entities_llm_endpoints**
> JsonApiLlmEndpointOutList get_all_entities_llm_endpoints(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all LLM endpoint entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_list import JsonApiLlmEndpointOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all LLM endpoint entities
        api_response = api_instance.get_all_entities_llm_endpoints(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiLlmEndpointOutList**](JsonApiLlmEndpointOutList.md)

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

# **get_all_entities_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutList get_all_entities_notification_channel_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_identifier_out_list import JsonApiNotificationChannelIdentifierOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        api_response = api_instance.get_all_entities_notification_channel_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_notification_channel_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_notification_channel_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiNotificationChannelIdentifierOutList**](JsonApiNotificationChannelIdentifierOutList.md)

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

# **get_all_entities_notification_channels**
> JsonApiNotificationChannelOutList get_all_entities_notification_channels(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Notification Channel entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_list import JsonApiNotificationChannelOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Notification Channel entities
        api_response = api_instance.get_all_entities_notification_channels(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiNotificationChannelOutList**](JsonApiNotificationChannelOutList.md)

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

# **get_all_entities_organization_settings**
> JsonApiOrganizationSettingOutList get_all_entities_organization_settings(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get Organization entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_setting_out_list import JsonApiOrganizationSettingOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'content==JsonNodeValue;type==SettingTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Organization entities
        api_response = api_instance.get_all_entities_organization_settings(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_organization_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_organization_settings: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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

# **get_all_entities_themes**
> JsonApiThemeOutList get_all_entities_themes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get all Theming entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_theme_out_list import JsonApiThemeOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Theming entities
        api_response = api_instance.get_all_entities_themes(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_themes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_themes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiThemeOutList**](JsonApiThemeOutList.md)

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

# **get_all_entities_user_groups**
> JsonApiUserGroupOutList get_all_entities_user_groups(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)

Get UserGroup entities

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_group_out_list import JsonApiUserGroupOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parents'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get UserGroup entities
        api_response = api_instance.get_all_entities_user_groups(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiUserGroupOutList**](JsonApiUserGroupOutList.md)

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

# **get_all_entities_user_identifiers**
> JsonApiUserIdentifierOutList get_all_entities_user_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

Get UserIdentifier entities

UserIdentifier - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_identifier_out_list import JsonApiUserIdentifierOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'firstname==someString;lastname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get UserIdentifier entities
        api_response = api_instance.get_all_entities_user_identifiers(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_user_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_user_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiUserIdentifierOutList**](JsonApiUserIdentifierOutList.md)

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

# **get_all_entities_users**
> JsonApiUserOutList get_all_entities_users(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)

Get User entities

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_out_list import JsonApiUserOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'authenticationId==someString;firstname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['userGroups'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get User entities
        api_response = api_instance.get_all_entities_users(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiUserOutList**](JsonApiUserOutList.md)

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

# **get_all_entities_workspaces**
> JsonApiWorkspaceOutList get_all_entities_workspaces(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)

Get Workspace entities

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_out_list import JsonApiWorkspaceOutList
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    filter = 'name==someString;earlyAccess==someString;parent.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parent'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=config,permissions,hierarchy,dataModelDatasets,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Workspace entities
        api_response = api_instance.get_all_entities_workspaces(filter=filter, include=include, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_all_entities_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiWorkspaceOutList**](JsonApiWorkspaceOutList.md)

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

# **get_entity_color_palettes**
> JsonApiColorPaletteOutDocument get_entity_color_palettes(id, filter=filter)

Get Color Pallette

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_color_palettes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_color_palettes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

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
> JsonApiCspDirectiveOutDocument get_entity_csp_directives(id, filter=filter)

Get CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_csp_directives: %s\n" % e)
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

# **get_entity_data_source_identifiers**
> JsonApiDataSourceIdentifierOutDocument get_entity_data_source_identifiers(id, filter=filter, meta_include=meta_include)

Get Data Source Identifier

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;schema==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(id, filter=filter, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_entity_data_source_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_source_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceIdentifierOutDocument**](JsonApiDataSourceIdentifierOutDocument.md)

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

# **get_entity_data_sources**
> JsonApiDataSourceOutDocument get_entity_data_sources(id, filter=filter, meta_include=meta_include)

Get Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    meta_include = ['metaInclude=permissions,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(id, filter=filter, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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
> JsonApiEntitlementOutDocument get_entity_entitlements(id, filter=filter)

Get Entitlement

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_entitlement_out_document import JsonApiEntitlementOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'value==someString;expiry==LocalDateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_entitlements:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_entitlements: %s\n" % e)
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

# **get_entity_export_templates**
> JsonApiExportTemplateOutDocument get_entity_export_templates(id, filter=filter)

GET Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **get_entity_identity_providers**
> JsonApiIdentityProviderOutDocument get_entity_identity_providers(id, filter=filter)

Get Identity Provider

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'identifiers==v1,v2,v3;customClaimMapping==MapValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Identity Provider
        api_response = api_instance.get_entity_identity_providers(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_identity_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **get_entity_jwks**
> JsonApiJwkOutDocument get_entity_jwks(id, filter=filter)

Get Jwk

Returns JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Jwk
        api_response = api_instance.get_entity_jwks(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **get_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument get_entity_llm_endpoints(id, filter=filter)

Get LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get LLM endpoint entity
        api_response = api_instance.get_entity_llm_endpoints(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **get_entity_notification_channel_identifiers**
> JsonApiNotificationChannelIdentifierOutDocument get_entity_notification_channel_identifiers(id, filter=filter)



### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_identifier_out_document import JsonApiNotificationChannelIdentifierOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        api_response = api_instance.get_entity_notification_channel_identifiers(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_notification_channel_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_notification_channel_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelIdentifierOutDocument**](JsonApiNotificationChannelIdentifierOutDocument.md)

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

# **get_entity_notification_channels**
> JsonApiNotificationChannelOutDocument get_entity_notification_channels(id, filter=filter)

Get Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Notification Channel entity
        api_response = api_instance.get_entity_notification_channels(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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
> JsonApiOrganizationSettingOutDocument get_entity_organization_settings(id, filter=filter)

Get Organization entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'content==JsonNodeValue;type==SettingTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_organization_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_organization_settings: %s\n" % e)
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

# **get_entity_themes**
> JsonApiThemeOutDocument get_entity_themes(id, filter=filter)

Get Theming

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_theme_out_document import JsonApiThemeOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_themes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_themes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

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

# **get_entity_user_groups**
> JsonApiUserGroupOutDocument get_entity_user_groups(id, filter=filter, include=include)

Get UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_group_out_document import JsonApiUserGroupOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parents'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(id, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->get_entity_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **get_entity_user_identifiers**
> JsonApiUserIdentifierOutDocument get_entity_user_identifiers(id, filter=filter)

Get UserIdentifier entity

UserIdentifier - represents basic information about entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_identifier_out_document import JsonApiUserIdentifierOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'firstname==someString;lastname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Get UserIdentifier entity
        api_response = api_instance.get_entity_user_identifiers(id, filter=filter)
        print("The response of OrganizationModelControllerApi->get_entity_user_identifiers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_identifiers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiUserIdentifierOutDocument**](JsonApiUserIdentifierOutDocument.md)

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

# **get_entity_users**
> JsonApiUserOutDocument get_entity_users(id, filter=filter, include=include)

Get User entity

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_out_document import JsonApiUserOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'authenticationId==someString;firstname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['userGroups'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Get User entity
        api_response = api_instance.get_entity_users(id, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->get_entity_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **get_entity_workspaces**
> JsonApiWorkspaceOutDocument get_entity_workspaces(id, filter=filter, include=include, meta_include=meta_include)

Get Workspace entity

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;earlyAccess==someString;parent.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parent'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = ['metaInclude=config,permissions,hierarchy,dataModelDatasets,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(id, filter=filter, include=include, meta_include=meta_include)
        print("The response of OrganizationModelControllerApi->get_entity_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **patch_entity_color_palettes**
> JsonApiColorPaletteOutDocument patch_entity_color_palettes(id, json_api_color_palette_patch_document, filter=filter)

Patch Color Pallette

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from gooddata_api_client.models.json_api_color_palette_patch_document import JsonApiColorPalettePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_color_palette_patch_document = gooddata_api_client.JsonApiColorPalettePatchDocument() # JsonApiColorPalettePatchDocument | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(id, json_api_color_palette_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_color_palettes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_color_palettes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_color_palette_patch_document** | [**JsonApiColorPalettePatchDocument**](JsonApiColorPalettePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

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

# **patch_entity_csp_directives**
> JsonApiCspDirectiveOutDocument patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)

Patch CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.models.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_csp_directive_patch_document = gooddata_api_client.JsonApiCspDirectivePatchDocument() # JsonApiCspDirectivePatchDocument | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(id, json_api_csp_directive_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_csp_directives: %s\n" % e)
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

# **patch_entity_data_sources**
> JsonApiDataSourceOutDocument patch_entity_data_sources(id, json_api_data_source_patch_document, filter=filter)

Patch Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from gooddata_api_client.models.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_data_source_patch_document = gooddata_api_client.JsonApiDataSourcePatchDocument() # JsonApiDataSourcePatchDocument | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(id, json_api_data_source_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_data_source_patch_document** | [**JsonApiDataSourcePatchDocument**](JsonApiDataSourcePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **patch_entity_export_templates**
> JsonApiExportTemplateOutDocument patch_entity_export_templates(id, json_api_export_template_patch_document, filter=filter)

Patch Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.models.json_api_export_template_patch_document import JsonApiExportTemplatePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_export_template_patch_document = gooddata_api_client.JsonApiExportTemplatePatchDocument() # JsonApiExportTemplatePatchDocument | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(id, json_api_export_template_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_export_template_patch_document** | [**JsonApiExportTemplatePatchDocument**](JsonApiExportTemplatePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **patch_entity_identity_providers**
> JsonApiIdentityProviderOutDocument patch_entity_identity_providers(id, json_api_identity_provider_patch_document, filter=filter)

Patch Identity Provider

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
from gooddata_api_client.models.json_api_identity_provider_patch_document import JsonApiIdentityProviderPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_identity_provider_patch_document = gooddata_api_client.JsonApiIdentityProviderPatchDocument() # JsonApiIdentityProviderPatchDocument | 
    filter = 'identifiers==v1,v2,v3;customClaimMapping==MapValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Identity Provider
        api_response = api_instance.patch_entity_identity_providers(id, json_api_identity_provider_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_identity_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_identity_provider_patch_document** | [**JsonApiIdentityProviderPatchDocument**](JsonApiIdentityProviderPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **patch_entity_jwks**
> JsonApiJwkOutDocument patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)

Patch Jwk

Patches JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
from gooddata_api_client.models.json_api_jwk_patch_document import JsonApiJwkPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_jwk_patch_document = gooddata_api_client.JsonApiJwkPatchDocument() # JsonApiJwkPatchDocument | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Jwk
        api_response = api_instance.patch_entity_jwks(id, json_api_jwk_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_jwk_patch_document** | [**JsonApiJwkPatchDocument**](JsonApiJwkPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **patch_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document, filter=filter)

Patch LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
from gooddata_api_client.models.json_api_llm_endpoint_patch_document import JsonApiLlmEndpointPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_llm_endpoint_patch_document = gooddata_api_client.JsonApiLlmEndpointPatchDocument() # JsonApiLlmEndpointPatchDocument | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch LLM endpoint entity
        api_response = api_instance.patch_entity_llm_endpoints(id, json_api_llm_endpoint_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_llm_endpoint_patch_document** | [**JsonApiLlmEndpointPatchDocument**](JsonApiLlmEndpointPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **patch_entity_notification_channels**
> JsonApiNotificationChannelOutDocument patch_entity_notification_channels(id, json_api_notification_channel_patch_document, filter=filter)

Patch Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
from gooddata_api_client.models.json_api_notification_channel_patch_document import JsonApiNotificationChannelPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_notification_channel_patch_document = gooddata_api_client.JsonApiNotificationChannelPatchDocument() # JsonApiNotificationChannelPatchDocument | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Notification Channel entity
        api_response = api_instance.patch_entity_notification_channels(id, json_api_notification_channel_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_notification_channel_patch_document** | [**JsonApiNotificationChannelPatchDocument**](JsonApiNotificationChannelPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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

# **patch_entity_organization_settings**
> JsonApiOrganizationSettingOutDocument patch_entity_organization_settings(id, json_api_organization_setting_patch_document, filter=filter)

Patch Organization entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from gooddata_api_client.models.json_api_organization_setting_patch_document import JsonApiOrganizationSettingPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_organization_setting_patch_document = gooddata_api_client.JsonApiOrganizationSettingPatchDocument() # JsonApiOrganizationSettingPatchDocument | 
    filter = 'content==JsonNodeValue;type==SettingTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(id, json_api_organization_setting_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_organization_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_organization_settings: %s\n" % e)
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

# **patch_entity_themes**
> JsonApiThemeOutDocument patch_entity_themes(id, json_api_theme_patch_document, filter=filter)

Patch Theming

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_theme_out_document import JsonApiThemeOutDocument
from gooddata_api_client.models.json_api_theme_patch_document import JsonApiThemePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_theme_patch_document = gooddata_api_client.JsonApiThemePatchDocument() # JsonApiThemePatchDocument | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(id, json_api_theme_patch_document, filter=filter)
        print("The response of OrganizationModelControllerApi->patch_entity_themes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_themes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_theme_patch_document** | [**JsonApiThemePatchDocument**](JsonApiThemePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

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

# **patch_entity_user_groups**
> JsonApiUserGroupOutDocument patch_entity_user_groups(id, json_api_user_group_patch_document, filter=filter, include=include)

Patch UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_api_client.models.json_api_user_group_patch_document import JsonApiUserGroupPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_user_group_patch_document = gooddata_api_client.JsonApiUserGroupPatchDocument() # JsonApiUserGroupPatchDocument | 
    filter = 'name==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parents'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(id, json_api_user_group_patch_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->patch_entity_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_user_group_patch_document** | [**JsonApiUserGroupPatchDocument**](JsonApiUserGroupPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **patch_entity_users**
> JsonApiUserOutDocument patch_entity_users(id, json_api_user_patch_document, filter=filter, include=include)

Patch User entity

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_api_client.models.json_api_user_patch_document import JsonApiUserPatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_user_patch_document = gooddata_api_client.JsonApiUserPatchDocument() # JsonApiUserPatchDocument | 
    filter = 'authenticationId==someString;firstname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['userGroups'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(id, json_api_user_patch_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->patch_entity_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_user_patch_document** | [**JsonApiUserPatchDocument**](JsonApiUserPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **patch_entity_workspaces**
> JsonApiWorkspaceOutDocument patch_entity_workspaces(id, json_api_workspace_patch_document, filter=filter, include=include)

Patch Workspace entity

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.models.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_workspace_patch_document = gooddata_api_client.JsonApiWorkspacePatchDocument() # JsonApiWorkspacePatchDocument | 
    filter = 'name==someString;earlyAccess==someString;parent.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parent'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(id, json_api_workspace_patch_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->patch_entity_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_workspace_patch_document** | [**JsonApiWorkspacePatchDocument**](JsonApiWorkspacePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

# **update_entity_color_palettes**
> JsonApiColorPaletteOutDocument update_entity_color_palettes(id, json_api_color_palette_in_document, filter=filter)

Put Color Pallette

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.models.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_color_palette_in_document = gooddata_api_client.JsonApiColorPaletteInDocument() # JsonApiColorPaletteInDocument | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(id, json_api_color_palette_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_color_palettes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_color_palettes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_color_palette_in_document** | [**JsonApiColorPaletteInDocument**](JsonApiColorPaletteInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiColorPaletteOutDocument**](JsonApiColorPaletteOutDocument.md)

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
> JsonApiCspDirectiveOutDocument update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)

Put CSP Directives

 Context Security Police Directive

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_csp_directive_in_document = gooddata_api_client.JsonApiCspDirectiveInDocument() # JsonApiCspDirectiveInDocument | 
    filter = 'sources==v1,v2,v3' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(id, json_api_csp_directive_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_csp_directives:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_csp_directives: %s\n" % e)
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

# **update_entity_data_sources**
> JsonApiDataSourceOutDocument update_entity_data_sources(id, json_api_data_source_in_document, filter=filter)

Put Data Source entity

Data Source - represents data source for the workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.models.json_api_data_source_out_document import JsonApiDataSourceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_data_source_in_document = gooddata_api_client.JsonApiDataSourceInDocument() # JsonApiDataSourceInDocument | 
    filter = 'name==someString;type==DatabaseTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(id, json_api_data_source_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_data_sources:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_data_sources: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_data_source_in_document** | [**JsonApiDataSourceInDocument**](JsonApiDataSourceInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiDataSourceOutDocument**](JsonApiDataSourceOutDocument.md)

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

# **update_entity_export_templates**
> JsonApiExportTemplateOutDocument update_entity_export_templates(id, json_api_export_template_in_document, filter=filter)

PUT Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_in_document import JsonApiExportTemplateInDocument
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_export_template_in_document = gooddata_api_client.JsonApiExportTemplateInDocument() # JsonApiExportTemplateInDocument | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(id, json_api_export_template_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_export_template_in_document** | [**JsonApiExportTemplateInDocument**](JsonApiExportTemplateInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **update_entity_identity_providers**
> JsonApiIdentityProviderOutDocument update_entity_identity_providers(id, json_api_identity_provider_in_document, filter=filter)

Put Identity Provider

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument
from gooddata_api_client.models.json_api_identity_provider_out_document import JsonApiIdentityProviderOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_identity_provider_in_document = gooddata_api_client.JsonApiIdentityProviderInDocument() # JsonApiIdentityProviderInDocument | 
    filter = 'identifiers==v1,v2,v3;customClaimMapping==MapValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Identity Provider
        api_response = api_instance.update_entity_identity_providers(id, json_api_identity_provider_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_identity_providers:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_identity_providers: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_identity_provider_in_document** | [**JsonApiIdentityProviderInDocument**](JsonApiIdentityProviderInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiIdentityProviderOutDocument**](JsonApiIdentityProviderOutDocument.md)

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

# **update_entity_jwks**
> JsonApiJwkOutDocument update_entity_jwks(id, json_api_jwk_in_document, filter=filter)

Put Jwk

Updates JSON web key - used to verify JSON web tokens (Jwts)

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_jwk_in_document import JsonApiJwkInDocument
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_jwk_in_document = gooddata_api_client.JsonApiJwkInDocument() # JsonApiJwkInDocument | 
    filter = 'content==JwkSpecificationValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Jwk
        api_response = api_instance.update_entity_jwks(id, json_api_jwk_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_jwks:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_jwks: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_jwk_in_document** | [**JsonApiJwkInDocument**](JsonApiJwkInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiJwkOutDocument**](JsonApiJwkOutDocument.md)

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

# **update_entity_llm_endpoints**
> JsonApiLlmEndpointOutDocument update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document, filter=filter)

PUT LLM endpoint entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_llm_endpoint_in_document import JsonApiLlmEndpointInDocument
from gooddata_api_client.models.json_api_llm_endpoint_out_document import JsonApiLlmEndpointOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_llm_endpoint_in_document = gooddata_api_client.JsonApiLlmEndpointInDocument() # JsonApiLlmEndpointInDocument | 
    filter = 'title==someString;provider==LLMProviderValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # PUT LLM endpoint entity
        api_response = api_instance.update_entity_llm_endpoints(id, json_api_llm_endpoint_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_llm_endpoints:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_llm_endpoints: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_llm_endpoint_in_document** | [**JsonApiLlmEndpointInDocument**](JsonApiLlmEndpointInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiLlmEndpointOutDocument**](JsonApiLlmEndpointOutDocument.md)

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

# **update_entity_notification_channels**
> JsonApiNotificationChannelOutDocument update_entity_notification_channels(id, json_api_notification_channel_in_document, filter=filter)

Put Notification Channel entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_notification_channel_in_document import JsonApiNotificationChannelInDocument
from gooddata_api_client.models.json_api_notification_channel_out_document import JsonApiNotificationChannelOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_notification_channel_in_document = gooddata_api_client.JsonApiNotificationChannelInDocument() # JsonApiNotificationChannelInDocument | 
    filter = 'name==someString;description==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Notification Channel entity
        api_response = api_instance.update_entity_notification_channels(id, json_api_notification_channel_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_notification_channels:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_notification_channels: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_notification_channel_in_document** | [**JsonApiNotificationChannelInDocument**](JsonApiNotificationChannelInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiNotificationChannelOutDocument**](JsonApiNotificationChannelOutDocument.md)

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
> JsonApiOrganizationSettingOutDocument update_entity_organization_settings(id, json_api_organization_setting_in_document, filter=filter)

Put Organization entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.models.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_organization_setting_in_document = gooddata_api_client.JsonApiOrganizationSettingInDocument() # JsonApiOrganizationSettingInDocument | 
    filter = 'content==JsonNodeValue;type==SettingTypeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(id, json_api_organization_setting_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_organization_settings:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_organization_settings: %s\n" % e)
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

# **update_entity_themes**
> JsonApiThemeOutDocument update_entity_themes(id, json_api_theme_in_document, filter=filter)

Put Theming

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.models.json_api_theme_out_document import JsonApiThemeOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_theme_in_document = gooddata_api_client.JsonApiThemeInDocument() # JsonApiThemeInDocument | 
    filter = 'name==someString;content==JsonNodeValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(id, json_api_theme_in_document, filter=filter)
        print("The response of OrganizationModelControllerApi->update_entity_themes:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_themes: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_theme_in_document** | [**JsonApiThemeInDocument**](JsonApiThemeInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiThemeOutDocument**](JsonApiThemeOutDocument.md)

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

# **update_entity_user_groups**
> JsonApiUserGroupOutDocument update_entity_user_groups(id, json_api_user_group_in_document, filter=filter, include=include)

Put UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.models.json_api_user_group_out_document import JsonApiUserGroupOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_user_group_in_document = gooddata_api_client.JsonApiUserGroupInDocument() # JsonApiUserGroupInDocument | 
    filter = 'name==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parents'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(id, json_api_user_group_in_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->update_entity_user_groups:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_user_groups: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_user_group_in_document** | [**JsonApiUserGroupInDocument**](JsonApiUserGroupInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserGroupOutDocument**](JsonApiUserGroupOutDocument.md)

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

# **update_entity_users**
> JsonApiUserOutDocument update_entity_users(id, json_api_user_in_document, filter=filter, include=include)

Put User entity

User - represents entity interacting with platform

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.models.json_api_user_out_document import JsonApiUserOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_user_in_document = gooddata_api_client.JsonApiUserInDocument() # JsonApiUserInDocument | 
    filter = 'authenticationId==someString;firstname==someString' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['userGroups'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put User entity
        api_response = api_instance.update_entity_users(id, json_api_user_in_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->update_entity_users:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_users: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_user_in_document** | [**JsonApiUserInDocument**](JsonApiUserInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiUserOutDocument**](JsonApiUserOutDocument.md)

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

# **update_entity_workspaces**
> JsonApiWorkspaceOutDocument update_entity_workspaces(id, json_api_workspace_in_document, filter=filter, include=include)

Put Workspace entity

Space of the shared interest

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from gooddata_api_client.models.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
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
    api_instance = gooddata_api_client.OrganizationModelControllerApi(api_client)
    id = 'id_example' # str | 
    json_api_workspace_in_document = gooddata_api_client.JsonApiWorkspaceInDocument() # JsonApiWorkspaceInDocument | 
    filter = 'name==someString;earlyAccess==someString;parent.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['parent'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(id, json_api_workspace_in_document, filter=filter, include=include)
        print("The response of OrganizationModelControllerApi->update_entity_workspaces:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_workspaces: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_workspace_in_document** | [**JsonApiWorkspaceInDocument**](JsonApiWorkspaceInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

### Return type

[**JsonApiWorkspaceOutDocument**](JsonApiWorkspaceOutDocument.md)

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

