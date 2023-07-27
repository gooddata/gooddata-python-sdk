<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.organization_model_controller_api.OrganizationModelControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_color_palettes**](#create_entity_color_palettes) | **post** /api/v1/entities/colorPalettes | Post Color Pallettes
[**create_entity_csp_directives**](#create_entity_csp_directives) | **post** /api/v1/entities/cspDirectives | Post CSP Directives
[**create_entity_data_sources**](#create_entity_data_sources) | **post** /api/v1/entities/dataSources | Post Data Sources
[**create_entity_organization_settings**](#create_entity_organization_settings) | **post** /api/v1/entities/organizationSettings | Post Organization Setting entities
[**create_entity_themes**](#create_entity_themes) | **post** /api/v1/entities/themes | Post Theming
[**create_entity_user_groups**](#create_entity_user_groups) | **post** /api/v1/entities/userGroups | Post User Group entities
[**create_entity_users**](#create_entity_users) | **post** /api/v1/entities/users | Post User entities
[**create_entity_workspaces**](#create_entity_workspaces) | **post** /api/v1/entities/workspaces | Post Workspace entities
[**delete_entity_color_palettes**](#delete_entity_color_palettes) | **delete** /api/v1/entities/colorPalettes/{id} | Delete a Color Pallette
[**delete_entity_csp_directives**](#delete_entity_csp_directives) | **delete** /api/v1/entities/cspDirectives/{id} | Delete CSP Directives
[**delete_entity_data_sources**](#delete_entity_data_sources) | **delete** /api/v1/entities/dataSources/{id} | Delete Data Source entity
[**delete_entity_organization_settings**](#delete_entity_organization_settings) | **delete** /api/v1/entities/organizationSettings/{id} | Delete Organization entity
[**delete_entity_themes**](#delete_entity_themes) | **delete** /api/v1/entities/themes/{id} | Delete Theming
[**delete_entity_user_groups**](#delete_entity_user_groups) | **delete** /api/v1/entities/userGroups/{id} | Delete UserGroup entity
[**delete_entity_users**](#delete_entity_users) | **delete** /api/v1/entities/users/{id} | Delete User entity
[**delete_entity_workspaces**](#delete_entity_workspaces) | **delete** /api/v1/entities/workspaces/{id} | Delete Workspace entity
[**get_all_entities_color_palettes**](#get_all_entities_color_palettes) | **get** /api/v1/entities/colorPalettes | Get all Color Pallettes
[**get_all_entities_csp_directives**](#get_all_entities_csp_directives) | **get** /api/v1/entities/cspDirectives | Get CSP Directives
[**get_all_entities_data_source_identifiers**](#get_all_entities_data_source_identifiers) | **get** /api/v1/entities/dataSourceIdentifiers | Get all Data Source Identifiers
[**get_all_entities_data_sources**](#get_all_entities_data_sources) | **get** /api/v1/entities/dataSources | Get Data Source entities
[**get_all_entities_entitlements**](#get_all_entities_entitlements) | **get** /api/v1/entities/entitlements | Get Entitlements
[**get_all_entities_organization_settings**](#get_all_entities_organization_settings) | **get** /api/v1/entities/organizationSettings | Get Organization entities
[**get_all_entities_themes**](#get_all_entities_themes) | **get** /api/v1/entities/themes | Get all Theming entities
[**get_all_entities_user_groups**](#get_all_entities_user_groups) | **get** /api/v1/entities/userGroups | Get UserGroup entities
[**get_all_entities_users**](#get_all_entities_users) | **get** /api/v1/entities/users | Get User entities
[**get_all_entities_workspaces**](#get_all_entities_workspaces) | **get** /api/v1/entities/workspaces | Get Workspace entities
[**get_entity_color_palettes**](#get_entity_color_palettes) | **get** /api/v1/entities/colorPalettes/{id} | Get Color Pallette
[**get_entity_csp_directives**](#get_entity_csp_directives) | **get** /api/v1/entities/cspDirectives/{id} | Get CSP Directives
[**get_entity_data_source_identifiers**](#get_entity_data_source_identifiers) | **get** /api/v1/entities/dataSourceIdentifiers/{id} | Get Data Source Identifier
[**get_entity_data_sources**](#get_entity_data_sources) | **get** /api/v1/entities/dataSources/{id} | Get Data Source entity
[**get_entity_entitlements**](#get_entity_entitlements) | **get** /api/v1/entities/entitlements/{id} | Get Entitlement
[**get_entity_organization_settings**](#get_entity_organization_settings) | **get** /api/v1/entities/organizationSettings/{id} | Get Organization entity
[**get_entity_themes**](#get_entity_themes) | **get** /api/v1/entities/themes/{id} | Get Theming
[**get_entity_user_groups**](#get_entity_user_groups) | **get** /api/v1/entities/userGroups/{id} | Get UserGroup entity
[**get_entity_users**](#get_entity_users) | **get** /api/v1/entities/users/{id} | Get User entity
[**get_entity_workspaces**](#get_entity_workspaces) | **get** /api/v1/entities/workspaces/{id} | Get Workspace entity
[**patch_entity_color_palettes**](#patch_entity_color_palettes) | **patch** /api/v1/entities/colorPalettes/{id} | Patch Color Pallette
[**patch_entity_csp_directives**](#patch_entity_csp_directives) | **patch** /api/v1/entities/cspDirectives/{id} | Patch CSP Directives
[**patch_entity_data_sources**](#patch_entity_data_sources) | **patch** /api/v1/entities/dataSources/{id} | Patch Data Source entity
[**patch_entity_organization_settings**](#patch_entity_organization_settings) | **patch** /api/v1/entities/organizationSettings/{id} | Patch Organization entity
[**patch_entity_themes**](#patch_entity_themes) | **patch** /api/v1/entities/themes/{id} | Patch Theming
[**patch_entity_user_groups**](#patch_entity_user_groups) | **patch** /api/v1/entities/userGroups/{id} | Patch UserGroup entity
[**patch_entity_users**](#patch_entity_users) | **patch** /api/v1/entities/users/{id} | Patch User entity
[**patch_entity_workspaces**](#patch_entity_workspaces) | **patch** /api/v1/entities/workspaces/{id} | Patch Workspace entity
[**update_entity_color_palettes**](#update_entity_color_palettes) | **put** /api/v1/entities/colorPalettes/{id} | Put Color Pallette
[**update_entity_csp_directives**](#update_entity_csp_directives) | **put** /api/v1/entities/cspDirectives/{id} | Put CSP Directives
[**update_entity_data_sources**](#update_entity_data_sources) | **put** /api/v1/entities/dataSources/{id} | Put Data Source entity
[**update_entity_organization_settings**](#update_entity_organization_settings) | **put** /api/v1/entities/organizationSettings/{id} | Put Organization entity
[**update_entity_themes**](#update_entity_themes) | **put** /api/v1/entities/themes/{id} | Put Theming
[**update_entity_user_groups**](#update_entity_user_groups) | **put** /api/v1/entities/userGroups/{id} | Put UserGroup entity
[**update_entity_users**](#update_entity_users) | **put** /api/v1/entities/users/{id} | Put User entity
[**update_entity_workspaces**](#update_entity_workspaces) | **put** /api/v1/entities/workspaces/{id} | Put Workspace entity

# **create_entity_color_palettes**
<a id="create_entity_color_palettes"></a>
> JsonApiColorPaletteOutDocument create_entity_color_palettes(json_api_color_palette_in_document)

Post Color Pallettes

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiColorPaletteInDocument(
        data=JsonApiColorPaletteIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    )
    try:
        # Post Color Pallettes
        api_response = api_instance.create_entity_color_palettes(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteInDocument**](../../models/JsonApiColorPaletteInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_color_palettes.ApiResponseFor201) | Request successfully processed

#### create_entity_color_palettes.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteOutDocument**](../../models/JsonApiColorPaletteOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_csp_directives**
<a id="create_entity_csp_directives"></a>
> JsonApiCspDirectiveOutDocument create_entity_csp_directives(json_api_csp_directive_in_document)

Post CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=dict(
                sources=[
                    "sources_example"
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    )
    try:
        # Post CSP Directives
        api_response = api_instance.create_entity_csp_directives(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveInDocument**](../../models/JsonApiCspDirectiveInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_csp_directives.ApiResponseFor201) | Request successfully processed

#### create_entity_csp_directives.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveOutDocument**](../../models/JsonApiCspDirectiveOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_data_sources**
<a id="create_entity_data_sources"></a>
> JsonApiDataSourceOutDocument create_entity_data_sources(json_api_data_source_in_document)

Post Data Sources

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_data_sources: %s\n" % e)

    # example passing only optional values
    query_params = {
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Post Data Sources
        api_response = api_instance.create_entity_data_sources(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceInDocument**](../../models/JsonApiDataSourceInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
metaInclude | MetaIncludeSchema | | optional


# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_data_sources.ApiResponseFor201) | Request successfully processed

#### create_entity_data_sources.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_organization_settings**
<a id="create_entity_organization_settings"></a>
> JsonApiOrganizationSettingOutDocument create_entity_organization_settings(json_api_organization_setting_in_document)

Post Organization Setting entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    )
    try:
        # Post Organization Setting entities
        api_response = api_instance.create_entity_organization_settings(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingInDocument**](../../models/JsonApiOrganizationSettingInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_organization_settings.ApiResponseFor201) | Request successfully processed

#### create_entity_organization_settings.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingOutDocument**](../../models/JsonApiOrganizationSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_themes**
<a id="create_entity_themes"></a>
> JsonApiThemeOutDocument create_entity_themes(json_api_theme_in_document)

Post Theming

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiThemeInDocument(
        data=JsonApiThemeIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    )
    try:
        # Post Theming
        api_response = api_instance.create_entity_themes(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeInDocument**](../../models/JsonApiThemeInDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_themes.ApiResponseFor201) | Request successfully processed

#### create_entity_themes.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeOutDocument**](../../models/JsonApiThemeOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_user_groups**
<a id="create_entity_user_groups"></a>
> JsonApiUserGroupOutDocument create_entity_user_groups(json_api_user_group_in_document)

Post User Group entities

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
    }
    body = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_user_groups: %s\n" % e)

    # example passing only optional values
    query_params = {
        'include': [
        "include=parents"
    ],
    }
    body = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Post User Group entities
        api_response = api_instance.create_entity_user_groups(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupInDocument**](../../models/JsonApiUserGroupInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "parents", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_user_groups.ApiResponseFor201) | Request successfully processed

#### create_entity_user_groups.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupOutDocument**](../../models/JsonApiUserGroupOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_users**
<a id="create_entity_users"></a>
> JsonApiUserOutDocument create_entity_users(json_api_user_in_document)

Post User entities

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
    }
    body = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_users: %s\n" % e)

    # example passing only optional values
    query_params = {
        'include': [
        "include=userGroups"
    ],
    }
    body = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Post User entities
        api_response = api_instance.create_entity_users(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserInDocument**](../../models/JsonApiUserInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_users.ApiResponseFor201) | Request successfully processed

#### create_entity_users.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserOutDocument**](../../models/JsonApiUserOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **create_entity_workspaces**
<a id="create_entity_workspaces"></a>
> JsonApiWorkspaceOutDocument create_entity_workspaces(json_api_workspace_in_document)

Post Workspace entities

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    query_params = {
    }
    body = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_workspaces: %s\n" % e)

    # example passing only optional values
    query_params = {
        'include': [
        "include=parent"
    ],
        'metaInclude': [
        "metaInclude=config,permissions,all"
    ],
    }
    body = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Post Workspace entities
        api_response = api_instance.create_entity_workspaces(
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->create_entity_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceInDocument**](../../models/JsonApiWorkspaceInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "parent", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["config", "permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_workspaces.ApiResponseFor201) | Request successfully processed

#### create_entity_workspaces.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceOutDocument**](../../models/JsonApiWorkspaceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_color_palettes**
<a id="delete_entity_color_palettes"></a>
> delete_entity_color_palettes(id)

Delete a Color Pallette

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete a Color Pallette
        api_response = api_instance.delete_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_color_palettes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    try:
        # Delete a Color Pallette
        api_response = api_instance.delete_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_color_palettes.ApiResponseFor204) | Successfully deleted

#### delete_entity_color_palettes.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_csp_directives**
<a id="delete_entity_csp_directives"></a>
> delete_entity_csp_directives(id)

Delete CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete CSP Directives
        api_response = api_instance.delete_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_csp_directives: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=sources==v1,v2,v3",
    }
    try:
        # Delete CSP Directives
        api_response = api_instance.delete_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_csp_directives.ApiResponseFor204) | Successfully deleted

#### delete_entity_csp_directives.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_data_sources**
<a id="delete_entity_data_sources"></a>
> delete_entity_data_sources(id)

Delete Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Data Source entity
        api_response = api_instance.delete_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    try:
        # Delete Data Source entity
        api_response = api_instance.delete_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_data_sources.ApiResponseFor204) | Successfully deleted

#### delete_entity_data_sources.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_organization_settings**
<a id="delete_entity_organization_settings"></a>
> delete_entity_organization_settings(id)

Delete Organization entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Organization entity
        api_response = api_instance.delete_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_organization_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    try:
        # Delete Organization entity
        api_response = api_instance.delete_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_organization_settings.ApiResponseFor204) | Successfully deleted

#### delete_entity_organization_settings.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_themes**
<a id="delete_entity_themes"></a>
> delete_entity_themes(id)

Delete Theming

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Theming
        api_response = api_instance.delete_entity_themes(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_themes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    try:
        # Delete Theming
        api_response = api_instance.delete_entity_themes(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_themes.ApiResponseFor204) | Successfully deleted

#### delete_entity_themes.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_user_groups**
<a id="delete_entity_user_groups"></a>
> delete_entity_user_groups(id)

Delete UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete UserGroup entity
        api_response = api_instance.delete_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_user_groups: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString",
    }
    try:
        # Delete UserGroup entity
        api_response = api_instance.delete_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_user_groups.ApiResponseFor204) | Successfully deleted

#### delete_entity_user_groups.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_users**
<a id="delete_entity_users"></a>
> delete_entity_users(id)

Delete User entity

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete User entity
        api_response = api_instance.delete_entity_users(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_users: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=authenticationId==someString;firstname==someString",
    }
    try:
        # Delete User entity
        api_response = api_instance.delete_entity_users(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_users.ApiResponseFor204) | Successfully deleted

#### delete_entity_users.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_workspaces**
<a id="delete_entity_workspaces"></a>
> delete_entity_workspaces(id)

Delete Workspace entity

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Workspace entity
        api_response = api_instance.delete_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_workspaces: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;earlyAccess==someString;parent.id==321",
    }
    try:
        # Delete Workspace entity
        api_response = api_instance.delete_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->delete_entity_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_workspaces.ApiResponseFor204) | Successfully deleted

#### delete_entity_workspaces.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_color_palettes**
<a id="get_all_entities_color_palettes"></a>
> JsonApiColorPaletteOutList get_all_entities_color_palettes()

Get all Color Pallettes

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_color_palette_out_list import JsonApiColorPaletteOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get all Color Pallettes
        api_response = api_instance.get_all_entities_color_palettes(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_color_palettes.ApiResponseFor200) | Request successfully processed

#### get_all_entities_color_palettes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteOutList**](../../models/JsonApiColorPaletteOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_csp_directives**
<a id="get_all_entities_csp_directives"></a>
> JsonApiCspDirectiveOutList get_all_entities_csp_directives()

Get CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_csp_directive_out_list import JsonApiCspDirectiveOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=sources==v1,v2,v3",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get CSP Directives
        api_response = api_instance.get_all_entities_csp_directives(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_csp_directives.ApiResponseFor200) | Request successfully processed

#### get_all_entities_csp_directives.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveOutList**](../../models/JsonApiCspDirectiveOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_data_source_identifiers**
<a id="get_all_entities_data_source_identifiers"></a>
> JsonApiDataSourceIdentifierOutList get_all_entities_data_source_identifiers()

Get all Data Source Identifiers

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;schema==someString",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get all Data Source Identifiers
        api_response = api_instance.get_all_entities_data_source_identifiers(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_data_source_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_data_source_identifiers.ApiResponseFor200) | Request successfully processed

#### get_all_entities_data_source_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceIdentifierOutList**](../../models/JsonApiDataSourceIdentifierOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_data_sources**
<a id="get_all_entities_data_sources"></a>
> JsonApiDataSourceOutList get_all_entities_data_sources()

Get Data Source entities

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_out_list import JsonApiDataSourceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source entities
        api_response = api_instance.get_all_entities_data_sources(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_data_sources.ApiResponseFor200) | Request successfully processed

#### get_all_entities_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutList**](../../models/JsonApiDataSourceOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_entitlements**
<a id="get_all_entities_entitlements"></a>
> JsonApiEntitlementOutList get_all_entities_entitlements()

Get Entitlements

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_entitlement_out_list import JsonApiEntitlementOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=value==someString;expiry==LocalDateValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get Entitlements
        api_response = api_instance.get_all_entities_entitlements(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_entitlements: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_entitlements.ApiResponseFor200) | Request successfully processed

#### get_all_entities_entitlements.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiEntitlementOutList**](../../models/JsonApiEntitlementOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_organization_settings**
<a id="get_all_entities_organization_settings"></a>
> JsonApiOrganizationSettingOutList get_all_entities_organization_settings()

Get Organization entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_organization_setting_out_list import JsonApiOrganizationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get Organization entities
        api_response = api_instance.get_all_entities_organization_settings(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_organization_settings.ApiResponseFor200) | Request successfully processed

#### get_all_entities_organization_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingOutList**](../../models/JsonApiOrganizationSettingOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_themes**
<a id="get_all_entities_themes"></a>
> JsonApiThemeOutList get_all_entities_themes()

Get all Theming entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_theme_out_list import JsonApiThemeOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get all Theming entities
        api_response = api_instance.get_all_entities_themes(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_themes.ApiResponseFor200) | Request successfully processed

#### get_all_entities_themes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeOutList**](../../models/JsonApiThemeOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_user_groups**
<a id="get_all_entities_user_groups"></a>
> JsonApiUserGroupOutList get_all_entities_user_groups()

Get UserGroup entities

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_group_out_list import JsonApiUserGroupOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString",
        'include': [
        "include=parents"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get UserGroup entities
        api_response = api_instance.get_all_entities_user_groups(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "parents", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_user_groups.ApiResponseFor200) | Request successfully processed

#### get_all_entities_user_groups.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupOutList**](../../models/JsonApiUserGroupOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_users**
<a id="get_all_entities_users"></a>
> JsonApiUserOutList get_all_entities_users()

Get User entities

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_out_list import JsonApiUserOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=authenticationId==someString;firstname==someString",
        'include': [
        "include=userGroups"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
    }
    try:
        # Get User entities
        api_response = api_instance.get_all_entities_users(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_users.ApiResponseFor200) | Request successfully processed

#### get_all_entities_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserOutList**](../../models/JsonApiUserOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_workspaces**
<a id="get_all_entities_workspaces"></a>
> JsonApiWorkspaceOutList get_all_entities_workspaces()

Get Workspace entities

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_workspace_out_list import JsonApiWorkspaceOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "filter=name==someString;earlyAccess==someString;parent.id==321",
        'include': [
        "include=parent"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=config,permissions,all"
    ],
    }
    try:
        # Get Workspace entities
        api_response = api_instance.get_all_entities_workspaces(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_all_entities_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "parent", "ALL", ] 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["config", "permissions", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_workspaces.ApiResponseFor200) | Request successfully processed

#### get_all_entities_workspaces.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceOutList**](../../models/JsonApiWorkspaceOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_color_palettes**
<a id="get_entity_color_palettes"></a>
> JsonApiColorPaletteOutDocument get_entity_color_palettes(id)

Get Color Pallette

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_color_palettes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    try:
        # Get Color Pallette
        api_response = api_instance.get_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_color_palettes.ApiResponseFor200) | Request successfully processed

#### get_entity_color_palettes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteOutDocument**](../../models/JsonApiColorPaletteOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_csp_directives**
<a id="get_entity_csp_directives"></a>
> JsonApiCspDirectiveOutDocument get_entity_csp_directives(id)

Get CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_csp_directives: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=sources==v1,v2,v3",
    }
    try:
        # Get CSP Directives
        api_response = api_instance.get_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_csp_directives.ApiResponseFor200) | Request successfully processed

#### get_entity_csp_directives.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveOutDocument**](../../models/JsonApiCspDirectiveOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_data_source_identifiers**
<a id="get_entity_data_source_identifiers"></a>
> JsonApiDataSourceIdentifierOutDocument get_entity_data_source_identifiers(id)

Get Data Source Identifier

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_identifier_out_document import JsonApiDataSourceIdentifierOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_source_identifiers: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;schema==someString",
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source Identifier
        api_response = api_instance.get_entity_data_source_identifiers(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_source_identifiers: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_data_source_identifiers.ApiResponseFor200) | Request successfully processed

#### get_entity_data_source_identifiers.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceIdentifierOutDocument**](../../models/JsonApiDataSourceIdentifierOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_data_sources**
<a id="get_entity_data_sources"></a>
> JsonApiDataSourceOutDocument get_entity_data_sources(id)

Get Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
        'metaInclude': [
        "metaInclude=permissions,all"
    ],
    }
    try:
        # Get Data Source entity
        api_response = api_instance.get_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["permissions", "all", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### get_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_entitlements**
<a id="get_entity_entitlements"></a>
> JsonApiEntitlementOutDocument get_entity_entitlements(id)

Get Entitlement

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_entitlement_out_document import JsonApiEntitlementOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_entitlements: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=value==someString;expiry==LocalDateValue",
    }
    try:
        # Get Entitlement
        api_response = api_instance.get_entity_entitlements(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_entitlements: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_entitlements.ApiResponseFor200) | Request successfully processed

#### get_entity_entitlements.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiEntitlementOutDocument**](../../models/JsonApiEntitlementOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_organization_settings**
<a id="get_entity_organization_settings"></a>
> JsonApiOrganizationSettingOutDocument get_entity_organization_settings(id)

Get Organization entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_organization_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    try:
        # Get Organization entity
        api_response = api_instance.get_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_organization_settings.ApiResponseFor200) | Request successfully processed

#### get_entity_organization_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingOutDocument**](../../models/JsonApiOrganizationSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_themes**
<a id="get_entity_themes"></a>
> JsonApiThemeOutDocument get_entity_themes(id)

Get Theming

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_themes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    try:
        # Get Theming
        api_response = api_instance.get_entity_themes(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_themes.ApiResponseFor200) | Request successfully processed

#### get_entity_themes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeOutDocument**](../../models/JsonApiThemeOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_user_groups**
<a id="get_entity_user_groups"></a>
> JsonApiUserGroupOutDocument get_entity_user_groups(id)

Get UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_groups: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString",
        'include': [
        "include=parents"
    ],
    }
    try:
        # Get UserGroup entity
        api_response = api_instance.get_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "parents", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_user_groups.ApiResponseFor200) | Request successfully processed

#### get_entity_user_groups.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupOutDocument**](../../models/JsonApiUserGroupOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_users**
<a id="get_entity_users"></a>
> JsonApiUserOutDocument get_entity_users(id)

Get User entity

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_users: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=authenticationId==someString;firstname==someString",
        'include': [
        "include=userGroups"
    ],
    }
    try:
        # Get User entity
        api_response = api_instance.get_entity_users(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_users.ApiResponseFor200) | Request successfully processed

#### get_entity_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserOutDocument**](../../models/JsonApiUserOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_workspaces**
<a id="get_entity_workspaces"></a>
> JsonApiWorkspaceOutDocument get_entity_workspaces(id)

Get Workspace entity

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_workspaces: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;earlyAccess==someString;parent.id==321",
        'include': [
        "include=parent"
    ],
        'metaInclude': [
        "metaInclude=config,permissions,all"
    ],
    }
    try:
        # Get Workspace entity
        api_response = api_instance.get_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->get_entity_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "parent", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["config", "permissions", "all", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_workspaces.ApiResponseFor200) | Request successfully processed

#### get_entity_workspaces.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceOutDocument**](../../models/JsonApiWorkspaceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_color_palettes**
<a id="patch_entity_color_palettes"></a>
> JsonApiColorPaletteOutDocument patch_entity_color_palettes(idjson_api_color_palette_patch_document)

Patch Color Pallette

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_color_palette_patch_document import JsonApiColorPalettePatchDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiColorPalettePatchDocument(
        data=JsonApiColorPalettePatch(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    )
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_color_palettes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    body = JsonApiColorPalettePatchDocument(
        data=JsonApiColorPalettePatch(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    )
    try:
        # Patch Color Pallette
        api_response = api_instance.patch_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPalettePatchDocument**](../../models/JsonApiColorPalettePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_color_palettes.ApiResponseFor200) | Request successfully processed

#### patch_entity_color_palettes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteOutDocument**](../../models/JsonApiColorPaletteOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_csp_directives**
<a id="patch_entity_csp_directives"></a>
> JsonApiCspDirectiveOutDocument patch_entity_csp_directives(idjson_api_csp_directive_patch_document)

Patch CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiCspDirectivePatchDocument(
        data=JsonApiCspDirectivePatch(
            attributes=dict(
                sources=[
                    "sources_example"
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    )
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_csp_directives: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=sources==v1,v2,v3",
    }
    body = JsonApiCspDirectivePatchDocument(
        data=JsonApiCspDirectivePatch(
            attributes=dict(
                sources=[
                    "sources_example"
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    )
    try:
        # Patch CSP Directives
        api_response = api_instance.patch_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectivePatchDocument**](../../models/JsonApiCspDirectivePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_csp_directives.ApiResponseFor200) | Request successfully processed

#### patch_entity_csp_directives.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveOutDocument**](../../models/JsonApiCspDirectiveOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_data_sources**
<a id="patch_entity_data_sources"></a>
> JsonApiDataSourceOutDocument patch_entity_data_sources(idjson_api_data_source_patch_document)

Patch Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiDataSourcePatchDocument(
        data=JsonApiDataSourcePatch(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    body = JsonApiDataSourcePatchDocument(
        data=JsonApiDataSourcePatch(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Patch Data Source entity
        api_response = api_instance.patch_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourcePatchDocument**](../../models/JsonApiDataSourcePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### patch_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_organization_settings**
<a id="patch_entity_organization_settings"></a>
> JsonApiOrganizationSettingOutDocument patch_entity_organization_settings(idjson_api_organization_setting_patch_document)

Patch Organization entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from gooddata_api_client.model.json_api_organization_setting_patch_document import JsonApiOrganizationSettingPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiOrganizationSettingPatchDocument(
        data=JsonApiOrganizationSettingPatch(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    )
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_organization_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    body = JsonApiOrganizationSettingPatchDocument(
        data=JsonApiOrganizationSettingPatch(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    )
    try:
        # Patch Organization entity
        api_response = api_instance.patch_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingPatchDocument**](../../models/JsonApiOrganizationSettingPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_organization_settings.ApiResponseFor200) | Request successfully processed

#### patch_entity_organization_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingOutDocument**](../../models/JsonApiOrganizationSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_themes**
<a id="patch_entity_themes"></a>
> JsonApiThemeOutDocument patch_entity_themes(idjson_api_theme_patch_document)

Patch Theming

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_theme_patch_document import JsonApiThemePatchDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiThemePatchDocument(
        data=JsonApiThemePatch(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    )
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_themes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    body = JsonApiThemePatchDocument(
        data=JsonApiThemePatch(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    )
    try:
        # Patch Theming
        api_response = api_instance.patch_entity_themes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemePatchDocument**](../../models/JsonApiThemePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_themes.ApiResponseFor200) | Request successfully processed

#### patch_entity_themes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeOutDocument**](../../models/JsonApiThemeOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_user_groups**
<a id="patch_entity_user_groups"></a>
> JsonApiUserGroupOutDocument patch_entity_user_groups(idjson_api_user_group_patch_document)

Patch UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from gooddata_api_client.model.json_api_user_group_patch_document import JsonApiUserGroupPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiUserGroupPatchDocument(
        data=JsonApiUserGroupPatch(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_user_groups: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString",
        'include': [
        "include=parents"
    ],
    }
    body = JsonApiUserGroupPatchDocument(
        data=JsonApiUserGroupPatch(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Patch UserGroup entity
        api_response = api_instance.patch_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupPatchDocument**](../../models/JsonApiUserGroupPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "parents", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_user_groups.ApiResponseFor200) | Request successfully processed

#### patch_entity_user_groups.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupOutDocument**](../../models/JsonApiUserGroupOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_users**
<a id="patch_entity_users"></a>
> JsonApiUserOutDocument patch_entity_users(idjson_api_user_patch_document)

Patch User entity

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from gooddata_api_client.model.json_api_user_patch_document import JsonApiUserPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiUserPatchDocument(
        data=JsonApiUserPatch(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_users: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=authenticationId==someString;firstname==someString",
        'include': [
        "include=userGroups"
    ],
    }
    body = JsonApiUserPatchDocument(
        data=JsonApiUserPatch(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Patch User entity
        api_response = api_instance.patch_entity_users(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserPatchDocument**](../../models/JsonApiUserPatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_users.ApiResponseFor200) | Request successfully processed

#### patch_entity_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserOutDocument**](../../models/JsonApiUserOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_workspaces**
<a id="patch_entity_workspaces"></a>
> JsonApiWorkspaceOutDocument patch_entity_workspaces(idjson_api_workspace_patch_document)

Patch Workspace entity

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_patch_document import JsonApiWorkspacePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiWorkspacePatchDocument(
        data=JsonApiWorkspacePatch(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_workspaces: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;earlyAccess==someString;parent.id==321",
        'include': [
        "include=parent"
    ],
    }
    body = JsonApiWorkspacePatchDocument(
        data=JsonApiWorkspacePatch(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Patch Workspace entity
        api_response = api_instance.patch_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->patch_entity_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspacePatchDocument**](../../models/JsonApiWorkspacePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "parent", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_workspaces.ApiResponseFor200) | Request successfully processed

#### patch_entity_workspaces.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceOutDocument**](../../models/JsonApiWorkspaceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_color_palettes**
<a id="update_entity_color_palettes"></a>
> JsonApiColorPaletteOutDocument update_entity_color_palettes(idjson_api_color_palette_in_document)

Put Color Pallette

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_color_palette_in_document import JsonApiColorPaletteInDocument
from gooddata_api_client.model.json_api_color_palette_out_document import JsonApiColorPaletteOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiColorPaletteInDocument(
        data=JsonApiColorPaletteIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    )
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_color_palettes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    body = JsonApiColorPaletteInDocument(
        data=JsonApiColorPaletteIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="colorPalette",
        ),
    )
    try:
        # Put Color Pallette
        api_response = api_instance.update_entity_color_palettes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_color_palettes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteInDocument**](../../models/JsonApiColorPaletteInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_color_palettes.ApiResponseFor200) | Request successfully processed

#### update_entity_color_palettes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiColorPaletteOutDocument**](../../models/JsonApiColorPaletteOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_csp_directives**
<a id="update_entity_csp_directives"></a>
> JsonApiCspDirectiveOutDocument update_entity_csp_directives(idjson_api_csp_directive_in_document)

Put CSP Directives

 Context Security Police Directive

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument
from gooddata_api_client.model.json_api_csp_directive_in_document import JsonApiCspDirectiveInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=dict(
                sources=[
                    "sources_example"
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    )
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_csp_directives: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=sources==v1,v2,v3",
    }
    body = JsonApiCspDirectiveInDocument(
        data=JsonApiCspDirectiveIn(
            attributes=dict(
                sources=[
                    "sources_example"
                ],
            ),
            id="id1",
            type="cspDirective",
        ),
    )
    try:
        # Put CSP Directives
        api_response = api_instance.update_entity_csp_directives(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_csp_directives: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveInDocument**](../../models/JsonApiCspDirectiveInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_csp_directives.ApiResponseFor200) | Request successfully processed

#### update_entity_csp_directives.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiCspDirectiveOutDocument**](../../models/JsonApiCspDirectiveOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_data_sources**
<a id="update_entity_data_sources"></a>
> JsonApiDataSourceOutDocument update_entity_data_sources(idjson_api_data_source_in_document)

Put Data Source entity

Data Source - represents data source for the workspace

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_data_source_in_document import JsonApiDataSourceInDocument
from gooddata_api_client.model.json_api_data_source_out_document import JsonApiDataSourceOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_data_sources: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;type==DatabaseTypeValue",
    }
    body = JsonApiDataSourceInDocument(
        data=JsonApiDataSourceIn(
            attributes=dict(
                cache_path=[
                    "cache_path_example"
                ],
                enable_caching=False,
                name="name_example",
                parameters=[
                    dict(
                        name="name_example",
                        value="value_example",
                    )
                ],
                password="password_example",
                schema="schema_example",
                token="token_example",
                type="POSTGRESQL",
                url="url_example",
                username="username_example",
            ),
            id="id1",
            type="dataSource",
        ),
    )
    try:
        # Put Data Source entity
        api_response = api_instance.update_entity_data_sources(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_data_sources: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceInDocument**](../../models/JsonApiDataSourceInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_data_sources.ApiResponseFor200) | Request successfully processed

#### update_entity_data_sources.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDataSourceOutDocument**](../../models/JsonApiDataSourceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_organization_settings**
<a id="update_entity_organization_settings"></a>
> JsonApiOrganizationSettingOutDocument update_entity_organization_settings(idjson_api_organization_setting_in_document)

Put Organization entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_organization_setting_in_document import JsonApiOrganizationSettingInDocument
from gooddata_api_client.model.json_api_organization_setting_out_document import JsonApiOrganizationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    )
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_organization_settings: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=content==JsonNodeValue;type==SettingConfigurationValue",
    }
    body = JsonApiOrganizationSettingInDocument(
        data=JsonApiOrganizationSettingIn(
            attributes=dict(
                content=dict(),
                type="TIMEZONE",
            ),
            id="id1",
            type="organizationSetting",
        ),
    )
    try:
        # Put Organization entity
        api_response = api_instance.update_entity_organization_settings(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_organization_settings: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingInDocument**](../../models/JsonApiOrganizationSettingInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_organization_settings.ApiResponseFor200) | Request successfully processed

#### update_entity_organization_settings.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiOrganizationSettingOutDocument**](../../models/JsonApiOrganizationSettingOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_themes**
<a id="update_entity_themes"></a>
> JsonApiThemeOutDocument update_entity_themes(idjson_api_theme_in_document)

Put Theming

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_theme_in_document import JsonApiThemeInDocument
from gooddata_api_client.model.json_api_theme_out_document import JsonApiThemeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiThemeInDocument(
        data=JsonApiThemeIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    )
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_themes: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;content==JsonNodeValue",
    }
    body = JsonApiThemeInDocument(
        data=JsonApiThemeIn(
            attributes=dict(
                content=dict(),
                name="name_example",
            ),
            id="id1",
            type="theme",
        ),
    )
    try:
        # Put Theming
        api_response = api_instance.update_entity_themes(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_themes: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeInDocument**](../../models/JsonApiThemeInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_themes.ApiResponseFor200) | Request successfully processed

#### update_entity_themes.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiThemeOutDocument**](../../models/JsonApiThemeOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_user_groups**
<a id="update_entity_user_groups"></a>
> JsonApiUserGroupOutDocument update_entity_user_groups(idjson_api_user_group_in_document)

Put UserGroup entity

User Group - creates tree-like structure for categorizing users

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_group_in_document import JsonApiUserGroupInDocument
from gooddata_api_client.model.json_api_user_group_out_document import JsonApiUserGroupOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_user_groups: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString",
        'include': [
        "include=parents"
    ],
    }
    body = JsonApiUserGroupInDocument(
        data=JsonApiUserGroupIn(
            attributes=dict(
                name="name_example",
            ),
            id="id1",
            relationships=dict(
                parents=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="userGroup",
        ),
    )
    try:
        # Put UserGroup entity
        api_response = api_instance.update_entity_user_groups(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_user_groups: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupInDocument**](../../models/JsonApiUserGroupInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "parents", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_user_groups.ApiResponseFor200) | Request successfully processed

#### update_entity_user_groups.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserGroupOutDocument**](../../models/JsonApiUserGroupOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_users**
<a id="update_entity_users"></a>
> JsonApiUserOutDocument update_entity_users(idjson_api_user_in_document)

Put User entity

User - represents entity interacting with platform

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_user_in_document import JsonApiUserInDocument
from gooddata_api_client.model.json_api_user_out_document import JsonApiUserOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_users: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=authenticationId==someString;firstname==someString",
        'include': [
        "include=userGroups"
    ],
    }
    body = JsonApiUserInDocument(
        data=JsonApiUserIn(
            attributes=dict(
                authentication_id="authentication_id_example",
                email="email_example",
                firstname="firstname_example",
                lastname="lastname_example",
            ),
            id="id1",
            relationships=dict(
                user_groups=dict(
                    data=JsonApiUserGroupToManyLinkage([
                        JsonApiUserGroupLinkage(
                            id="id_example",
                            type="userGroup",
                        )
                    ]),
                ),
            ),
            type="user",
        ),
    )
    try:
        # Put User entity
        api_response = api_instance.update_entity_users(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_users: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserInDocument**](../../models/JsonApiUserInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["userGroups", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_users.ApiResponseFor200) | Request successfully processed

#### update_entity_users.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiUserOutDocument**](../../models/JsonApiUserOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_workspaces**
<a id="update_entity_workspaces"></a>
> JsonApiWorkspaceOutDocument update_entity_workspaces(idjson_api_workspace_in_document)

Put Workspace entity

Space of the shared interest

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import organization_model_controller_api
from gooddata_api_client.model.json_api_workspace_out_document import JsonApiWorkspaceOutDocument
from gooddata_api_client.model.json_api_workspace_in_document import JsonApiWorkspaceInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = organization_model_controller_api.OrganizationModelControllerApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_workspaces: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "filter=name==someString;earlyAccess==someString;parent.id==321",
        'include': [
        "include=parent"
    ],
    }
    body = JsonApiWorkspaceInDocument(
        data=JsonApiWorkspaceIn(
            attributes=dict(
                description="description_example",
                early_access="early_access_example",
                name="name_example",
                prefix="/6bUUGjjNSwg0_bs",
            ),
            id="id1",
            relationships=dict(
                parent=dict(
                    data=JsonApiWorkspaceToOneLinkage(None),
                ),
            ),
            type="workspace",
        ),
    )
    try:
        # Put Workspace entity
        api_response = api_instance.update_entity_workspaces(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OrganizationModelControllerApi->update_entity_workspaces: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/vnd.gooddata.api+json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceInDocument**](../../models/JsonApiWorkspaceInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["workspaces", "parent", "ALL", ] 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_workspaces.ApiResponseFor200) | Request successfully processed

#### update_entity_workspaces.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiWorkspaceOutDocument**](../../models/JsonApiWorkspaceOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

