# gooddata_api_client.ReportTemplateControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_report_templates**](ReportTemplateControllerApi.md#create_entity_report_templates) | **POST** /api/v1/entities/workspaces/{workspaceId}/reportTemplates | Post Report Template
[**delete_entity_report_templates**](ReportTemplateControllerApi.md#delete_entity_report_templates) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/reportTemplates/{objectId} | Delete a Report Template
[**get_all_entities_report_templates**](ReportTemplateControllerApi.md#get_all_entities_report_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/reportTemplates | Get all Report Templates
[**get_entity_report_templates**](ReportTemplateControllerApi.md#get_entity_report_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/reportTemplates/{objectId} | Get a Report Template
[**patch_entity_report_templates**](ReportTemplateControllerApi.md#patch_entity_report_templates) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/reportTemplates/{objectId} | Patch a Report Template
[**update_entity_report_templates**](ReportTemplateControllerApi.md#update_entity_report_templates) | **PUT** /api/v1/entities/workspaces/{workspaceId}/reportTemplates/{objectId} | Put a Report Template


# **create_entity_report_templates**
> JsonApiReportTemplateOutDocument create_entity_report_templates(workspace_id, json_api_report_template_post_optional_id_document)

Post Report Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from gooddata_api_client.model.json_api_report_template_post_optional_id_document import JsonApiReportTemplatePostOptionalIdDocument
from gooddata_api_client.model.json_api_report_template_out_document import JsonApiReportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_report_template_post_optional_id_document = JsonApiReportTemplatePostOptionalIdDocument(
        data=JsonApiReportTemplatePostOptionalId(
            attributes=JsonApiReportTemplateInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="reportTemplate",
        ),
    ) # JsonApiReportTemplatePostOptionalIdDocument | 
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Report Template
        api_response = api_instance.create_entity_report_templates(workspace_id, json_api_report_template_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->create_entity_report_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Report Template
        api_response = api_instance.create_entity_report_templates(workspace_id, json_api_report_template_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->create_entity_report_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_report_template_post_optional_id_document** | [**JsonApiReportTemplatePostOptionalIdDocument**](JsonApiReportTemplatePostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiReportTemplateOutDocument**](JsonApiReportTemplateOutDocument.md)

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

# **delete_entity_report_templates**
> delete_entity_report_templates(workspace_id, object_id)

Delete a Report Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Report Template
        api_instance.delete_entity_report_templates(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->delete_entity_report_templates: %s\n" % e)
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

# **get_all_entities_report_templates**
> JsonApiReportTemplateOutList get_all_entities_report_templates(workspace_id)

Get all Report Templates

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from gooddata_api_client.model.json_api_report_template_out_list import JsonApiReportTemplateOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
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
        # Get all Report Templates
        api_response = api_instance.get_all_entities_report_templates(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->get_all_entities_report_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Report Templates
        api_response = api_instance.get_all_entities_report_templates(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->get_all_entities_report_templates: %s\n" % e)
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

[**JsonApiReportTemplateOutList**](JsonApiReportTemplateOutList.md)

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

# **get_entity_report_templates**
> JsonApiReportTemplateOutDocument get_entity_report_templates(workspace_id, object_id)

Get a Report Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from gooddata_api_client.model.json_api_report_template_out_document import JsonApiReportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Report Template
        api_response = api_instance.get_entity_report_templates(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->get_entity_report_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Report Template
        api_response = api_instance.get_entity_report_templates(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->get_entity_report_templates: %s\n" % e)
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

[**JsonApiReportTemplateOutDocument**](JsonApiReportTemplateOutDocument.md)

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

# **patch_entity_report_templates**
> JsonApiReportTemplateOutDocument patch_entity_report_templates(workspace_id, object_id, json_api_report_template_patch_document)

Patch a Report Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from gooddata_api_client.model.json_api_report_template_patch_document import JsonApiReportTemplatePatchDocument
from gooddata_api_client.model.json_api_report_template_out_document import JsonApiReportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_report_template_patch_document = JsonApiReportTemplatePatchDocument(
        data=JsonApiReportTemplatePatch(
            attributes=JsonApiReportTemplatePatchAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="reportTemplate",
        ),
    ) # JsonApiReportTemplatePatchDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Report Template
        api_response = api_instance.patch_entity_report_templates(workspace_id, object_id, json_api_report_template_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->patch_entity_report_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Report Template
        api_response = api_instance.patch_entity_report_templates(workspace_id, object_id, json_api_report_template_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->patch_entity_report_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_report_template_patch_document** | [**JsonApiReportTemplatePatchDocument**](JsonApiReportTemplatePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiReportTemplateOutDocument**](JsonApiReportTemplateOutDocument.md)

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

# **update_entity_report_templates**
> JsonApiReportTemplateOutDocument update_entity_report_templates(workspace_id, object_id, json_api_report_template_in_document)

Put a Report Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import report_template_controller_api
from gooddata_api_client.model.json_api_report_template_in_document import JsonApiReportTemplateInDocument
from gooddata_api_client.model.json_api_report_template_out_document import JsonApiReportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = report_template_controller_api.ReportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_report_template_in_document = JsonApiReportTemplateInDocument(
        data=JsonApiReportTemplateIn(
            attributes=JsonApiReportTemplateInAttributes(
                are_relations_valid=True,
                content={},
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
            ),
            id="id1",
            type="reportTemplate",
        ),
    ) # JsonApiReportTemplateInDocument | 
    filter = "title==someString;description==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Report Template
        api_response = api_instance.update_entity_report_templates(workspace_id, object_id, json_api_report_template_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->update_entity_report_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Report Template
        api_response = api_instance.update_entity_report_templates(workspace_id, object_id, json_api_report_template_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ReportTemplateControllerApi->update_entity_report_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_report_template_in_document** | [**JsonApiReportTemplateInDocument**](JsonApiReportTemplateInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiReportTemplateOutDocument**](JsonApiReportTemplateOutDocument.md)

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

