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
> JsonApiFilterViewOutDocument create_entity_filter_views(workspace_id, json_api_filter_view_in_document, include=include)

Post Filter views

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.models.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    json_api_filter_view_in_document = gooddata_api_client.JsonApiFilterViewInDocument() # JsonApiFilterViewInDocument | 
    include = ['analyticalDashboard,user'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Post Filter views
        api_response = api_instance.create_entity_filter_views(workspace_id, json_api_filter_view_in_document, include=include)
        print("The response of FilterViewsApi->create_entity_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->create_entity_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **json_api_filter_view_in_document** | [**JsonApiFilterViewInDocument**](JsonApiFilterViewInDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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
> delete_entity_filter_views(workspace_id, object_id, filter=filter)

Delete Filter view

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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;analyticalDashboard.id==321;user.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Filter view
        api_instance.delete_entity_filter_views(workspace_id, object_id, filter=filter)
    except Exception as e:
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
> JsonApiFilterViewOutList get_all_entities_filter_views(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)

Get all Filter views

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_filter_view_out_list import JsonApiFilterViewOutList
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    origin = ALL # str |  (optional) (default to ALL)
    filter = 'title==someString;description==someString;analyticalDashboard.id==321;user.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['analyticalDashboard,user'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Filter views
        api_response = api_instance.get_all_entities_filter_views(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        print("The response of FilterViewsApi->get_all_entities_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->get_all_entities_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **origin** | **str**|  | [optional] [default to ALL]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **x_gdc_validate_relations** | **bool**|  | [optional] [default to False]
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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
> JsonApiFilterViewOutDocument get_entity_filter_views(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)

Get Filter view

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;analyticalDashboard.id==321;user.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['analyticalDashboard,user'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)

    try:
        # Get Filter view
        api_response = api_instance.get_entity_filter_views(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        print("The response of FilterViewsApi->get_entity_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->get_entity_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **x_gdc_validate_relations** | **bool**|  | [optional] [default to False]

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
> List[DeclarativeFilterView] get_filter_views(workspace_id, exclude=exclude)

Get filter views

Retrieve filter views for the specific workspace

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.declarative_filter_view import DeclarativeFilterView
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    exclude = ['exclude_example'] # List[str] |  (optional)

    try:
        # Get filter views
        api_response = api_instance.get_filter_views(workspace_id, exclude=exclude)
        print("The response of FilterViewsApi->get_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->get_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **exclude** | [**List[str]**](str.md)|  | [optional] 

### Return type

[**List[DeclarativeFilterView]**](DeclarativeFilterView.md)

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
> JsonApiFilterViewOutDocument patch_entity_filter_views(workspace_id, object_id, json_api_filter_view_patch_document, filter=filter, include=include)

Patch Filter view

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
from gooddata_api_client.models.json_api_filter_view_patch_document import JsonApiFilterViewPatchDocument
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_filter_view_patch_document = gooddata_api_client.JsonApiFilterViewPatchDocument() # JsonApiFilterViewPatchDocument | 
    filter = 'title==someString;description==someString;analyticalDashboard.id==321;user.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['analyticalDashboard,user'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch Filter view
        api_response = api_instance.patch_entity_filter_views(workspace_id, object_id, json_api_filter_view_patch_document, filter=filter, include=include)
        print("The response of FilterViewsApi->patch_entity_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->patch_entity_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_filter_view_patch_document** | [**JsonApiFilterViewPatchDocument**](JsonApiFilterViewPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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
import gooddata_api_client
from gooddata_api_client.models.declarative_filter_view import DeclarativeFilterView
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    declarative_filter_view = [gooddata_api_client.DeclarativeFilterView()] # List[DeclarativeFilterView] | 

    try:
        # Set filter views
        api_instance.set_filter_views(workspace_id, declarative_filter_view)
    except Exception as e:
        print("Exception when calling FilterViewsApi->set_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **declarative_filter_view** | [**List[DeclarativeFilterView]**](DeclarativeFilterView.md)|  | 

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
> JsonApiFilterViewOutDocument update_entity_filter_views(workspace_id, object_id, json_api_filter_view_in_document, filter=filter, include=include)

Put Filter views

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_filter_view_in_document import JsonApiFilterViewInDocument
from gooddata_api_client.models.json_api_filter_view_out_document import JsonApiFilterViewOutDocument
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
    api_instance = gooddata_api_client.FilterViewsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_filter_view_in_document = gooddata_api_client.JsonApiFilterViewInDocument() # JsonApiFilterViewInDocument | 
    filter = 'title==someString;description==someString;analyticalDashboard.id==321;user.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['analyticalDashboard,user'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put Filter views
        api_response = api_instance.update_entity_filter_views(workspace_id, object_id, json_api_filter_view_in_document, filter=filter, include=include)
        print("The response of FilterViewsApi->update_entity_filter_views:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling FilterViewsApi->update_entity_filter_views: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_filter_view_in_document** | [**JsonApiFilterViewInDocument**](JsonApiFilterViewInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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

