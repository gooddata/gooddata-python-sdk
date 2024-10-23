# gooddata_api_client.FilterViewsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_filter_views**](FilterViewsApi.md#create_entity_filter_views) | **POST** /api/v1/entities/workspaces/{workspaceId}/filterViews | Post Filter views
[**delete_entity_filter_views**](FilterViewsApi.md#delete_entity_filter_views) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Delete Filter view
[**get_all_entities_filter_views**](FilterViewsApi.md#get_all_entities_filter_views) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterViews | Get all Filter views
[**get_entity_filter_views**](FilterViewsApi.md#get_entity_filter_views) | **GET** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Get Filter view
[**get_filter_views**](FilterViewsApi.md#get_filter_views) | **GET** /api/v1/layout/workspaces/{workspaceId}/filterViews | Get filter views
[**patch_entity_filter_views**](FilterViewsApi.md#patch_entity_filter_views) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Patch Filter view
[**set_filter_views**](FilterViewsApi.md#set_filter_views) | **PUT** /api/v1/layout/workspaces/{workspaceId}/filterViews | Set filter views
[**update_entity_filter_views**](FilterViewsApi.md#update_entity_filter_views) | **PUT** /api/v1/entities/workspaces/{workspaceId}/filterViews/{objectId} | Put Filter views


# **create_entity_filter_views**
> JsonApiFilterViewOutDocument create_entity_filter_views(workspace_id, json_api_filter_view_in_document)

Post Filter views

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_filter_view_in_document = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=JsonApiFilterViewInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiFilterViewInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    ) # JsonApiFilterViewInDocument | 
    include = [
        "include=analyticalDashboard,user",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Filter views
        api_response = api_instance.create_entity_filter_views(workspace_id, json_api_filter_view_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->create_entity_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Filter views
        api_response = api_instance.create_entity_filter_views(workspace_id, json_api_filter_view_in_document, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->create_entity_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_filter_view_in_document** | [**JsonApiFilterViewInDocument**](JsonApiFilterViewInDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterViewOutDocument**](JsonApiFilterViewOutDocument.md)

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

# **delete_entity_filter_views**
> delete_entity_filter_views(workspace_id, object_id)

Delete Filter view

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;analyticalDashboard.id==321;user.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Filter view
        api_instance.delete_entity_filter_views(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->delete_entity_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Filter view
        api_instance.delete_entity_filter_views(workspace_id, object_id, filter=filter)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->delete_entity_filter_views: %s\n" % e)
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

# **get_all_entities_filter_views**
> JsonApiFilterViewOutList get_all_entities_filter_views(workspace_id)

Get all Filter views

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.json_api_filter_view_out_list import JsonApiFilterViewOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "filter=title==someString;description==someString;analyticalDashboard.id==321;user.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=analyticalDashboard,user",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get all Filter views
        api_response = api_instance.get_all_entities_filter_views(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_all_entities_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Filter views
        api_response = api_instance.get_all_entities_filter_views(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_all_entities_filter_views: %s\n" % e)
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

[**JsonApiFilterViewOutList**](JsonApiFilterViewOutList.md)

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

# **get_entity_filter_views**
> JsonApiFilterViewOutDocument get_entity_filter_views(workspace_id, object_id)

Get Filter view

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "filter=title==someString;description==someString;analyticalDashboard.id==321;user.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=analyticalDashboard,user",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Get Filter view
        api_response = api_instance.get_entity_filter_views(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_entity_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get Filter view
        api_response = api_instance.get_entity_filter_views(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_entity_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiFilterViewOutDocument**](JsonApiFilterViewOutDocument.md)

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

# **get_filter_views**
> [DeclarativeFilterView] get_filter_views(workspace_id)

Get filter views

Retrieve filter views for the specific workspace

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    exclude = [
        "ACTIVITY_INFO",
    ] # [str] |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id, exclude=exclude)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->get_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **exclude** | **[str]**|  | [optional]

### Return type

[**[DeclarativeFilterView]**](DeclarativeFilterView.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved filterViews. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_filter_views**
> JsonApiFilterViewOutDocument patch_entity_filter_views(workspace_id, object_id, json_api_filter_view_patch_document)

Patch Filter view

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.json_api_filter_view_patch_document import JsonApiFilterViewPatchDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_filter_view_patch_document = JsonApiFilterViewPatchDocument(
        data=JsonApiFilterViewPatch(
            attributes=JsonApiFilterViewPatchAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiFilterViewInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    ) # JsonApiFilterViewPatchDocument | 
    filter = "filter=title==someString;description==someString;analyticalDashboard.id==321;user.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=analyticalDashboard,user",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Filter view
        api_response = api_instance.patch_entity_filter_views(workspace_id, object_id, json_api_filter_view_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->patch_entity_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Filter view
        api_response = api_instance.patch_entity_filter_views(workspace_id, object_id, json_api_filter_view_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->patch_entity_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_filter_view_patch_document** | [**JsonApiFilterViewPatchDocument**](JsonApiFilterViewPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterViewOutDocument**](JsonApiFilterViewOutDocument.md)

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

# **set_filter_views**
> set_filter_views(workspace_id, declarative_filter_view)

Set filter views

Set filter views for the specific workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.declarative_filter_view import DeclarativeFilterView
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_filter_view = [
        DeclarativeFilterView(
            analytical_dashboard=DeclarativeAnalyticalDashboardIdentifier(
                id="dashboard123",
                type="analyticalDashboard",
            ),
            content=JsonNode(),
            description="description_example",
            id="filterView-1",
            is_default=True,
            tags=[
                "["Revenue","Sales"]",
            ],
            title="title_example",
            user=DeclarativeUserIdentifier(
                id="employee123",
                type="user",
            ),
        ),
    ] # [DeclarativeFilterView] | 

    # example passing only required values which don't have defaults set
    try:
        # Set filter views
        api_instance.set_filter_views(workspace_id, declarative_filter_view)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->set_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_filter_view** | [**[DeclarativeFilterView]**](DeclarativeFilterView.md)|  |

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
**204** | FilterViews successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_filter_views**
> JsonApiFilterViewOutDocument update_entity_filter_views(workspace_id, object_id, json_api_filter_view_in_document)

Put Filter views

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import filter_views_api
from gooddata_api_client.model.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.model.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = filter_views_api.FilterViewsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_filter_view_in_document = JsonApiFilterViewInDocument(
        data=JsonApiFilterViewIn(
            attributes=JsonApiFilterViewInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                is_default=True,
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            relationships=JsonApiFilterViewInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                user=JsonApiFilterViewInRelationshipsUser(
                    data=JsonApiUserToOneLinkage(None),
                ),
            ),
            type="filterView",
        ),
    ) # JsonApiFilterViewInDocument | 
    filter = "filter=title==someString;description==someString;analyticalDashboard.id==321;user.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "include=analyticalDashboard,user",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put Filter views
        api_response = api_instance.update_entity_filter_views(workspace_id, object_id, json_api_filter_view_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->update_entity_filter_views: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put Filter views
        api_response = api_instance.update_entity_filter_views(workspace_id, object_id, json_api_filter_view_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling FilterViewsApi->update_entity_filter_views: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_filter_view_in_document** | [**JsonApiFilterViewInDocument**](JsonApiFilterViewInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterViewOutDocument**](JsonApiFilterViewOutDocument.md)

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

