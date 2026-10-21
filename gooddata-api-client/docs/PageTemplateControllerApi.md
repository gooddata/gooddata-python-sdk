# gooddata_api_client.PageTemplateControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_page_templates**](PageTemplateControllerApi.md#create_entity_page_templates) | **POST** /api/v1/entities/workspaces/{workspaceId}/pageTemplates | Post Page Template
[**delete_entity_page_templates**](PageTemplateControllerApi.md#delete_entity_page_templates) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/pageTemplates/{objectId} | Delete a Page Template
[**get_all_entities_page_templates**](PageTemplateControllerApi.md#get_all_entities_page_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/pageTemplates | Get all Page Templates
[**get_entity_page_templates**](PageTemplateControllerApi.md#get_entity_page_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/pageTemplates/{objectId} | Get a Page Template
[**patch_entity_page_templates**](PageTemplateControllerApi.md#patch_entity_page_templates) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/pageTemplates/{objectId} | Patch a Page Template
[**update_entity_page_templates**](PageTemplateControllerApi.md#update_entity_page_templates) | **PUT** /api/v1/entities/workspaces/{workspaceId}/pageTemplates/{objectId} | Put a Page Template


# **create_entity_page_templates**
> JsonApiPublisherDocumentPageTemplateOutDocument create_entity_page_templates(workspace_id, json_api_publisher_document_page_template_post_optional_id_document)

Post Page Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from gooddata_api_client.model.json_api_publisher_document_page_template_out_document import JsonApiPublisherDocumentPageTemplateOutDocument
from gooddata_api_client.model.json_api_publisher_document_page_template_post_optional_id_document import JsonApiPublisherDocumentPageTemplatePostOptionalIdDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_publisher_document_page_template_post_optional_id_document = JsonApiPublisherDocumentPageTemplatePostOptionalIdDocument(
        data=JsonApiPublisherDocumentPageTemplatePostOptionalId(
            attributes=JsonApiPublisherDocumentPageTemplateInAttributes(
                are_relations_valid=True,
                content=JsonApiPublisherDocumentPageTemplateInAttributesContent(
                    filters=[
                        PublisherDocumentFilter(),
                    ],
                    kind="cover",
                    layout=PublisherDocumentLayoutNode(),
                    notes="notes_example",
                    page_size="widescreen",
                    style=PublisherDocumentPageStyle(
                        background_color="background_color_example",
                        background_fit="cover",
                        background_horizontal_align="left",
                        background_image="background_image_example",
                        background_image_opacity=0,
                        background_offset=0,
                        background_offset_bottom=0,
                        background_offset_left=0,
                        background_offset_right=0,
                        background_offset_top=0,
                        background_opacity=0,
                        background_vertical_align="top",
                        font_size=0,
                        font_style="normal",
                        font_weight=1,
                        gap=PublisherDocumentAreaStyleGap(None),
                        horizontal_align="left",
                        letter_spacing=3.14,
                        line_height=3.14,
                        padding=PublisherDocumentContainerStylePadding(None),
                        padding_bottom=PublisherDocumentContainerStylePadding(None),
                        padding_left=PublisherDocumentContainerStylePadding(None),
                        padding_right=PublisherDocumentContainerStylePadding(None),
                        padding_top=PublisherDocumentContainerStylePadding(None),
                        text_color="text_color_example",
                        text_overflow="shrink",
                        text_style="title",
                        text_transform="none",
                        vertical_align="top",
                    ),
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                version="2",
            ),
            id="id1",
            type="pageTemplate",
        ),
    ) # JsonApiPublisherDocumentPageTemplatePostOptionalIdDocument | 
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Page Template
        api_response = api_instance.create_entity_page_templates(workspace_id, json_api_publisher_document_page_template_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->create_entity_page_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Page Template
        api_response = api_instance.create_entity_page_templates(workspace_id, json_api_publisher_document_page_template_post_optional_id_document, include=include, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->create_entity_page_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_publisher_document_page_template_post_optional_id_document** | [**JsonApiPublisherDocumentPageTemplatePostOptionalIdDocument**](JsonApiPublisherDocumentPageTemplatePostOptionalIdDocument.md)|  |
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiPublisherDocumentPageTemplateOutDocument**](JsonApiPublisherDocumentPageTemplateOutDocument.md)

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

# **delete_entity_page_templates**
> delete_entity_page_templates(workspace_id, object_id)

Delete a Page Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Page Template
        api_instance.delete_entity_page_templates(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->delete_entity_page_templates: %s\n" % e)
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

# **get_all_entities_page_templates**
> JsonApiPublisherDocumentPageTemplateOutList get_all_entities_page_templates(workspace_id)

Get all Page Templates

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from gooddata_api_client.model.json_api_publisher_document_page_template_out_list import JsonApiPublisherDocumentPageTemplateOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "version==someString;title==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all Page Templates
        api_response = api_instance.get_all_entities_page_templates(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->get_all_entities_page_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Page Templates
        api_response = api_instance.get_all_entities_page_templates(workspace_id, origin=origin, filter=filter, include=include, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->get_all_entities_page_templates: %s\n" % e)
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

[**JsonApiPublisherDocumentPageTemplateOutList**](JsonApiPublisherDocumentPageTemplateOutList.md)

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

# **get_entity_page_templates**
> JsonApiPublisherDocumentPageTemplateOutDocument get_entity_page_templates(workspace_id, object_id)

Get a Page Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from gooddata_api_client.model.json_api_publisher_document_page_template_out_document import JsonApiPublisherDocumentPageTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "version==someString;title==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Page Template
        api_response = api_instance.get_entity_page_templates(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->get_entity_page_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Page Template
        api_response = api_instance.get_entity_page_templates(workspace_id, object_id, filter=filter, include=include, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->get_entity_page_templates: %s\n" % e)
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

[**JsonApiPublisherDocumentPageTemplateOutDocument**](JsonApiPublisherDocumentPageTemplateOutDocument.md)

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

# **patch_entity_page_templates**
> JsonApiPublisherDocumentPageTemplateOutDocument patch_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_patch_document)

Patch a Page Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from gooddata_api_client.model.json_api_publisher_document_page_template_patch_document import JsonApiPublisherDocumentPageTemplatePatchDocument
from gooddata_api_client.model.json_api_publisher_document_page_template_out_document import JsonApiPublisherDocumentPageTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_publisher_document_page_template_patch_document = JsonApiPublisherDocumentPageTemplatePatchDocument(
        data=JsonApiPublisherDocumentPageTemplatePatch(
            attributes=JsonApiPublisherDocumentPageTemplatePatchAttributes(
                are_relations_valid=True,
                content=JsonApiPublisherDocumentPageTemplateInAttributesContent(
                    filters=[
                        PublisherDocumentFilter(),
                    ],
                    kind="cover",
                    layout=PublisherDocumentLayoutNode(),
                    notes="notes_example",
                    page_size="widescreen",
                    style=PublisherDocumentPageStyle(
                        background_color="background_color_example",
                        background_fit="cover",
                        background_horizontal_align="left",
                        background_image="background_image_example",
                        background_image_opacity=0,
                        background_offset=0,
                        background_offset_bottom=0,
                        background_offset_left=0,
                        background_offset_right=0,
                        background_offset_top=0,
                        background_opacity=0,
                        background_vertical_align="top",
                        font_size=0,
                        font_style="normal",
                        font_weight=1,
                        gap=PublisherDocumentAreaStyleGap(None),
                        horizontal_align="left",
                        letter_spacing=3.14,
                        line_height=3.14,
                        padding=PublisherDocumentContainerStylePadding(None),
                        padding_bottom=PublisherDocumentContainerStylePadding(None),
                        padding_left=PublisherDocumentContainerStylePadding(None),
                        padding_right=PublisherDocumentContainerStylePadding(None),
                        padding_top=PublisherDocumentContainerStylePadding(None),
                        text_color="text_color_example",
                        text_overflow="shrink",
                        text_style="title",
                        text_transform="none",
                        vertical_align="top",
                    ),
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                version="2",
            ),
            id="id1",
            type="pageTemplate",
        ),
    ) # JsonApiPublisherDocumentPageTemplatePatchDocument | 
    filter = "version==someString;title==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Page Template
        api_response = api_instance.patch_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->patch_entity_page_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Page Template
        api_response = api_instance.patch_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_patch_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->patch_entity_page_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_publisher_document_page_template_patch_document** | [**JsonApiPublisherDocumentPageTemplatePatchDocument**](JsonApiPublisherDocumentPageTemplatePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiPublisherDocumentPageTemplateOutDocument**](JsonApiPublisherDocumentPageTemplateOutDocument.md)

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

# **update_entity_page_templates**
> JsonApiPublisherDocumentPageTemplateOutDocument update_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_in_document)

Put a Page Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import page_template_controller_api
from gooddata_api_client.model.json_api_publisher_document_page_template_in_document import JsonApiPublisherDocumentPageTemplateInDocument
from gooddata_api_client.model.json_api_publisher_document_page_template_out_document import JsonApiPublisherDocumentPageTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = page_template_controller_api.PageTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_publisher_document_page_template_in_document = JsonApiPublisherDocumentPageTemplateInDocument(
        data=JsonApiPublisherDocumentPageTemplateIn(
            attributes=JsonApiPublisherDocumentPageTemplateInAttributes(
                are_relations_valid=True,
                content=JsonApiPublisherDocumentPageTemplateInAttributesContent(
                    filters=[
                        PublisherDocumentFilter(),
                    ],
                    kind="cover",
                    layout=PublisherDocumentLayoutNode(),
                    notes="notes_example",
                    page_size="widescreen",
                    style=PublisherDocumentPageStyle(
                        background_color="background_color_example",
                        background_fit="cover",
                        background_horizontal_align="left",
                        background_image="background_image_example",
                        background_image_opacity=0,
                        background_offset=0,
                        background_offset_bottom=0,
                        background_offset_left=0,
                        background_offset_right=0,
                        background_offset_top=0,
                        background_opacity=0,
                        background_vertical_align="top",
                        font_size=0,
                        font_style="normal",
                        font_weight=1,
                        gap=PublisherDocumentAreaStyleGap(None),
                        horizontal_align="left",
                        letter_spacing=3.14,
                        line_height=3.14,
                        padding=PublisherDocumentContainerStylePadding(None),
                        padding_bottom=PublisherDocumentContainerStylePadding(None),
                        padding_left=PublisherDocumentContainerStylePadding(None),
                        padding_right=PublisherDocumentContainerStylePadding(None),
                        padding_top=PublisherDocumentContainerStylePadding(None),
                        text_color="text_color_example",
                        text_overflow="shrink",
                        text_style="title",
                        text_transform="none",
                        vertical_align="top",
                    ),
                ),
                description="description_example",
                tags=[
                    "tags_example",
                ],
                title="title_example",
                version="2",
            ),
            id="id1",
            type="pageTemplate",
        ),
    ) # JsonApiPublisherDocumentPageTemplateInDocument | 
    filter = "version==someString;title==someString;createdBy.id==321;modifiedBy.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    include = [
        "createdBy,modifiedBy",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Page Template
        api_response = api_instance.update_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->update_entity_page_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Page Template
        api_response = api_instance.update_entity_page_templates(workspace_id, object_id, json_api_publisher_document_page_template_in_document, filter=filter, include=include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PageTemplateControllerApi->update_entity_page_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_publisher_document_page_template_in_document** | [**JsonApiPublisherDocumentPageTemplateInDocument**](JsonApiPublisherDocumentPageTemplateInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiPublisherDocumentPageTemplateOutDocument**](JsonApiPublisherDocumentPageTemplateOutDocument.md)

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

