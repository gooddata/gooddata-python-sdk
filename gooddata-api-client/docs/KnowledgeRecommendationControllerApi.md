# gooddata_api_client.KnowledgeRecommendationControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#create_entity_knowledge_recommendations) | **POST** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | Post Knowledge Recommendations
[**delete_entity_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#delete_entity_knowledge_recommendations) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | Delete a Knowledge Recommendation
[**get_all_entities_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#get_all_entities_knowledge_recommendations) | **GET** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations | Get all Knowledge Recommendations
[**get_entity_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#get_entity_knowledge_recommendations) | **GET** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | Get a Knowledge Recommendation
[**patch_entity_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#patch_entity_knowledge_recommendations) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | Patch a Knowledge Recommendation
[**search_entities_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#search_entities_knowledge_recommendations) | **POST** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/search | The search endpoint (beta)
[**update_entity_knowledge_recommendations**](KnowledgeRecommendationControllerApi.md#update_entity_knowledge_recommendations) | **PUT** /api/v1/entities/workspaces/{workspaceId}/knowledgeRecommendations/{objectId} | Put a Knowledge Recommendation


# **create_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document)

Post Knowledge Recommendations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_post_optional_id_document import JsonApiKnowledgeRecommendationPostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_knowledge_recommendation_post_optional_id_document = JsonApiKnowledgeRecommendationPostOptionalIdDocument(
        data=JsonApiKnowledgeRecommendationPostOptionalId(
            attributes=JsonApiKnowledgeRecommendationInAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationPostOptionalIdDocument | 
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Knowledge Recommendations
        api_response = api_instance.create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->create_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Knowledge Recommendations
        api_response = api_instance.create_entity_knowledge_recommendations(workspace_id, json_api_knowledge_recommendation_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->create_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_knowledge_recommendation_post_optional_id_document** | [**JsonApiKnowledgeRecommendationPostOptionalIdDocument**](JsonApiKnowledgeRecommendationPostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_knowledge_recommendations**
> delete_entity_knowledge_recommendations(workspace_id, object_id)

Delete a Knowledge Recommendation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Knowledge Recommendation
        api_instance.delete_entity_knowledge_recommendations(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->delete_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |

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

# **get_all_entities_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutList get_all_entities_knowledge_recommendations(workspace_id)

Get all Knowledge Recommendations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
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
        # Get all Knowledge Recommendations
        api_response = api_instance.get_all_entities_knowledge_recommendations(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->get_all_entities_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Knowledge Recommendations
        api_response = api_instance.get_all_entities_knowledge_recommendations(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->get_all_entities_knowledge_recommendations: %s\n" % e)
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

[**JsonApiKnowledgeRecommendationOutList**](JsonApiKnowledgeRecommendationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument get_entity_knowledge_recommendations(workspace_id, object_id)

Get a Knowledge Recommendation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Knowledge Recommendation
        api_response = api_instance.get_entity_knowledge_recommendations(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->get_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Knowledge Recommendation
        api_response = api_instance.get_entity_knowledge_recommendations(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->get_entity_knowledge_recommendations: %s\n" % e)
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

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document)

Patch a Knowledge Recommendation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_patch_document import JsonApiKnowledgeRecommendationPatchDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_knowledge_recommendation_patch_document = JsonApiKnowledgeRecommendationPatchDocument(
        data=JsonApiKnowledgeRecommendationPatch(
            attributes=JsonApiKnowledgeRecommendationPatchAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationOutRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationPatchDocument | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Knowledge Recommendation
        api_response = api_instance.patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->patch_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Knowledge Recommendation
        api_response = api_instance.patch_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->patch_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_knowledge_recommendation_patch_document** | [**JsonApiKnowledgeRecommendationPatchDocument**](JsonApiKnowledgeRecommendationPatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **search_entities_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutList search_entities_knowledge_recommendations(workspace_id, entity_search_body)

The search endpoint (beta)

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_list import JsonApiKnowledgeRecommendationOutList
from gooddata_api_client.model.entity_search_body import EntitySearchBody
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    entity_search_body = EntitySearchBody(
        filter="filter_example",
        include=[
            "include_example",
        ],
        meta_include=[
            "meta_include_example",
        ],
        page=EntitySearchPage(
            index=0,
            size=100,
        ),
        sort=[
            EntitySearchSort(
                direction="ASC",
                _property="_property_example",
            ),
        ],
    ) # EntitySearchBody | Search request body with filter, pagination, and sorting options
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # The search endpoint (beta)
        api_response = api_instance.search_entities_knowledge_recommendations(workspace_id, entity_search_body)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->search_entities_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # The search endpoint (beta)
        api_response = api_instance.search_entities_knowledge_recommendations(workspace_id, entity_search_body, origin=origin, x_gdc_validate_relations=x_gdc_validate_relations)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->search_entities_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **entity_search_body** | [**EntitySearchBody**](EntitySearchBody.md)| Search request body with filter, pagination, and sorting options |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False

### Return type

[**JsonApiKnowledgeRecommendationOutList**](JsonApiKnowledgeRecommendationOutList.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_knowledge_recommendations**
> JsonApiKnowledgeRecommendationOutDocument update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document)

Put a Knowledge Recommendation

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import knowledge_recommendation_controller_api
from gooddata_api_client.model.json_api_knowledge_recommendation_out_document import JsonApiKnowledgeRecommendationOutDocument
from gooddata_api_client.model.json_api_knowledge_recommendation_in_document import JsonApiKnowledgeRecommendationInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = knowledge_recommendation_controller_api.KnowledgeRecommendationControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_knowledge_recommendation_in_document = JsonApiKnowledgeRecommendationInDocument(
        data=JsonApiKnowledgeRecommendationIn(
            attributes=JsonApiKnowledgeRecommendationInAttributes(
                analytical_dashboard_title="Portfolio Health Insights",
                analyzed_period="2023-07",
                analyzed_value=None,
                are_relations_valid=True,
                comparison_type="MONTH",
                confidence=None,
                description="description_example",
                direction="DECREASED",
                metric_title="Revenue",
                recommendations={},
                reference_period="2023-06",
                reference_value=None,
                source_count=2,
                tags=[
                    "tags_example",
                ],
                title="title_example",
                widget_id="widget-123",
                widget_name="Revenue Trend",
            ),
            id="id1",
            relationships=JsonApiKnowledgeRecommendationInRelationships(
                analytical_dashboard=JsonApiAutomationInRelationshipsAnalyticalDashboard(
                    data=JsonApiAnalyticalDashboardToOneLinkage(None),
                ),
                metric=JsonApiKnowledgeRecommendationInRelationshipsMetric(
                    data=JsonApiMetricToOneLinkage(None),
                ),
            ),
            type="knowledgeRecommendation",
        ),
    ) # JsonApiKnowledgeRecommendationInDocument | 
    filter = "title==someString;description==someString;metric.id==321;analyticalDashboard.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "metric,analyticalDashboard",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Knowledge Recommendation
        api_response = api_instance.update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->update_entity_knowledge_recommendations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Knowledge Recommendation
        api_response = api_instance.update_entity_knowledge_recommendations(workspace_id, object_id, json_api_knowledge_recommendation_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling KnowledgeRecommendationControllerApi->update_entity_knowledge_recommendations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_knowledge_recommendation_in_document** | [**JsonApiKnowledgeRecommendationInDocument**](JsonApiKnowledgeRecommendationInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiKnowledgeRecommendationOutDocument**](JsonApiKnowledgeRecommendationOutDocument.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

