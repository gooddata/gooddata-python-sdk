# gooddata_metadata_client.WorkspaceObjectControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#create_entity_analytical_dashboards) | **POST** /api/entities/workspaces/{workspaceId}/analyticalDashboards | 
[**create_entity_filter_contexts**](WorkspaceObjectControllerApi.md#create_entity_filter_contexts) | **POST** /api/entities/workspaces/{workspaceId}/filterContexts | 
[**create_entity_metrics**](WorkspaceObjectControllerApi.md#create_entity_metrics) | **POST** /api/entities/workspaces/{workspaceId}/metrics | 
[**create_entity_visualization_objects**](WorkspaceObjectControllerApi.md#create_entity_visualization_objects) | **POST** /api/entities/workspaces/{workspaceId}/visualizationObjects | 
[**create_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#create_entity_workspace_data_filters) | **POST** /api/entities/workspaces/{workspaceId}/workspaceDataFilters | 
[**delete_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#delete_entity_analytical_dashboards) | **DELETE** /api/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | 
[**delete_entity_filter_contexts**](WorkspaceObjectControllerApi.md#delete_entity_filter_contexts) | **DELETE** /api/entities/workspaces/{workspaceId}/filterContexts/{objectId} | 
[**delete_entity_metrics**](WorkspaceObjectControllerApi.md#delete_entity_metrics) | **DELETE** /api/entities/workspaces/{workspaceId}/metrics/{objectId} | 
[**delete_entity_visualization_objects**](WorkspaceObjectControllerApi.md#delete_entity_visualization_objects) | **DELETE** /api/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | 
[**delete_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#delete_entity_workspace_data_filters) | **DELETE** /api/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | 
[**get_all_entities_analytical_dashboards**](WorkspaceObjectControllerApi.md#get_all_entities_analytical_dashboards) | **GET** /api/entities/workspaces/{workspaceId}/analyticalDashboards | 
[**get_all_entities_attributes**](WorkspaceObjectControllerApi.md#get_all_entities_attributes) | **GET** /api/entities/workspaces/{workspaceId}/attributes | 
[**get_all_entities_datasets**](WorkspaceObjectControllerApi.md#get_all_entities_datasets) | **GET** /api/entities/workspaces/{workspaceId}/datasets | 
[**get_all_entities_facts**](WorkspaceObjectControllerApi.md#get_all_entities_facts) | **GET** /api/entities/workspaces/{workspaceId}/facts | 
[**get_all_entities_filter_contexts**](WorkspaceObjectControllerApi.md#get_all_entities_filter_contexts) | **GET** /api/entities/workspaces/{workspaceId}/filterContexts | 
[**get_all_entities_labels**](WorkspaceObjectControllerApi.md#get_all_entities_labels) | **GET** /api/entities/workspaces/{workspaceId}/labels | 
[**get_all_entities_metrics**](WorkspaceObjectControllerApi.md#get_all_entities_metrics) | **GET** /api/entities/workspaces/{workspaceId}/metrics | 
[**get_all_entities_visualization_objects**](WorkspaceObjectControllerApi.md#get_all_entities_visualization_objects) | **GET** /api/entities/workspaces/{workspaceId}/visualizationObjects | 
[**get_all_entities_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#get_all_entities_workspace_data_filter_settings) | **GET** /api/entities/workspaces/{workspaceId}/workspaceDataFilterSettings | 
[**get_all_entities_workspace_data_filters**](WorkspaceObjectControllerApi.md#get_all_entities_workspace_data_filters) | **GET** /api/entities/workspaces/{workspaceId}/workspaceDataFilters | 
[**get_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#get_entity_analytical_dashboards) | **GET** /api/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | 
[**get_entity_attributes**](WorkspaceObjectControllerApi.md#get_entity_attributes) | **GET** /api/entities/workspaces/{workspaceId}/attributes/{objectId} | 
[**get_entity_datasets**](WorkspaceObjectControllerApi.md#get_entity_datasets) | **GET** /api/entities/workspaces/{workspaceId}/datasets/{objectId} | 
[**get_entity_facts**](WorkspaceObjectControllerApi.md#get_entity_facts) | **GET** /api/entities/workspaces/{workspaceId}/facts/{objectId} | 
[**get_entity_filter_contexts**](WorkspaceObjectControllerApi.md#get_entity_filter_contexts) | **GET** /api/entities/workspaces/{workspaceId}/filterContexts/{objectId} | 
[**get_entity_labels**](WorkspaceObjectControllerApi.md#get_entity_labels) | **GET** /api/entities/workspaces/{workspaceId}/labels/{objectId} | 
[**get_entity_metrics**](WorkspaceObjectControllerApi.md#get_entity_metrics) | **GET** /api/entities/workspaces/{workspaceId}/metrics/{objectId} | 
[**get_entity_visualization_objects**](WorkspaceObjectControllerApi.md#get_entity_visualization_objects) | **GET** /api/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | 
[**get_entity_workspace_data_filter_settings**](WorkspaceObjectControllerApi.md#get_entity_workspace_data_filter_settings) | **GET** /api/entities/workspaces/{workspaceId}/workspaceDataFilterSettings/{objectId} | 
[**get_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#get_entity_workspace_data_filters) | **GET** /api/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | 
[**update_entity_analytical_dashboards**](WorkspaceObjectControllerApi.md#update_entity_analytical_dashboards) | **PUT** /api/entities/workspaces/{workspaceId}/analyticalDashboards/{objectId} | 
[**update_entity_filter_contexts**](WorkspaceObjectControllerApi.md#update_entity_filter_contexts) | **PUT** /api/entities/workspaces/{workspaceId}/filterContexts/{objectId} | 
[**update_entity_metrics**](WorkspaceObjectControllerApi.md#update_entity_metrics) | **PUT** /api/entities/workspaces/{workspaceId}/metrics/{objectId} | 
[**update_entity_visualization_objects**](WorkspaceObjectControllerApi.md#update_entity_visualization_objects) | **PUT** /api/entities/workspaces/{workspaceId}/visualizationObjects/{objectId} | 
[**update_entity_workspace_data_filters**](WorkspaceObjectControllerApi.md#update_entity_workspace_data_filters) | **PUT** /api/entities/workspaces/{workspaceId}/workspaceDataFilters/{objectId} | 


# **create_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_analytical_dashboard_in_document import JsonApiAnalyticalDashboardInDocument
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_analytical_dashboard_in_document = JsonApiAnalyticalDashboardInDocument(
        data=JsonApiAnalyticalDashboardIn(
            id="id1",
            type="analyticalDashboard",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiAnalyticalDashboardInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_analytical_dashboards(workspace_id, json_api_analytical_dashboard_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_analytical_dashboard_in_document** | [**JsonApiAnalyticalDashboardInDocument**](JsonApiAnalyticalDashboardInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

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

# **create_entity_filter_contexts**
> JsonApiFilterContextOutDocument create_entity_filter_contexts(workspace_id, json_api_filter_context_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from gooddata_metadata_client.model.json_api_filter_context_in_document import JsonApiFilterContextInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_filter_context_in_document = JsonApiFilterContextInDocument(
        data=JsonApiFilterContextIn(
            id="id1",
            type="filterContext",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiFilterContextInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_filter_contexts(workspace_id, json_api_filter_context_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_filter_contexts(workspace_id, json_api_filter_context_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_filter_context_in_document** | [**JsonApiFilterContextInDocument**](JsonApiFilterContextInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

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

# **create_entity_metrics**
> JsonApiMetricOutDocument create_entity_metrics(workspace_id, json_api_metric_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_metric_in_document import JsonApiMetricInDocument
from gooddata_metadata_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_metric_in_document = JsonApiMetricInDocument(
        data=JsonApiMetricIn(
            id="id1",
            type="metric",
            attributes=JsonApiMetricOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content=JsonApiMetricOutAttributesContent(
                    format="format_example",
                    maql="maql_example",
                ),
            ),
        ),
    ) # JsonApiMetricInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_metric_in_document** | [**JsonApiMetricInDocument**](JsonApiMetricInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

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

# **create_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument create_entity_visualization_objects(workspace_id, json_api_visualization_object_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_visualization_object_in_document import JsonApiVisualizationObjectInDocument
from gooddata_metadata_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_visualization_object_in_document = JsonApiVisualizationObjectInDocument(
        data=JsonApiVisualizationObjectIn(
            id="id1",
            type="visualizationObject",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiVisualizationObjectInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_visualization_objects(workspace_id, json_api_visualization_object_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_visualization_object_in_document** | [**JsonApiVisualizationObjectInDocument**](JsonApiVisualizationObjectInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            id="id1",
            type="workspaceDataFilter",
            attributes=JsonApiWorkspaceDataFilterOutAttributes(
                title="title_example",
                description="description_example",
                column_name="column_name_example",
                data_source_id="data_source_id_example",
            ),
            relationships=JsonApiWorkspaceDataFilterOutRelationships(
                filter_settings=JsonApiWorkspaceDataFilterOutRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.create_entity_workspace_data_filters(workspace_id, json_api_workspace_data_filter_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->create_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_analytical_dashboards**
> delete_entity_analytical_dashboards(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_analytical_dashboards(workspace_id, object_id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_filter_contexts**
> delete_entity_filter_contexts(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_filter_contexts(workspace_id, object_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_filter_contexts(workspace_id, object_id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_metrics**
> delete_entity_metrics(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_metrics(workspace_id, object_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_metrics(workspace_id, object_id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **delete_entity_visualization_objects**
> delete_entity_visualization_objects(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_visualization_objects(workspace_id, object_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_visualization_objects(workspace_id, object_id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_instance.delete_entity_workspace_data_filters(workspace_id, object_id, predicate=predicate, filter=filter)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->delete_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

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

# **get_all_entities_analytical_dashboards**
> JsonApiAnalyticalDashboardOutList get_all_entities_analytical_dashboards(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_list import JsonApiAnalyticalDashboardOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_analytical_dashboards(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_analytical_dashboards(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiAnalyticalDashboardOutList**](JsonApiAnalyticalDashboardOutList.md)

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

# **get_all_entities_attributes**
> JsonApiAttributeOutList get_all_entities_attributes(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_attribute_out_list import JsonApiAttributeOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=dataset,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_attributes(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_attributes(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiAttributeOutList**](JsonApiAttributeOutList.md)

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

# **get_all_entities_datasets**
> JsonApiDatasetOutList get_all_entities_datasets(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_dataset_out_list import JsonApiDatasetOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,facts,references",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_datasets(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_datasets(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_datasets: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiDatasetOutList**](JsonApiDatasetOutList.md)

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

# **get_all_entities_facts**
> JsonApiFactOutList get_all_entities_facts(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_fact_out_list import JsonApiFactOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=dataset",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_facts(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_facts(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_facts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiFactOutList**](JsonApiFactOutList.md)

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

# **get_all_entities_filter_contexts**
> JsonApiFilterContextOutList get_all_entities_filter_contexts(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_filter_context_out_list import JsonApiFilterContextOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_filter_contexts(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_filter_contexts(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiFilterContextOutList**](JsonApiFilterContextOutList.md)

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

# **get_all_entities_labels**
> JsonApiLabelOutList get_all_entities_labels(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_label_out_list import JsonApiLabelOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;attribute.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attribute",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_labels(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_labels(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_labels: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiLabelOutList**](JsonApiLabelOutList.md)

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

# **get_all_entities_metrics**
> JsonApiMetricOutList get_all_entities_metrics(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_metric_out_list import JsonApiMetricOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_metrics(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_metrics(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiMetricOutList**](JsonApiMetricOutList.md)

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

# **get_all_entities_visualization_objects**
> JsonApiVisualizationObjectOutList get_all_entities_visualization_objects(workspace_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_visualization_object_out_list import JsonApiVisualizationObjectOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_visualization_objects(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiVisualizationObjectOutList**](JsonApiVisualizationObjectOutList.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_list import JsonApiWorkspaceDataFilterSettingOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_workspace_data_filter_settings(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_list import JsonApiWorkspaceDataFilterOutList
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_all_entities_workspace_data_filters(workspace_id, predicate=predicate, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_all_entities_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property(,asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

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

# **get_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument get_entity_analytical_dashboards(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_analytical_dashboards(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_analytical_dashboards(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

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

# **get_entity_attributes**
> JsonApiAttributeOutDocument get_entity_attributes(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_attribute_out_document import JsonApiAttributeOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=dataset,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_attributes(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_attributes: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_attributes(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_attributes: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiAttributeOutDocument**](JsonApiAttributeOutDocument.md)

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

# **get_entity_datasets**
> JsonApiDatasetOutDocument get_entity_datasets(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_dataset_out_document import JsonApiDatasetOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,facts,references",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_datasets(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_datasets: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_datasets(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_datasets: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiDatasetOutDocument**](JsonApiDatasetOutDocument.md)

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

# **get_entity_facts**
> JsonApiFactOutDocument get_entity_facts(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_fact_out_document import JsonApiFactOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;dataset.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=dataset",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_facts(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_facts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_facts(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_facts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiFactOutDocument**](JsonApiFactOutDocument.md)

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

# **get_entity_filter_contexts**
> JsonApiFilterContextOutDocument get_entity_filter_contexts(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_filter_contexts(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_filter_contexts(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

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

# **get_entity_labels**
> JsonApiLabelOutDocument get_entity_labels(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_label_out_document import JsonApiLabelOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;attribute.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attribute",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_labels(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_labels: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_labels(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_labels: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiLabelOutDocument**](JsonApiLabelOutDocument.md)

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

# **get_entity_metrics**
> JsonApiMetricOutDocument get_entity_metrics(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_metrics(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_metrics(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

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

# **get_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument get_entity_visualization_objects(workspace_id, object_id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_visualization_objects(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_setting_out_document import JsonApiWorkspaceDataFilterSettingOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString;workspaceDataFilter.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=workspaceDataFilter",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filter_settings: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_workspace_data_filter_settings(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filter_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_workspace_data_filters(workspace_id, object_id, predicate=predicate, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->get_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

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

# **update_entity_analytical_dashboards**
> JsonApiAnalyticalDashboardOutDocument update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_analytical_dashboard_in_document import JsonApiAnalyticalDashboardInDocument
from gooddata_metadata_client.model.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_analytical_dashboard_in_document = JsonApiAnalyticalDashboardInDocument(
        data=JsonApiAnalyticalDashboardIn(
            id="id1",
            type="analyticalDashboard",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiAnalyticalDashboardInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=visualizationObjects,analyticalDashboards,labels,metrics,datasets,filterContexts",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_analytical_dashboards: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_analytical_dashboards(workspace_id, object_id, json_api_analytical_dashboard_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_analytical_dashboards: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_analytical_dashboard_in_document** | [**JsonApiAnalyticalDashboardInDocument**](JsonApiAnalyticalDashboardInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiAnalyticalDashboardOutDocument**](JsonApiAnalyticalDashboardOutDocument.md)

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

# **update_entity_filter_contexts**
> JsonApiFilterContextOutDocument update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_filter_context_out_document import JsonApiFilterContextOutDocument
from gooddata_metadata_client.model.json_api_filter_context_in_document import JsonApiFilterContextInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_filter_context_in_document = JsonApiFilterContextInDocument(
        data=JsonApiFilterContextIn(
            id="id1",
            type="filterContext",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiFilterContextInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=attributes,datasets,labels",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_filter_contexts: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_filter_contexts(workspace_id, object_id, json_api_filter_context_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_filter_contexts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_filter_context_in_document** | [**JsonApiFilterContextInDocument**](JsonApiFilterContextInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiFilterContextOutDocument**](JsonApiFilterContextOutDocument.md)

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

# **update_entity_metrics**
> JsonApiMetricOutDocument update_entity_metrics(workspace_id, object_id, json_api_metric_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_metric_in_document import JsonApiMetricInDocument
from gooddata_metadata_client.model.json_api_metric_out_document import JsonApiMetricOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_metric_in_document = JsonApiMetricInDocument(
        data=JsonApiMetricIn(
            id="id1",
            type="metric",
            attributes=JsonApiMetricOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content=JsonApiMetricOutAttributesContent(
                    format="format_example",
                    maql="maql_example",
                ),
            ),
        ),
    ) # JsonApiMetricInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_metrics: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_metrics: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_metric_in_document** | [**JsonApiMetricInDocument**](JsonApiMetricInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiMetricOutDocument**](JsonApiMetricOutDocument.md)

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

# **update_entity_visualization_objects**
> JsonApiVisualizationObjectOutDocument update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_visualization_object_in_document import JsonApiVisualizationObjectInDocument
from gooddata_metadata_client.model.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_visualization_object_in_document = JsonApiVisualizationObjectInDocument(
        data=JsonApiVisualizationObjectIn(
            id="id1",
            type="visualizationObject",
            attributes=JsonApiAnalyticalDashboardOutAttributes(
                title="title_example",
                description="description_example",
                tags=[
                    "tags_example",
                ],
                are_relations_valid=True,
                content={},
            ),
        ),
    ) # JsonApiVisualizationObjectInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=facts,attributes,labels,metrics,datasets",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_visualization_objects: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_visualization_objects(workspace_id, object_id, json_api_visualization_object_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_visualization_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_visualization_object_in_document** | [**JsonApiVisualizationObjectInDocument**](JsonApiVisualizationObjectInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiVisualizationObjectOutDocument**](JsonApiVisualizationObjectOutDocument.md)

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



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import workspace_object_controller_api
from gooddata_metadata_client.model.json_api_workspace_data_filter_in_document import JsonApiWorkspaceDataFilterInDocument
from gooddata_metadata_client.model.json_api_workspace_data_filter_out_document import JsonApiWorkspaceDataFilterOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_object_controller_api.WorkspaceObjectControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_data_filter_in_document = JsonApiWorkspaceDataFilterInDocument(
        data=JsonApiWorkspaceDataFilterIn(
            id="id1",
            type="workspaceDataFilter",
            attributes=JsonApiWorkspaceDataFilterOutAttributes(
                title="title_example",
                description="description_example",
                column_name="column_name_example",
                data_source_id="data_source_id_example",
            ),
            relationships=JsonApiWorkspaceDataFilterOutRelationships(
                filter_settings=JsonApiWorkspaceDataFilterOutRelationshipsFilterSettings(
                    data=JsonApiWorkspaceDataFilterSettingToManyLinkage([
                        JsonApiWorkspaceDataFilterSettingLinkage(
                            id="id_example",
                            type="workspaceDataFilterSetting",
                        ),
                    ]),
                ),
            ),
        ),
    ) # JsonApiWorkspaceDataFilterInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=title==someString;description==someString" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=filterSettings",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filters: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_workspace_data_filters(workspace_id, object_id, json_api_workspace_data_filter_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling WorkspaceObjectControllerApi->update_entity_workspace_data_filters: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_data_filter_in_document** | [**JsonApiWorkspaceDataFilterInDocument**](JsonApiWorkspaceDataFilterInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
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

