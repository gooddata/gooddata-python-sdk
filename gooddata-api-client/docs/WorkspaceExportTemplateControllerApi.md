# gooddata_api_client.WorkspaceExportTemplateControllerApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#create_entity_workspace_export_templates) | **POST** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates | Post Workspace Export Template
[**delete_entity_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#delete_entity_workspace_export_templates) | **DELETE** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates/{objectId} | Delete a Workspace Export Template
[**get_all_entities_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#get_all_entities_workspace_export_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates | Get all Workspace Export Templates
[**get_entity_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#get_entity_workspace_export_templates) | **GET** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates/{objectId} | Get a Workspace Export Template
[**patch_entity_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#patch_entity_workspace_export_templates) | **PATCH** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates/{objectId} | Patch a Workspace Export Template
[**update_entity_workspace_export_templates**](WorkspaceExportTemplateControllerApi.md#update_entity_workspace_export_templates) | **PUT** /api/v1/entities/workspaces/{workspaceId}/workspaceExportTemplates/{objectId} | Put a Workspace Export Template


# **create_entity_workspace_export_templates**
> JsonApiWorkspaceExportTemplateOutDocument create_entity_workspace_export_templates(workspace_id, json_api_workspace_export_template_post_optional_id_document)

Post Workspace Export Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from gooddata_api_client.model.json_api_workspace_export_template_post_optional_id_document import JsonApiWorkspaceExportTemplatePostOptionalIdDocument
from gooddata_api_client.model.json_api_workspace_export_template_out_document import JsonApiWorkspaceExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    json_api_workspace_export_template_post_optional_id_document = JsonApiWorkspaceExportTemplatePostOptionalIdDocument(
        data=JsonApiWorkspaceExportTemplatePostOptionalId(
            attributes=JsonApiWorkspaceExportTemplateInAttributes(
                dashboard_slides_template=JsonApiWorkspaceExportTemplateInAttributesDashboardSlidesTemplate(
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
                widget_slides_template=JsonApiWorkspaceExportTemplateInAttributesWidgetSlidesTemplate(
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
            type="workspaceExportTemplate",
        ),
    ) # JsonApiWorkspaceExportTemplatePostOptionalIdDocument | 
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Post Workspace Export Template
        api_response = api_instance.create_entity_workspace_export_templates(workspace_id, json_api_workspace_export_template_post_optional_id_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->create_entity_workspace_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Post Workspace Export Template
        api_response = api_instance.create_entity_workspace_export_templates(workspace_id, json_api_workspace_export_template_post_optional_id_document, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->create_entity_workspace_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **json_api_workspace_export_template_post_optional_id_document** | [**JsonApiWorkspaceExportTemplatePostOptionalIdDocument**](JsonApiWorkspaceExportTemplatePostOptionalIdDocument.md)|  |
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceExportTemplateOutDocument**](JsonApiWorkspaceExportTemplateOutDocument.md)

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

# **delete_entity_workspace_export_templates**
> delete_entity_workspace_export_templates(workspace_id, object_id)

Delete a Workspace Export Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Delete a Workspace Export Template
        api_instance.delete_entity_workspace_export_templates(workspace_id, object_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->delete_entity_workspace_export_templates: %s\n" % e)
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

# **get_all_entities_workspace_export_templates**
> JsonApiWorkspaceExportTemplateOutList get_all_entities_workspace_export_templates(workspace_id)

Get all Workspace Export Templates

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from gooddata_api_client.model.json_api_workspace_export_template_out_list import JsonApiWorkspaceExportTemplateOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    origin = "ALL" # str |  (optional) if omitted the server will use the default value of "ALL"
    filter = "name==someString;dashboardSlidesTemplate==WorkspaceDashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
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
        # Get all Workspace Export Templates
        api_response = api_instance.get_all_entities_workspace_export_templates(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->get_all_entities_workspace_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get all Workspace Export Templates
        api_response = api_instance.get_all_entities_workspace_export_templates(workspace_id, origin=origin, filter=filter, page=page, size=size, sort=sort, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->get_all_entities_workspace_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **origin** | **str**|  | [optional] if omitted the server will use the default value of "ALL"
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **page** | **int**| Zero-based page index (0..N) | [optional] if omitted the server will use the default value of 0
 **size** | **int**| The size of the page to be returned | [optional] if omitted the server will use the default value of 20
 **sort** | **[str]**| Sorting criteria in the format: property,(asc|desc). Default sort order is ascending. Multiple sort criteria are supported. | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceExportTemplateOutList**](JsonApiWorkspaceExportTemplateOutList.md)

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

# **get_entity_workspace_export_templates**
> JsonApiWorkspaceExportTemplateOutDocument get_entity_workspace_export_templates(workspace_id, object_id)

Get a Workspace Export Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from gooddata_api_client.model.json_api_workspace_export_template_out_document import JsonApiWorkspaceExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    filter = "name==someString;dashboardSlidesTemplate==WorkspaceDashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)
    x_gdc_validate_relations = False # bool |  (optional) if omitted the server will use the default value of False
    meta_include = [
        "metaInclude=origin,all",
    ] # [str] | Include Meta objects. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get a Workspace Export Template
        api_response = api_instance.get_entity_workspace_export_templates(workspace_id, object_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->get_entity_workspace_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a Workspace Export Template
        api_response = api_instance.get_entity_workspace_export_templates(workspace_id, object_id, filter=filter, x_gdc_validate_relations=x_gdc_validate_relations, meta_include=meta_include)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->get_entity_workspace_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]
 **x_gdc_validate_relations** | **bool**|  | [optional] if omitted the server will use the default value of False
 **meta_include** | **[str]**| Include Meta objects. | [optional]

### Return type

[**JsonApiWorkspaceExportTemplateOutDocument**](JsonApiWorkspaceExportTemplateOutDocument.md)

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

# **patch_entity_workspace_export_templates**
> JsonApiWorkspaceExportTemplateOutDocument patch_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_patch_document)

Patch a Workspace Export Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from gooddata_api_client.model.json_api_workspace_export_template_patch_document import JsonApiWorkspaceExportTemplatePatchDocument
from gooddata_api_client.model.json_api_workspace_export_template_out_document import JsonApiWorkspaceExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_export_template_patch_document = JsonApiWorkspaceExportTemplatePatchDocument(
        data=JsonApiWorkspaceExportTemplatePatch(
            attributes=JsonApiWorkspaceExportTemplatePatchAttributes(
                dashboard_slides_template=JsonApiWorkspaceExportTemplateInAttributesDashboardSlidesTemplate(
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
                widget_slides_template=JsonApiWorkspaceExportTemplateInAttributesWidgetSlidesTemplate(
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
            type="workspaceExportTemplate",
        ),
    ) # JsonApiWorkspaceExportTemplatePatchDocument | 
    filter = "name==someString;dashboardSlidesTemplate==WorkspaceDashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Patch a Workspace Export Template
        api_response = api_instance.patch_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_patch_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->patch_entity_workspace_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Patch a Workspace Export Template
        api_response = api_instance.patch_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_patch_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->patch_entity_workspace_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_export_template_patch_document** | [**JsonApiWorkspaceExportTemplatePatchDocument**](JsonApiWorkspaceExportTemplatePatchDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceExportTemplateOutDocument**](JsonApiWorkspaceExportTemplateOutDocument.md)

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

# **update_entity_workspace_export_templates**
> JsonApiWorkspaceExportTemplateOutDocument update_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_in_document)

Put a Workspace Export Template

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import workspace_export_template_controller_api
from gooddata_api_client.model.json_api_workspace_export_template_out_document import JsonApiWorkspaceExportTemplateOutDocument
from gooddata_api_client.model.json_api_workspace_export_template_in_document import JsonApiWorkspaceExportTemplateInDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = workspace_export_template_controller_api.WorkspaceExportTemplateControllerApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    object_id = "objectId_example" # str | 
    json_api_workspace_export_template_in_document = JsonApiWorkspaceExportTemplateInDocument(
        data=JsonApiWorkspaceExportTemplateIn(
            attributes=JsonApiWorkspaceExportTemplateInAttributes(
                dashboard_slides_template=JsonApiWorkspaceExportTemplateInAttributesDashboardSlidesTemplate(
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
                widget_slides_template=JsonApiWorkspaceExportTemplateInAttributesWidgetSlidesTemplate(
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
            type="workspaceExportTemplate",
        ),
    ) # JsonApiWorkspaceExportTemplateInDocument | 
    filter = "name==someString;dashboardSlidesTemplate==WorkspaceDashboardSlidesTemplateValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title=='Some Title';description=='desc'). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty=='Value 123'). (optional)

    # example passing only required values which don't have defaults set
    try:
        # Put a Workspace Export Template
        api_response = api_instance.update_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_in_document)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->update_entity_workspace_export_templates: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Put a Workspace Export Template
        api_response = api_instance.update_entity_workspace_export_templates(workspace_id, object_id, json_api_workspace_export_template_in_document, filter=filter)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling WorkspaceExportTemplateControllerApi->update_entity_workspace_export_templates: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **object_id** | **str**|  |
 **json_api_workspace_export_template_in_document** | [**JsonApiWorkspaceExportTemplateInDocument**](JsonApiWorkspaceExportTemplateInDocument.md)|  |
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser. You can specify any object parameter and parameter of related entity (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;). Additionally, if the entity relationship represents a polymorphic entity type, it can be casted to its subtypes (for example relatedEntity::subtype.subtypeProperty&#x3D;&#x3D;&#39;Value 123&#39;). | [optional]

### Return type

[**JsonApiWorkspaceExportTemplateOutDocument**](JsonApiWorkspaceExportTemplateOutDocument.md)

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

