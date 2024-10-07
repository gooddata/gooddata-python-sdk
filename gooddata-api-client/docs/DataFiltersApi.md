# gooddata_api_client.DataFiltersApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_user_data_filters**](DataFiltersApi.md#create_entity_user_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Post User Data Filters
[**create_entity_workspace_data_filter_settings**](DataFiltersApi.md#create_entity_workspace_data_filter_settings) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Post Settings for Workspace Data Filters
[**create_entity_workspace_data_filters**](DataFiltersApi.md#create_entity_workspace_data_filters) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Post Workspace Data Filters
[**delete_entity_user_data_filters**](DataFiltersApi.md#delete_entity_user_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Delete a User Data Filter
[**delete_entity_workspace_data_filter_settings**](DataFiltersApi.md#delete_entity_workspace_data_filter_settings) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Delete a Settings for Workspace Data Filter
[**delete_entity_workspace_data_filters**](DataFiltersApi.md#delete_entity_workspace_data_filters) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Delete a Workspace Data Filter
[**get_all_entities_user_data_filters**](DataFiltersApi.md#get_all_entities_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters | Get all User Data Filters
[**get_all_entities_workspace_data_filter_settings**](DataFiltersApi.md#get_all_entities_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | Get all Settings for Workspace Data Filters
[**get_all_entities_workspace_data_filters**](DataFiltersApi.md#get_all_entities_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters | Get all Workspace Data Filters
[**get_entity_user_data_filters**](DataFiltersApi.md#get_entity_user_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Get a User Data Filter
[**get_entity_workspace_data_filter_settings**](DataFiltersApi.md#get_entity_workspace_data_filter_settings) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Get a Setting for Workspace Data Filter
[**get_entity_workspace_data_filters**](DataFiltersApi.md#get_entity_workspace_data_filters) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Get a Workspace Data Filter
[**get_workspace_data_filters_layout**](DataFiltersApi.md#get_workspace_data_filters_layout) | **GET** /api/v1/layout/workspaceDataFilters | Get workspace data filters for all workspaces
[**patch_entity_user_data_filters**](DataFiltersApi.md#patch_entity_user_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Patch a User Data Filter
[**patch_entity_workspace_data_filter_settings**](DataFiltersApi.md#patch_entity_workspace_data_filter_settings) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Patch a Settings for Workspace Data Filter
[**patch_entity_workspace_data_filters**](DataFiltersApi.md#patch_entity_workspace_data_filters) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Patch a Workspace Data Filter
[**set_workspace_data_filters_layout**](DataFiltersApi.md#set_workspace_data_filters_layout) | **PUT** /api/v1/layout/workspaceDataFilters | Set all workspace data filters
[**update_entity_user_data_filters**](DataFiltersApi.md#update_entity_user_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/userDataFilters/{objectId} | Put a User Data Filter
[**update_entity_workspace_data_filter_settings**](DataFiltersApi.md#update_entity_workspace_data_filter_settings) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | Put a Settings for Workspace Data Filter
[**update_entity_workspace_data_filters**](DataFiltersApi.md#update_entity_workspace_data_filters) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | Put a Workspace Data Filter


# **create_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document)

Post User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_post_optional_id_document import JsonApiUserDataFilterPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_user_data_filter_post_optional_id_document = JsonApiUserDataFilterPostOptionalIdDocument(
        data=JsonApiUserDataFilterPostOptionalId(
            attributes=JsonApiUserDataFilterInAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterPostOptionalIdDocument | 
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post User Data Filters
        api_response = api_instance.create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post User Data Filters
        api_response = api_instance.create_entity_user_data_filters(workspace_id, json_api_user_data_filter_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_user_data_filter_post_optional_id_document** | [**JsonApiUserDataFilterPostOptionalIdDocument**](JsonApiUserDataFilterPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

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

# **create_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document)

Post Settings for Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_in_document import JsonApiWorkspaceDataFilterSettingInDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_data_filter_setting_in_document = JsonApiWorkspaceDataFilterSettingInDocument(
        data=JsonApiWorkspaceDataFilterSettingIn(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingInDocument | 
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Settings for Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Settings for Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filter_settings(workspace_id, json_api_workspace_data_filter_setting_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_data_filter_setting_in_document** | [**JsonApiWorkspaceDataFilterSettingInDocument**](JsonApiWorkspaceDataFilterSettingInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

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

# **create_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document)

Post Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Data Filters
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->create_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

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

# **delete_entity_user_data_filters**
> delete_entity_user_data_filters(workspace_id, object_id)

Delete a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a User Data Filter
        api_instance.delete_entity_user_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_user_data_filters: %s\n" % e)
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

# **delete_entity_workspace_data_filter_settings**
> delete_entity_workspace_data_filter_settings(workspace_id, object_id)

Delete a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Settings for Workspace Data Filter
        api_instance.delete_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_workspace_data_filter_settings: %s\n" % e)
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

# **delete_entity_workspace_data_filters**
> delete_entity_workspace_data_filters(workspace_id, object_id)

Delete a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete a Workspace Data Filter
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->delete_entity_workspace_data_filters: %s\n" % e)
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

# **get_all_entities_user_data_filters**
> JsonApiUserDataFilterOutList get_all_entities_user_data_filters(workspace_id)

Get all User Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_user_data_filter_out_list import JsonApiUserDataFilterOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all User Data Filters
        api_response = api_instance.get_all_entities_user_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all User Data Filters
        api_response = api_instance.get_all_entities_user_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutList**](JsonApiUserDataFilterOutList.md)

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

# **get_all_entities_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutList get_all_entities_workspace_data_filter_settings(workspace_id)

Get all Settings for Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_list import JsonApiWorkspaceDataFilterSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Settings for Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Settings for Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutList**](JsonApiWorkspaceDataFilterSettingOutList.md)

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

# **get_all_entities_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutList get_all_entities_workspace_data_filters(workspace_id)

Get all Workspace Data Filters

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_list import JsonApiWorkspaceDataFilterOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Data Filters
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_all_entities_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutList**](JsonApiWorkspaceDataFilterOutList.md)

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

# **get_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument get_entity_user_data_filters(workspace_id, object_id)

Get a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a User Data Filter
        api_response = api_instance.get_entity_user_data_filters(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a User Data Filter
        api_response = api_instance.get_entity_user_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

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

# **get_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument get_entity_workspace_data_filter_settings(workspace_id, object_id)

Get a Setting for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Setting for Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Setting for Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

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

# **get_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument get_entity_workspace_data_filters(workspace_id, object_id)

Get a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Data Filter
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

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

# **get_workspace_data_filters_layout**
> DeclarativeWorkspaceDataFilters get_workspace_data_filters_layout()

Get workspace data filters for all workspaces

Retrieve all workspaces and related workspace data filters (and their settings / values).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get workspace data filters for all workspaces
        api_response = api_instance.get_workspace_data_filters_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->get_workspace_data_filters_layout: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**DeclarativeWorkspaceDataFilters**](DeclarativeWorkspaceDataFilters.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all workspace data filters. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document)

Patch a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_patch_document import JsonApiUserDataFilterPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_user_data_filter_patch_document = JsonApiUserDataFilterPatchDocument(
        data=JsonApiUserDataFilterPatch(
            attributes=JsonApiUserDataFilterPatchAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterPatchDocument | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a User Data Filter
        api_response = api_instance.patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a User Data Filter
        api_response = api_instance.patch_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_user_data_filter_patch_document** | [**JsonApiUserDataFilterPatchDocument**](JsonApiUserDataFilterPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

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

# **patch_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document)

Patch a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_patch_document import JsonApiWorkspaceDataFilterSettingPatchDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_setting_patch_document = JsonApiWorkspaceDataFilterSettingPatchDocument(
        data=JsonApiWorkspaceDataFilterSettingPatch(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingPatchDocument | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Settings for Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Settings for Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_setting_patch_document** | [**JsonApiWorkspaceDataFilterSettingPatchDocument**](JsonApiWorkspaceDataFilterSettingPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

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

# **patch_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document)

Patch a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_patch_document import JsonApiWorkspaceDataFilterPatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_patch_document = JsonApiWorkspaceDataFilterPatchDocument(
        data=JsonApiWorkspaceDataFilterPatch(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterPatchDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Data Filter
        api_response = api_instance.patch_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->patch_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_patch_document** | [**JsonApiWorkspaceDataFilterPatchDocument**](JsonApiWorkspaceDataFilterPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

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

# **set_workspace_data_filters_layout**
> set_workspace_data_filters_layout(declarative_workspace_data_filters)

Set all workspace data filters

Sets workspace data filters in all workspaces in entire organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.declarative_workspace_data_filters import DeclarativeWorkspaceDataFilters
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    declarative_workspace_data_filters = DeclarativeWorkspaceDataFilters(
        workspace_data_filters=[
            DeclarativeWorkspaceDataFilter(
                column_name="country_id",
                description="ID of country",
                id="country_id",
                title="Country ID",
                workspace=WorkspaceIdentifier(
                    id="alpha.sales",
                    type="workspace",
                ),
                workspace_data_filter_settings=[
                    DeclarativeWorkspaceDataFilterSetting(
                        description="ID of country setting",
                        filter_values=["US"],
                        id="country_id_setting",
                        title="Country ID setting",
                        workspace=WorkspaceIdentifier(
                            id="alpha.sales",
                            type="workspace",
                        ),
                    ),
                ],
            ),
        ],
    ) # DeclarativeWorkspaceDataFilters | 

    # example passing only required values which don't have defaults set
    try:
        # Set all workspace data filters
        api_instance.set_workspace_data_filters_layout(declarative_workspace_data_filters)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->set_workspace_data_filters_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_workspace_data_filters** | [**DeclarativeWorkspaceDataFilters**](DeclarativeWorkspaceDataFilters.md)|  |

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
**204** | All workspace data filters set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_user_data_filters**
> JsonApiUserDataFilterOutDocument update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document)

Put a User Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument
from gooddata_api_client.model.json_api_user_data_filter_in_document import JsonApiUserDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_user_data_filter_in_document = JsonApiUserDataFilterInDocument(
        data=JsonApiUserDataFilterIn(
            attributes=JsonApiUserDataFilterInAttributes(
                are_relations_valid=True,
                description="description_example",
                maql="maql_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiUserDataFilterInRelationships(
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
                user_group=JsonApiOrganizationOutRelationshipsBootstrapUserGroup(
                    data=JsonApiUserGroupToOneLinkage(None),
                ),
            ),
            type="userDataFilter",
        ),
    ) # JsonApiUserDataFilterInDocument | 
    filter = "filter=title==someString;description==someString;user.id==321;userGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=user,userGroup,facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a User Data Filter
        api_response = api_instance.update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_user_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a User Data Filter
        api_response = api_instance.update_entity_user_data_filters(workspace_id, object_id, json_api_user_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_user_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_user_data_filter_in_document** | [**JsonApiUserDataFilterInDocument**](JsonApiUserDataFilterInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiUserDataFilterOutDocument**](JsonApiUserDataFilterOutDocument.md)

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

# **update_entity_workspace_data_filter_settings**
> JsonApiWorkspaceDataFilterSettingOutDocument update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document)

Put a Settings for Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_setting_in_document import JsonApiWorkspaceDataFilterSettingInDocument
from gooddata_api_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_setting_in_document = JsonApiWorkspaceDataFilterSettingInDocument(
        data=JsonApiWorkspaceDataFilterSettingIn(
            attributes=JsonApiWorkspaceDataFilterSettingInAttributes(
                description="description_example",
                filter_values=[
                    "filter_values_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterSettingInRelationships(
                workspace_data_filter=JsonApiWorkspaceDataFilterSettingInRelationshipsWorkspaceDataFilter(
                    data=JsonApiWorkspaceDataFilterToOneLinkage(None),
                ),
            ),
            type="workspaceDataFilterSetting",
        ),
    ) # JsonApiWorkspaceDataFilterSettingInDocument | 
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Settings for Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Settings for Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filter_settings(workspace_id, object_id, json_api_workspace_data_filter_setting_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_setting_in_document** | [**JsonApiWorkspaceDataFilterSettingInDocument**](JsonApiWorkspaceDataFilterSettingInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterSettingOutDocument**](JsonApiWorkspaceDataFilterSettingOutDocument.md)

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

# **update_entity_workspace_data_filters**
> JsonApiWorkspaceDataFilterOutDocument update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document)

Put a Workspace Data Filter

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_filters_api
from gooddata_api_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from gooddata_api_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_filters_api.DataFiltersApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            attributes=JsonApiWorkspaceDataFilterInAttributes(
                column_name="column_name_example",
                description="description_example",
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiWorkspaceDataFilterInRelationships(
                filter_settings=JsonApiWorkspaceDataFilterInRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
            type="workspaceDataFilter",
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Data Filter
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataFiltersApi->update_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiWorkspaceDataFilterOutDocument**](JsonApiWorkspaceDataFilterOutDocument.md)

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

