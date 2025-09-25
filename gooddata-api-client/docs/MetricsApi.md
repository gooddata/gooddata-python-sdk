# gooddata_api_client.MetricsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_metrics**](MetricsApi.md#create_entity_metrics) | **POST** /api/v1/entities/workspaces/{workspaceId}/metrics | Post Metrics
[**delete_entity_metrics**](MetricsApi.md#delete_entity_metrics) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Delete a Metric
[**get_all_entities_metrics**](MetricsApi.md#get_all_entities_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics | Get all Metrics
[**get_entity_metrics**](MetricsApi.md#get_entity_metrics) | **GET** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Get a Metric
[**patch_entity_metrics**](MetricsApi.md#patch_entity_metrics) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Patch a Metric
[**update_entity_metrics**](MetricsApi.md#update_entity_metrics) | **PUT** /api/v1/entities/workspaces/{workspaceId}/metrics/{objectId} | Put a Metric


# **create_entity_metrics**
> JsonApiMetricOutDocument create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document, include=include, meta_include=meta_include)

Post Metrics

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_metric_out_document import JsonApiMetricOutDocument
from gooddata_api_client.models.json_api_metric_post_optional_id_document import JsonApiMetricPostOptionalIdDocument
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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    json_api_metric_post_optional_id_document = gooddata_api_client.JsonApiMetricPostOptionalIdDocument() # JsonApiMetricPostOptionalIdDocument | 
    include = ['createdBy,modifiedBy,facts,attributes,labels,metrics,datasets'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = ['metaInclude=origin,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Post Metrics
        api_response = api_instance.create_entity_metrics(workspace_id, json_api_metric_post_optional_id_document, include=include, meta_include=meta_include)
        print("The response of MetricsApi->create_entity_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->create_entity_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **json_api_metric_post_optional_id_document** | [**JsonApiMetricPostOptionalIdDocument**](JsonApiMetricPostOptionalIdDocument.md)|  | 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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

# **delete_entity_metrics**
> delete_entity_metrics(workspace_id, object_id, filter=filter)

Delete a Metric

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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;createdBy.id==321;modifiedBy.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete a Metric
        api_instance.delete_entity_metrics(workspace_id, object_id, filter=filter)
    except Exception as e:
        print("Exception when calling MetricsApi->delete_entity_metrics: %s\n" % e)
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

# **get_all_entities_metrics**
> JsonApiMetricOutList get_all_entities_metrics(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)

Get all Metrics

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_metric_out_list import JsonApiMetricOutList
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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    origin = ALL # str |  (optional) (default to ALL)
    filter = 'title==someString;description==someString;createdBy.id==321;modifiedBy.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['createdBy,modifiedBy,facts,attributes,labels,metrics,datasets'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)
    meta_include = ['metaInclude=origin,page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get all Metrics
        api_response = api_instance.get_all_entities_metrics(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        print("The response of MetricsApi->get_all_entities_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->get_all_entities_metrics: %s\n" % e)
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

# **get_entity_metrics**
> JsonApiMetricOutDocument get_entity_metrics(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)

Get a Metric

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_metric_out_document import JsonApiMetricOutDocument
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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    filter = 'title==someString;description==someString;createdBy.id==321;modifiedBy.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['createdBy,modifiedBy,facts,attributes,labels,metrics,datasets'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) (default to False)
    meta_include = ['metaInclude=origin,all'] # List[str] | Include Meta objects. (optional)

    try:
        # Get a Metric
        api_response = api_instance.get_entity_metrics(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        print("The response of MetricsApi->get_entity_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->get_entity_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 
 **x_gdc_validate_relations** | **bool**|  | [optional] [default to False]
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

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

# **patch_entity_metrics**
> JsonApiMetricOutDocument patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document, filter=filter, include=include)

Patch a Metric

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_metric_out_document import JsonApiMetricOutDocument
from gooddata_api_client.models.json_api_metric_patch_document import JsonApiMetricPatchDocument
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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_metric_patch_document = gooddata_api_client.JsonApiMetricPatchDocument() # JsonApiMetricPatchDocument | 
    filter = 'title==someString;description==someString;createdBy.id==321;modifiedBy.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['createdBy,modifiedBy,facts,attributes,labels,metrics,datasets'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Patch a Metric
        api_response = api_instance.patch_entity_metrics(workspace_id, object_id, json_api_metric_patch_document, filter=filter, include=include)
        print("The response of MetricsApi->patch_entity_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->patch_entity_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_metric_patch_document** | [**JsonApiMetricPatchDocument**](JsonApiMetricPatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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

# **update_entity_metrics**
> JsonApiMetricOutDocument update_entity_metrics(workspace_id, object_id, json_api_metric_in_document, filter=filter, include=include)

Put a Metric

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_metric_in_document import JsonApiMetricInDocument
from gooddata_api_client.models.json_api_metric_out_document import JsonApiMetricOutDocument
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
    api_instance = gooddata_api_client.MetricsApi(api_client)
    workspace_id = 'workspace_id_example' # str | 
    object_id = 'object_id_example' # str | 
    json_api_metric_in_document = gooddata_api_client.JsonApiMetricInDocument() # JsonApiMetricInDocument | 
    filter = 'title==someString;description==someString;createdBy.id==321;modifiedBy.id==321' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = ['createdBy,modifiedBy,facts,attributes,labels,metrics,datasets'] # List[str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    try:
        # Put a Metric
        api_response = api_instance.update_entity_metrics(workspace_id, object_id, json_api_metric_in_document, filter=filter, include=include)
        print("The response of MetricsApi->update_entity_metrics:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling MetricsApi->update_entity_metrics: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  | 
 **object_id** | **str**|  | 
 **json_api_metric_in_document** | [**JsonApiMetricInDocument**](JsonApiMetricInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **include** | [**List[str]**](str.md)| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional] 

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

