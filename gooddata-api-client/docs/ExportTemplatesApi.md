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
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from gooddata_api_client.model.json_api_export_template_post_optional_id_document import JsonApiExportTemplatePostOptionalIdDocument
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    json_api_export_template_post_optional_id_document = JsonApiExportTemplatePostOptionalIdDocument(
        data=JsonApiExportTemplatePostOptionalId(
            attributes=JsonApiExportTemplateInAttributes(
                dashboard_slides_template=JsonApiExportTemplateInAttributesDashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                name="name_example",
                widget_slides_template=JsonApiExportTemplateInAttributesWidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    ) # JsonApiExportTemplatePostOptionalIdDocument | 

    # example passing only required values which don't have defaults set
    try:
        # Post Export Template entities
        api_response = api_instance.create_entity_export_templates(json_api_export_template_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **delete_entity_export_templates**
> delete_entity_export_templates(id)

Delete Export Template entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Delete Export Template entity
        api_instance.delete_entity_export_templates(id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->delete_entity_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Delete Export Template entity
        api_instance.delete_entity_export_templates(id, filter=filter)
    except gooddata_api_client.ApiException as e:
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
> JsonApiExportTemplateOutList get_all_entities_export_templates()

GET all Export Template entities

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_list import JsonApiExportTemplateOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    filter = "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    page = 0 # int | Zero-based page index (0..N) (optional) if omitted the server will use the default value of 0
    size = 20 # int | The size of the page to be returned (optional) if omitted the server will use the default value of 20
    sort = [
        "sort_example",
    ] # [str] | Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. (optional)
    meta_include = [
        "metaInclude=page,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # GET all Export Template entities
        api_response = api_instance.get_all_entities_export_templates(filter=filter, page=page, size=size, sort=sort, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->get_all_entities_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiExportTemplateOutList**](JsonApiExportTemplateOutList.md)

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

# **get_entity_export_templates**
> JsonApiExportTemplateOutDocument get_entity_export_templates(id)

GET Export Template entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    filter = "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->get_entity_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(id, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **patch_entity_export_templates**
> JsonApiExportTemplateOutDocument patch_entity_export_templates(id, json_api_export_template_patch_document)

Patch Export Template entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.model.json_api_export_template_patch_document import JsonApiExportTemplatePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_export_template_patch_document = JsonApiExportTemplatePatchDocument(
        data=JsonApiExportTemplatePatch(
            attributes=JsonApiExportTemplatePatchAttributes(
                dashboard_slides_template=JsonApiExportTemplateInAttributesDashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                name="name_example",
                widget_slides_template=JsonApiExportTemplateInAttributesWidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    ) # JsonApiExportTemplatePatchDocument | 
    filter = "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(id, json_api_export_template_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->patch_entity_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(id, json_api_export_template_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **update_entity_export_templates**
> JsonApiExportTemplateOutDocument update_entity_export_templates(id, json_api_export_template_in_document)

PUT Export Template entity

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import export_templates_api
from gooddata_api_client.model.json_api_export_template_in_document import JsonApiExportTemplateInDocument
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)
    id = "/6bUUGjjNSwg0_bs" # str | 
    json_api_export_template_in_document = JsonApiExportTemplateInDocument(
        data=JsonApiExportTemplateIn(
            attributes=JsonApiExportTemplateInAttributes(
                dashboard_slides_template=JsonApiExportTemplateInAttributesDashboardSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field='''About:
{{dashboardDescription}}

{{dashboardFilters}}''',
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
                name="name_example",
                widget_slides_template=JsonApiExportTemplateInAttributesWidgetSlidesTemplate(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                        header=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
                    ),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    ) # JsonApiExportTemplateInDocument | 
    filter = "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(id, json_api_export_template_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->update_entity_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(id, json_api_export_template_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
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

 - **Content-Type**: application/json, application/vnd.gooddata.api+json
 - **Accept**: application/json, application/vnd.gooddata.api+json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Request successfully processed |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

