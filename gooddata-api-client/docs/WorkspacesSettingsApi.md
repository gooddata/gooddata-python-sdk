# gooddata_api_client.WorkspacesSettingsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_custom_application_settings**](WorkspacesSettingsApi.md#create_entity_custom_application_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Post Custom Application Settings
[**create_entity_workspace_settings**](WorkspacesSettingsApi.md#create_entity_workspace_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Post Settings for Workspaces
[**delete_entity_custom_application_settings**](WorkspacesSettingsApi.md#delete_entity_custom_application_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Delete a Custom Application Setting
[**delete_entity_workspace_settings**](WorkspacesSettingsApi.md#delete_entity_workspace_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Delete a Setting for Workspace
[**get_all_entities_custom_application_settings**](WorkspacesSettingsApi.md#get_all_entities_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings | Get all Custom Application Settings
[**get_all_entities_workspace_settings**](WorkspacesSettingsApi.md#get_all_entities_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings | Get all Setting for Workspaces
[**get_entity_custom_application_settings**](WorkspacesSettingsApi.md#get_entity_custom_application_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Get a Custom Application Setting
[**get_entity_workspace_settings**](WorkspacesSettingsApi.md#get_entity_workspace_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Get a Setting for Workspace
[**patch_entity_custom_application_settings**](WorkspacesSettingsApi.md#patch_entity_custom_application_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Patch a Custom Application Setting
[**patch_entity_workspace_settings**](WorkspacesSettingsApi.md#patch_entity_workspace_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Patch a Setting for Workspace
[**update_entity_custom_application_settings**](WorkspacesSettingsApi.md#update_entity_custom_application_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/customApplicationSettings/{objectId} | Put a Custom Application Setting
[**update_entity_workspace_settings**](WorkspacesSettingsApi.md#update_entity_workspace_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceSettings/{objectId} | Put a Setting for a Workspace
[**workspace_resolve_all_settings**](WorkspacesSettingsApi.md#workspace_resolve_all_settings) | **GET** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for all settings.
[**workspace_resolve_settings**](WorkspacesSettingsApi.md#workspace_resolve_settings) | **POST** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for selected settings.


# **create_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document)

Post Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from gooddata_api_client.model.json_api_custom_application_setting_post_optional_id_document import JsonApiCustomApplicationSettingPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_custom_application_setting_post_optional_id_document = JsonApiCustomApplicationSettingPostOptionalIdDocument(
        data=JsonApiCustomApplicationSettingPostOptionalId(
            attributes=JsonApiCustomApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingPostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Custom Application Settings
        api_response = api_instance.create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->create_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Custom Application Settings
        api_response = api_instance.create_entity_custom_application_settings(workspace_id, json_api_custom_application_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->create_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_custom_application_setting_post_optional_id_document** | [**JsonApiCustomApplicationSettingPostOptionalIdDocument**](JsonApiCustomApplicationSettingPostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

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

# **create_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document)

Post Settings for Workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_workspace_setting_post_optional_id_document import JsonApiWorkspaceSettingPostOptionalIdDocument
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_setting_post_optional_id_document = JsonApiWorkspaceSettingPostOptionalIdDocument(
        data=JsonApiWorkspaceSettingPostOptionalId(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingPostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Settings for Workspaces
        api_response = api_instance.create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->create_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspaces
        api_response = api_instance.create_entity_workspace_settings(workspace_id, json_api_workspace_setting_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->create_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_setting_post_optional_id_document** | [**JsonApiWorkspaceSettingPostOptionalIdDocument**](JsonApiWorkspaceSettingPostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

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

# **delete_entity_custom_application_settings**
> delete_entity_custom_application_settings(workspace_id, object_id)

Delete a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->delete_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Custom Application Setting
        api_instance.delete_entity_custom_application_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->delete_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
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

# **delete_entity_workspace_settings**
> delete_entity_workspace_settings(workspace_id, object_id)

Delete a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->delete_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Setting for Workspace
        api_instance.delete_entity_workspace_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->delete_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
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

# **get_all_entities_custom_application_settings**
> JsonApiCustomApplicationSettingOutList get_all_entities_custom_application_settings(workspace_id)

Get all Custom Application Settings

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_custom_application_setting_out_list import JsonApiCustomApplicationSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Custom Application Settings
        api_response = api_instance.get_all_entities_custom_application_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_all_entities_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Custom Application Settings
        api_response = api_instance.get_all_entities_custom_application_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_all_entities_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutList**](JsonApiCustomApplicationSettingOutList.md)

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

# **get_all_entities_workspace_settings**
> JsonApiWorkspaceSettingOutList get_all_entities_workspace_settings(workspace_id)

Get all Setting for Workspaces

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_workspace_setting_out_list import JsonApiWorkspaceSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Setting for Workspaces
        api_response = api_instance.get_all_entities_workspace_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_all_entities_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Setting for Workspaces
        api_response = api_instance.get_all_entities_workspace_settings(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_all_entities_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutList**](JsonApiWorkspaceSettingOutList.md)

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

# **get_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument get_entity_custom_application_settings(workspace_id, object_id)

Get a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Custom Application Setting
        api_response = api_instance.get_entity_custom_application_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Custom Application Setting
        api_response = api_instance.get_entity_custom_application_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

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

# **get_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument get_entity_workspace_settings(workspace_id, object_id)

Get a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Setting for Workspace
        api_response = api_instance.get_entity_workspace_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace
        api_response = api_instance.get_entity_workspace_settings(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->get_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

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

# **patch_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document)

Patch a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_custom_application_setting_patch_document import JsonApiCustomApplicationSettingPatchDocument
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_custom_application_setting_patch_document = JsonApiCustomApplicationSettingPatchDocument(
        data=JsonApiCustomApplicationSettingPatch(
            attributes=JsonApiCustomApplicationSettingPatchAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingPatchDocument | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Custom Application Setting
        api_response = api_instance.patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->patch_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Custom Application Setting
        api_response = api_instance.patch_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->patch_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_custom_application_setting_patch_document** | [**JsonApiCustomApplicationSettingPatchDocument**](JsonApiCustomApplicationSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

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

# **patch_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document)

Patch a Setting for Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from gooddata_api_client.model.json_api_workspace_setting_patch_document import JsonApiWorkspaceSettingPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_setting_patch_document = JsonApiWorkspaceSettingPatchDocument(
        data=JsonApiWorkspaceSettingPatch(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingPatchDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Setting for Workspace
        api_response = api_instance.patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->patch_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Setting for Workspace
        api_response = api_instance.patch_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->patch_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_setting_patch_document** | [**JsonApiWorkspaceSettingPatchDocument**](JsonApiWorkspaceSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

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

# **update_entity_custom_application_settings**
> JsonApiCustomApplicationSettingOutDocument update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document)

Put a Custom Application Setting

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_custom_application_setting_in_document import JsonApiCustomApplicationSettingInDocument
from gooddata_api_client.model.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_custom_application_setting_in_document = JsonApiCustomApplicationSettingInDocument(
        data=JsonApiCustomApplicationSettingIn(
            attributes=JsonApiCustomApplicationSettingInAttributes(
                application_name="application_name_example",
                content={},
            ),
            id="id1",
            type="customApplicationSetting",
        ),
    ) # JsonApiCustomApplicationSettingInDocument | 
    filter = "filter=applicationName==someString;content==JsonNodeValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Custom Application Setting
        api_response = api_instance.update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->update_entity_custom_application_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Custom Application Setting
        api_response = api_instance.update_entity_custom_application_settings(workspace_id, object_id, json_api_custom_application_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->update_entity_custom_application_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_custom_application_setting_in_document** | [**JsonApiCustomApplicationSettingInDocument**](JsonApiCustomApplicationSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiCustomApplicationSettingOutDocument**](JsonApiCustomApplicationSettingOutDocument.md)

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

# **update_entity_workspace_settings**
> JsonApiWorkspaceSettingOutDocument update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document)

Put a Setting for a Workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.json_api_workspace_setting_in_document import JsonApiWorkspaceSettingInDocument
from gooddata_api_client.model.json_api_workspace_setting_out_document import JsonApiWorkspaceSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_setting_in_document = JsonApiWorkspaceSettingInDocument(
        data=JsonApiWorkspaceSettingIn(
            attributes=JsonApiOrganizationSettingInAttributes(
                content={},
                type="TIMEZONE",
            ),
            id="id1",
            type="workspaceSetting",
        ),
    ) # JsonApiWorkspaceSettingInDocument | 
    filter = "filter=content==JsonNodeValue;type==SettingConfigurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Setting for a Workspace
        api_response = api_instance.update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->update_entity_workspace_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Setting for a Workspace
        api_response = api_instance.update_entity_workspace_settings(workspace_id, object_id, json_api_workspace_setting_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->update_entity_workspace_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_setting_in_document** | [**JsonApiWorkspaceSettingInDocument**](JsonApiWorkspaceSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceSettingOutDocument**](JsonApiWorkspaceSettingOutDocument.md)

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

# **workspace_resolve_all_settings**
> [ResolvedSetting] workspace_resolve_all_settings(workspace_id)

Values for all settings.

Resolves values for all settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Values for all settings.
        api_response = api_instance.workspace_resolve_all_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->workspace_resolve_all_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_settings**
> [ResolvedSetting] workspace_resolve_settings(workspace_id, resolve_settings_request)

Values for selected settings.

Resolves value for selected settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspaces_settings_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspaces_settings_api.WorkspacesSettingsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings.
        api_response = api_instance.workspace_resolve_settings(workspace_id, resolve_settings_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspacesSettingsApi->workspace_resolve_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

