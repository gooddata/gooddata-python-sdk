# gooddata_api_client.ExportTemplatesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_export_templates**](ExportTemplatesApi.md#create_entity_export_templates) | **POST** /api/v1/entities/exportTemplates | Post Export Template entities
[**delete_entity_export_templates**](ExportTemplatesApi.md#delete_entity_export_templates) | **DELETE** /api/v1/entities/exportTemplates/{id} | Delete Export Template entity
[**get_all_entities_export_templates**](ExportTemplatesApi.md#get_all_entities_export_templates) | **GET** /api/v1/entities/exportTemplates | GET all Export Template entities
[**get_entity_export_templates**](ExportTemplatesApi.md#get_entity_export_templates) | **GET** /api/v1/entities/exportTemplates/{id} | GET Export Template entity
[**patch_entity_export_templates**](ExportTemplatesApi.md#patch_entity_export_templates) | **PATCH** /api/v1/entities/exportTemplates/{id} | Patch Export Template entity
[**update_entity_export_templates**](ExportTemplatesApi.md#update_entity_export_templates) | **PUT** /api/v1/entities/exportTemplates/{id} | PUT Export Template entity


# **create_entity_export_templates**
> JsonApiExportTemplateOutDocument create_entity_export_templates(json_api_export_template_post_optional_id_document)

Post Export Template entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.models.json_api_export_template_post_optional_id_document import JsonApiExportTemplatePostOptionalIdDocument
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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    json_api_export_template_post_optional_id_document = gooddata_api_client.JsonApiExportTemplatePostOptionalIdDocument() # JsonApiExportTemplatePostOptionalIdDocument | 

    try:
        # Post Export Template entities
        api_response = api_instance.create_entity_export_templates(json_api_export_template_post_optional_id_document)
        print("The response of ExportTemplatesApi->create_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->create_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **json_api_export_template_post_optional_id_document** | [**JsonApiExportTemplatePostOptionalIdDocument**](JsonApiExportTemplatePostOptionalIdDocument.md)|  | 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **delete_entity_export_templates**
> delete_entity_export_templates(id, filter=filter)

Delete Export Template entity

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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Delete Export Template entity
        api_instance.delete_entity_export_templates(id, filter=filter)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->delete_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
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

# **get_all_entities_export_templates**
> JsonApiExportTemplateOutList get_all_entities_export_templates(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)

GET all Export Template entities

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_list import JsonApiExportTemplateOutList
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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) (default to 0)
    size = 20 # int | The size of the page to be returned (optional) (default to 20)
    sort = ['sort_example'] # List[str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = ['metaInclude=page,all'] # List[str] | Include Meta objects. (optional)

    try:
        # GET all Export Template entities
        api_response = api_instance.get_all_entities_export_templates(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        print("The response of ExportTemplatesApi->get_all_entities_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->get_all_entities_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 
 **page** | **int**| Zero-based page index (0..N) | [optional] [default to 0]
 **size** | **int**| The size of the page to be returned | [optional] [default to 20]
 **sort** | [**List[str]**](str.md)| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional] 
 **meta_include** | [**List[str]**](str.md)| Include Meta objects. | [optional] 

### Return type

[**JsonApiExportTemplateOutList**](JsonApiExportTemplateOutList.md)

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

# **get_entity_export_templates**
> JsonApiExportTemplateOutDocument get_entity_export_templates(id, filter=filter)

GET Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    id = 'id_example' # str | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(id, filter=filter)
        print("The response of ExportTemplatesApi->get_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->get_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **patch_entity_export_templates**
> JsonApiExportTemplateOutDocument patch_entity_export_templates(id, json_api_export_template_patch_document, filter=filter)

Patch Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.models.json_api_export_template_patch_document import JsonApiExportTemplatePatchDocument
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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    id = 'id_example' # str | 
    json_api_export_template_patch_document = gooddata_api_client.JsonApiExportTemplatePatchDocument() # JsonApiExportTemplatePatchDocument | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(id, json_api_export_template_patch_document, filter=filter)
        print("The response of ExportTemplatesApi->patch_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->patch_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_export_template_patch_document** | [**JsonApiExportTemplatePatchDocument**](JsonApiExportTemplatePatchDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

# **update_entity_export_templates**
> JsonApiExportTemplateOutDocument update_entity_export_templates(id, json_api_export_template_in_document, filter=filter)

PUT Export Template entity

### Example


```python
import gooddata_api_client
from gooddata_api_client.models.json_api_export_template_in_document import JsonApiExportTemplateInDocument
from gooddata_api_client.models.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
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
    api_instance = gooddata_api_client.ExportTemplatesApi(api_client)
    id = 'id_example' # str | 
    json_api_export_template_in_document = gooddata_api_client.JsonApiExportTemplateInDocument() # JsonApiExportTemplateInDocument | 
    filter = 'name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue' # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(id, json_api_export_template_in_document, filter=filter)
        print("The response of ExportTemplatesApi->update_entity_export_templates:\n")
        pprint(api_response)
    except Exception as e:
        print("Exception when calling ExportTemplatesApi->update_entity_export_templates: %s\n" % e)
```



### Parameters


Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  | 
 **json_api_export_template_in_document** | [**JsonApiExportTemplateInDocument**](JsonApiExportTemplateInDocument.md)|  | 
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional] 

### Return type

[**JsonApiExportTemplateOutDocument**](JsonApiExportTemplateOutDocument.md)

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

