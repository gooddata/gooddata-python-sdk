# gooddata_api_client.ActionsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**all_platform_usage**](ActionsApi.md#all_platform_usage) | **GET** /api/v1/actions/collectUsage | Info about the platform usage.
[**available_assignees**](ActionsApi.md#available_assignees) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/availableAssignees | Get Available Assignees
[**check_entity_overrides**](ActionsApi.md#check_entity_overrides) | **POST** /api/v1/actions/workspaces/{workspaceId}/checkEntityOverrides | Finds entities with given ID in hierarchy.
[**compute_label_elements_post**](ActionsApi.md#compute_label_elements_post) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
[**compute_report**](ActionsApi.md#compute_report) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute | Executes analytical request and returns link to the result
[**compute_valid_objects**](ActionsApi.md#compute_valid_objects) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/computeValidObjects | Valid objects
[**create_pdf_export**](ActionsApi.md#create_pdf_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/visual | Create visual - pdf export request
[**create_tabular_export**](ActionsApi.md#create_tabular_export) | **POST** /api/v1/actions/workspaces/{workspaceId}/export/tabular | Create tabular export request
[**dashboard_permissions**](ActionsApi.md#dashboard_permissions) | **GET** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/permissions | Get Dashboard Permissions
[**explain_afm**](ActionsApi.md#explain_afm) | **POST** /api/v1/actions/workspaces/{workspaceId}/execution/afm/explain | AFM explain resource.
[**generate_logical_model**](ActionsApi.md#generate_logical_model) | **POST** /api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate logical data model (LDM) from physical data model (PDM)
[**get_data_source_schemata**](ActionsApi.md#get_data_source_schemata) | **GET** /api/v1/actions/dataSources/{dataSourceId}/scanSchemata | Get a list of schema names of a database
[**get_dependent_entities_graph**](ActionsApi.md#get_dependent_entities_graph) | **GET** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph
[**get_dependent_entities_graph_from_entry_points**](ActionsApi.md#get_dependent_entities_graph_from_entry_points) | **POST** /api/v1/actions/workspaces/{workspaceId}/dependentEntitiesGraph | Computes the dependent entities graph from given entry points
[**get_exported_file**](ActionsApi.md#get_exported_file) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId} | Retrieve exported files
[**get_metadata**](ActionsApi.md#get_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/visual/{exportId}/metadata | Retrieve metadata context
[**get_tabular_export**](ActionsApi.md#get_tabular_export) | **GET** /api/v1/actions/workspaces/{workspaceId}/export/tabular/{exportId} | Retrieve exported files
[**inherited_entity_conflicts**](ActionsApi.md#inherited_entity_conflicts) | **GET** /api/v1/actions/workspaces/{workspaceId}/inheritedEntityConflicts | Finds API identifier conflicts in given workspace hierarchy.
[**manage_dashboard_permissions**](ActionsApi.md#manage_dashboard_permissions) | **POST** /api/v1/actions/workspaces/{workspaceId}/analyticalDashboards/{dashboardId}/managePermissions | Manage Permissions for a Dashboard
[**overridden_child_entities**](ActionsApi.md#overridden_child_entities) | **GET** /api/v1/actions/workspaces/{workspaceId}/overriddenChildEntities | Finds API identifier overrides in given workspace hierarchy.
[**particular_platform_usage**](ActionsApi.md#particular_platform_usage) | **POST** /api/v1/actions/collectUsage | Info about the platform usage for particular items.
[**register_upload_notification**](ActionsApi.md#register_upload_notification) | **POST** /api/v1/actions/dataSources/{dataSourceId}/uploadNotification | Register an upload notification
[**resolve_all_entitlements**](ActionsApi.md#resolve_all_entitlements) | **GET** /api/v1/actions/resolveEntitlements | Values for all public entitlements.
[**resolve_all_settings_without_workspace**](ActionsApi.md#resolve_all_settings_without_workspace) | **GET** /api/v1/actions/resolveSettings | Values for all settings without workspace.
[**resolve_requested_entitlements**](ActionsApi.md#resolve_requested_entitlements) | **POST** /api/v1/actions/resolveEntitlements | Values for requested public entitlements.
[**resolve_settings_without_workspace**](ActionsApi.md#resolve_settings_without_workspace) | **POST** /api/v1/actions/resolveSettings | Values for selected settings without workspace.
[**retrieve_execution_metadata**](ActionsApi.md#retrieve_execution_metadata) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId}/metadata | Get a single execution result&#39;s metadata.
[**retrieve_result**](ActionsApi.md#retrieve_result) | **GET** /api/v1/actions/workspaces/{workspaceId}/execution/afm/execute/result/{resultId} | Get a single execution result
[**scan_data_source**](ActionsApi.md#scan_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scan | Scan a database to get a physical data model (PDM)
[**scan_sql**](ActionsApi.md#scan_sql) | **POST** /api/v1/actions/dataSources/{dataSourceId}/scanSql | Collect metadata about SQL query
[**test_data_source**](ActionsApi.md#test_data_source) | **POST** /api/v1/actions/dataSources/{dataSourceId}/test | Test data source connection by data source id
[**test_data_source_definition**](ActionsApi.md#test_data_source_definition) | **POST** /api/v1/actions/dataSource/test | Test connection by data source definition
[**workspace_resolve_all_settings**](ActionsApi.md#workspace_resolve_all_settings) | **GET** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for all settings.
[**workspace_resolve_settings**](ActionsApi.md#workspace_resolve_settings) | **POST** /api/v1/actions/workspaces/{workspaceId}/resolveSettings | Values for selected settings.


# **all_platform_usage**
> [PlatformUsage] all_platform_usage()

Info about the platform usage.

Provides information about platform usage, like amount of users, workspaces, ...

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Info about the platform usage.
        api_response = api_instance.all_platform_usage()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->all_platform_usage: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **available_assignees**
> AvailableAssignees available_assignees(workspace_id, dashboard_id)

Get Available Assignees

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.available_assignees import AvailableAssignees
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Available Assignees
        api_response = api_instance.available_assignees(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->available_assignees: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dashboard_id** | **str**|  |

### Return type

[**AvailableAssignees**](AvailableAssignees.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **check_entity_overrides**
> [IdentifierDuplications] check_entity_overrides(workspace_id, hierarchy_object_identification)

Finds entities with given ID in hierarchy.

Finds entities with given ID in hierarchy (e.g. to check possible future conflicts).

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.hierarchy_object_identification import HierarchyObjectIdentification
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    hierarchy_object_identification = [
        HierarchyObjectIdentification(
            id="id_example",
            type="metric",
        ),
    ] # [HierarchyObjectIdentification] | 

    # example passing only required values which don't have defaults set
    try:
        # Finds entities with given ID in hierarchy.
        api_response = api_instance.check_entity_overrides(workspace_id, hierarchy_object_identification)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->check_entity_overrides: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **hierarchy_object_identification** | [**[HierarchyObjectIdentification]**](HierarchyObjectIdentification.md)|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for entities finished successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_label_elements_post**
> ElementsResponse compute_label_elements_post(workspace_id, elements_request)

Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.elements_request import ElementsRequest
from gooddata_api_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    elements_request = ElementsRequest(
        complement_filter=False,
        data_sampling_percentage=100,
        exact_filter=[
            "exact_filter_example",
        ],
        exclude_primary_label=False,
        filter_by=FilterBy(
            label_type="REQUESTED",
        ),
        label="/6bUUGjjNSwg0_bs",
        pattern_filter="pattern_filter_example",
        sort_order="ASC",
    ) # ElementsRequest | 
    offset = 0 # int | Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 0
    limit = 1000 # int | Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. (optional) if omitted the server will use the default value of 1000
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False

    # example passing only required values which don't have defaults set
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Listing of label values. The resulting data are limited by the static platform limit to the maximum of 10000 rows.
        api_response = api_instance.compute_label_elements_post(workspace_id, elements_request, offset=offset, limit=limit, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_label_elements_post: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **elements_request** | [**ElementsRequest**](ElementsRequest.md)|  |
 **offset** | **int**| Request page with this offset. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| Return only this number of items. Must be positive integer. The API is limited to the maximum of 10000 items. Therefore this parameter is limited to this number as well. | [optional] if omitted the server will use the default value of 1000
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False

### Return type

[**ElementsResponse**](ElementsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of label values. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_report**
> AfmExecutionResponse compute_report(workspace_id, afm_execution)

Executes analytical request and returns link to the result

AFM is a combination of attributes, measures and filters that describe a query you want to execute.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    ) # AfmExecution | 
    skip_cache = False # bool | Ignore all caches during execution of current request. (optional) if omitted the server will use the default value of False
    timestamp = "2020-06-03T10:15:30+01:00" # str |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Executes analytical request and returns link to the result
        api_response = api_instance.compute_report(workspace_id, afm_execution, skip_cache=skip_cache, timestamp=timestamp)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_report: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional] if omitted the server will use the default value of False
 **timestamp** | **str**|  | [optional]

### Return type

[**AfmExecutionResponse**](AfmExecutionResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | AFM Execution response with links to the result and server-enhanced dimensions from the original request. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **compute_valid_objects**
> AfmValidObjectsResponse compute_valid_objects(workspace_id, afm_valid_objects_query)

Valid objects

Returns list containing attributes, facts, or metrics, which can be added to given AFM while still keeping it computable.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.model.afm_valid_objects_response import AfmValidObjectsResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_valid_objects_query = AfmValidObjectsQuery(
        afm=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        types=[
            "facts",
        ],
    ) # AfmValidObjectsQuery | 

    # example passing only required values which don't have defaults set
    try:
        # Valid objects
        api_response = api_instance.compute_valid_objects(workspace_id, afm_valid_objects_query)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->compute_valid_objects: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_valid_objects_query** | [**AfmValidObjectsQuery**](AfmValidObjectsQuery.md)|  |

### Return type

[**AfmValidObjectsResponse**](AfmValidObjectsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of attributes, facts and metrics valid with respect to given AFM. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_pdf_export**
> ExportResponse create_pdf_export(workspace_id, pdf_export_request)

Create visual - pdf export request

An visual export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.pdf_export_request import PdfExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    pdf_export_request = PdfExportRequest(
        dashboard_id="761cd28b-3f57-4ac9-bbdc-1c552cc0d1d0",
        file_name="filename",
        metadata={},
    ) # PdfExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create visual - pdf export request
        api_response = api_instance.create_pdf_export(workspace_id, pdf_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->create_pdf_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **pdf_export_request** | [**PdfExportRequest**](PdfExportRequest.md)|  |

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Visual export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **create_tabular_export**
> ExportResponse create_tabular_export(workspace_id, tabular_export_request)

Create tabular export request

An tabular export job will be created based on the export request and put to queue to be executed. The result of the operation will be an exportResult identifier that will be assembled by the client into a url that can be polled.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.export_response import ExportResponse
from gooddata_api_client.model.tabular_export_request import TabularExportRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    tabular_export_request = TabularExportRequest(
        custom_override=CustomOverride(
            labels={
                "key": CustomLabel(
                    title="title_example",
                ),
            },
            metrics={
                "key": CustomMetric(
                    format="format_example",
                    title="title_example",
                ),
            },
        ),
        execution_result="ff483727196c9dc862c7fd3a5a84df55c96d61a4",
        file_name="result",
        format="CSV",
        settings=Settings(
            merge_headers=True,
            show_filters=False,
        ),
    ) # TabularExportRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Create tabular export request
        api_response = api_instance.create_tabular_export(workspace_id, tabular_export_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->create_tabular_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **tabular_export_request** | [**TabularExportRequest**](TabularExportRequest.md)|  |

### Return type

[**ExportResponse**](ExportResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**201** | Tabular export request created successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **dashboard_permissions**
> DashboardPermissions dashboard_permissions(workspace_id, dashboard_id)

Get Dashboard Permissions

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dashboard_permissions import DashboardPermissions
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Get Dashboard Permissions
        api_response = api_instance.dashboard_permissions(workspace_id, dashboard_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->dashboard_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dashboard_id** | **str**|  |

### Return type

[**DashboardPermissions**](DashboardPermissions.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **explain_afm**
> explain_afm(workspace_id, afm_execution)

AFM explain resource.

The resource provides static structures needed for investigation of a problem with given AFM.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.afm_execution import AfmExecution
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    afm_execution = AfmExecution(
        execution=AFM(
            attributes=[
                AttributeItem(
                    label=AfmObjectIdentifierLabel(
                        identifier=AfmObjectIdentifierLabelIdentifier(
                            id="sample_item.price",
                            type="label",
                        ),
                    ),
                    local_identifier="2",
                    show_all_values=False,
                ),
            ],
            aux_measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
            filters=[
                FilterDefinition(),
            ],
            measures=[
                MeasureItem(
                    definition=MeasureDefinition(),
                    local_identifier="metric_1",
                ),
            ],
        ),
        result_spec=ResultSpec(
            dimensions=[
                Dimension(
                    item_identifiers=["attribute_1","measureGroup"],
                    local_identifier="firstDimension",
                    sorting=[
                        SortKey(),
                    ],
                ),
            ],
            totals=[
                Total(
                    function="SUM",
                    local_identifier="firstTotal",
                    metric="metric_1",
                    total_dimensions=[
                        TotalDimension(
                            dimension_identifier="firstDimension",
                            total_dimension_items=["measureGroup"],
                        ),
                    ],
                ),
            ],
        ),
        settings=ExecutionSettings(
            data_sampling_percentage=0,
        ),
    ) # AfmExecution | 
    explain_type = "MAQL" # str | Requested explain type. If not specified all types are bundled in a ZIP archive.  `MAQL` - MAQL Abstract Syntax Tree, execution dimensions and related info  `GRPC_MODEL` - Datasets used in execution  `GRPC_MODEL_SVG` - Generated SVG image of the datasets  `WDF` - Workspace data filters in execution workspace context  `QT` - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  `QT_SVG` - Generated SVG image of the Query Tree  `OPT_QT` - Optimized Query Tree  `OPT_QT_SVG` - Generated SVG image of the Optimized Query Tree  `SQL` - Final SQL to be executed  `SETTINGS` - Settings used to execute explain request (optional)

    # example passing only required values which don't have defaults set
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # AFM explain resource.
        api_instance.explain_afm(workspace_id, afm_execution, explain_type=explain_type)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->explain_afm: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **afm_execution** | [**AfmExecution**](AfmExecution.md)|  |
 **explain_type** | **str**| Requested explain type. If not specified all types are bundled in a ZIP archive.  &#x60;MAQL&#x60; - MAQL Abstract Syntax Tree, execution dimensions and related info  &#x60;GRPC_MODEL&#x60; - Datasets used in execution  &#x60;GRPC_MODEL_SVG&#x60; - Generated SVG image of the datasets  &#x60;WDF&#x60; - Workspace data filters in execution workspace context  &#x60;QT&#x60; - Query Tree, created from MAQL AST using Logical Data Model,  contains all information needed to generate SQL  &#x60;QT_SVG&#x60; - Generated SVG image of the Query Tree  &#x60;OPT_QT&#x60; - Optimized Query Tree  &#x60;OPT_QT_SVG&#x60; - Generated SVG image of the Optimized Query Tree  &#x60;SQL&#x60; - Final SQL to be executed  &#x60;SETTINGS&#x60; - Settings used to execute explain request | [optional]

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json, application/sql, application/zip, image/svg+xml


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Requested resource |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate logical data model (LDM) from physical data model (PDM)

Generate logical data model (LDM) from physical data model (PDM) stored in data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from gooddata_api_client.model.generate_ldm_request import GenerateLdmRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    generate_ldm_request = GenerateLdmRequest(
        date_granularities="all",
        denorm_prefix="dr",
        fact_prefix="f",
        generate_long_ids=True,
        grain_prefix="g",
        grain_reference_prefix="gr",
        pdm=PdmLdmRequest(
            sqls=[
                PdmSql(
                    columns=[
                        SqlColumn(
                            data_type="INT",
                            name="customer_id",
                        ),
                    ],
                    statement="select * from abc",
                    title="My special dataset",
                ),
            ],
            tables=[
                DeclarativeTable(
                    columns=[
                        DeclarativeColumn(
                            data_type="INT",
                            is_primary_key=True,
                            name="customer_id",
                            referenced_table_column="customer_id",
                            referenced_table_id="customers",
                        ),
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="TABLE",
                ),
            ],
        ),
        primary_label_prefix="pl",
        reference_prefix="r",
        secondary_label_prefix="sl",
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
        wdf_prefix="wdf",
        workspace_id="workspace_id_example",
    ) # GenerateLdmRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Generate logical data model (LDM) from physical data model (PDM)
        api_response = api_instance.generate_logical_model(data_source_id, generate_ldm_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->generate_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **generate_ldm_request** | [**GenerateLdmRequest**](GenerateLdmRequest.md)|  |

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | LDM generated successfully. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_data_source_schemata**
> DataSourceSchemata get_data_source_schemata(data_source_id)

Get a list of schema names of a database

It scans a database and reads metadata. The result of the request contains a list of schema names of a database.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.data_source_schemata import DataSourceSchemata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id

    # example passing only required values which don't have defaults set
    try:
        # Get a list of schema names of a database
        api_response = api_instance.get_data_source_schemata(data_source_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_data_source_schemata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |

### Return type

[**DataSourceSchemata**](DataSourceSchemata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan schemata |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph**
> DependentEntitiesResponse get_dependent_entities_graph(workspace_id)

Computes the dependent entities graph

Computes the dependent entities graph

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph
        api_response = api_instance.get_dependent_entities_graph(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_dependent_entities_graph_from_entry_points**
> DependentEntitiesResponse get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)

Computes the dependent entities graph from given entry points

Computes the dependent entities graph from given entry points

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.dependent_entities_request import DependentEntitiesRequest
from gooddata_api_client.model.dependent_entities_response import DependentEntitiesResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dependent_entities_request = DependentEntitiesRequest(
        identifiers=[
            EntityIdentifier(
                id="/6bUUGjjNSwg0_bs",
                type="metric",
            ),
        ],
    ) # DependentEntitiesRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Computes the dependent entities graph from given entry points
        api_response = api_instance.get_dependent_entities_graph_from_entry_points(workspace_id, dependent_entities_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_dependent_entities_graph_from_entry_points: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dependent_entities_request** | [**DependentEntitiesRequest**](DependentEntitiesRequest.md)|  |

### Return type

[**DependentEntitiesResponse**](DependentEntitiesResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Computes the dependent entities graph from given entry points |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_exported_file**
> get_exported_file(workspace_id, export_id)

Retrieve exported files

Returns 202 until original POST export request is not processed.Returns 200 with exported data once the export is done.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_exported_file(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_exported_file: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/pdf


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_metadata**
> get_metadata(workspace_id, export_id)

Retrieve metadata context

This endpoints serves as a cache for user defined metadata for the front end ui to retrieve them, if one was created using the POST ../export/visual endpoint. The metadata structure is not verified. If metadata for given {exportId} has been found, endpoint returns the value 200 else 404.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve metadata context
        api_instance.get_metadata(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Json metadata representation |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_tabular_export**
> get_tabular_export(workspace_id, export_id)

Retrieve exported files

After clients creates a POST export request, the processing of it will start shortly asynchronously. To retrieve the result, client has to check periodically for the result on this endpoint. In case the result isn't ready yet, the service returns 202. If the result is ready, it returns 200 and octet stream of the result file with provided filename.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    export_id = "exportId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Retrieve exported files
        api_instance.get_tabular_export(workspace_id, export_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->get_tabular_export: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **export_id** | **str**|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, text/csv


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Binary export result. |  * Content-Disposition -  <br>  |
**202** | Request is accepted, provided exportId exists, but export is not yet ready. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **inherited_entity_conflicts**
> [IdentifierDuplications] inherited_entity_conflicts(workspace_id)

Finds API identifier conflicts in given workspace hierarchy.

Finds API identifier conflicts in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds API identifier conflicts in given workspace hierarchy.
        api_response = api_instance.inherited_entity_conflicts(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->inherited_entity_conflicts: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for conflicting identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **manage_dashboard_permissions**
> manage_dashboard_permissions(workspace_id, dashboard_id, permissions_for_assignee)

Manage Permissions for a Dashboard

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.permissions_for_assignee import PermissionsForAssignee
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    dashboard_id = "dashboardId_example" # str | 
    permissions_for_assignee = [
        PermissionsForAssignee(
            assignee_identifier=AssigneeIdentifier(
                id="id_example",
                type="user",
            ),
            permissions=[
                "EDIT",
            ],
        ),
    ] # [PermissionsForAssignee] | 

    # example passing only required values which don't have defaults set
    try:
        # Manage Permissions for a Dashboard
        api_instance.manage_dashboard_permissions(workspace_id, dashboard_id, permissions_for_assignee)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->manage_dashboard_permissions: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **dashboard_id** | **str**|  |
 **permissions_for_assignee** | [**[PermissionsForAssignee]**](PermissionsForAssignee.md)|  |

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
**204** | No Content |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **overridden_child_entities**
> [IdentifierDuplications] overridden_child_entities(workspace_id)

Finds API identifier overrides in given workspace hierarchy.

Finds API identifier overrides in given workspace hierarchy.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.identifier_duplications import IdentifierDuplications
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Finds API identifier overrides in given workspace hierarchy.
        api_response = api_instance.overridden_child_entities(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->overridden_child_entities: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[IdentifierDuplications]**](IdentifierDuplications.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Searching for overridden identifiers finished successfully |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **particular_platform_usage**
> [PlatformUsage] particular_platform_usage(platform_usage_request)

Info about the platform usage for particular items.

Provides information about platform usage, like amount of users, workspaces, ...

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.platform_usage_request import PlatformUsageRequest
from gooddata_api_client.model.platform_usage import PlatformUsage
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    platform_usage_request = PlatformUsageRequest(
        usage_item_names=[
            "UserCount",
        ],
    ) # PlatformUsageRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Info about the platform usage for particular items.
        api_response = api_instance.particular_platform_usage(platform_usage_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->particular_platform_usage: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **platform_usage_request** | [**PlatformUsageRequest**](PlatformUsageRequest.md)|  |

### Return type

[**[PlatformUsage]**](PlatformUsage.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **register_upload_notification**
> register_upload_notification(data_source_id)

Register an upload notification

Notification sets up all reports to be computed again with new data.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "dataSourceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Register an upload notification
        api_instance.register_upload_notification(data_source_id)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->register_upload_notification: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |

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
**204** | An upload notification has been successfully registered. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_entitlements**
> [ApiEntitlement] resolve_all_entitlements()

Values for all public entitlements.

Resolves values of available entitlements for the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all public entitlements.
        api_response = api_instance.resolve_all_entitlements()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_all_entitlements: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_all_settings_without_workspace**
> [ResolvedSetting] resolve_all_settings_without_workspace()

Values for all settings without workspace.

Resolves values for all settings without workspace by current user, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Values for all settings without workspace.
        api_response = api_instance.resolve_all_settings_without_workspace()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_all_settings_without_workspace: %s\n" % e)
```


### Parameters
This endpoint does not need any parameter.

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_requested_entitlements**
> [ApiEntitlement] resolve_requested_entitlements(entitlements_request)

Values for requested public entitlements.

Resolves values for requested entitlements in the organization.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.api_entitlement import ApiEntitlement
from gooddata_api_client.model.entitlements_request import EntitlementsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    entitlements_request = EntitlementsRequest(
        entitlements_name=[
            "CacheStrategy",
        ],
    ) # EntitlementsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for requested public entitlements.
        api_response = api_instance.resolve_requested_entitlements(entitlements_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_requested_entitlements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **entitlements_request** | [**EntitlementsRequest**](EntitlementsRequest.md)|  |

### Return type

[**[ApiEntitlement]**](ApiEntitlement.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | OK |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **resolve_settings_without_workspace**
> [ResolvedSetting] resolve_settings_without_workspace(resolve_settings_request)

Values for selected settings without workspace.

Resolves values for selected settings without workspace by current user, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings without workspace.
        api_response = api_instance.resolve_settings_without_workspace(resolve_settings_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->resolve_settings_without_workspace: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_execution_metadata**
> ResultCacheMetadata retrieve_execution_metadata(workspace_id, result_id)

Get a single execution result's metadata.

The resource provides execution result's metadata as AFM and resultSpec used in execution request and an executionResponse

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.result_cache_metadata import ResultCacheMetadata
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result's metadata.
        api_response = api_instance.retrieve_execution_metadata(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_execution_metadata: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |

### Return type

[**ResultCacheMetadata**](ResultCacheMetadata.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result&#39;s metadata was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **retrieve_result**
> ExecutionResult retrieve_result(workspace_id, result_id)

Get a single execution result

Gets a single execution result.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.execution_result import ExecutionResult
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "/6bUUGjjNSwg0_bs" # str | Workspace identifier
    result_id = "a9b28f9dc55f37ea9f4a5fb0c76895923591e781" # str | Result ID
    offset = [
        offset=1,10,
    ] # [int] | Request page with these offsets. Format is offset=1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    limit = [
        limit=1,10,
    ] # [int] | Return only this number of items. Format is limit=1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. (optional) if omitted the server will use the default value of []
    excluded_total_dimensions = [
        "excludedTotalDimensions=dim_0,dim_1",
    ] # [str] | Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. (optional) if omitted the server will use the default value of []

    # example passing only required values which don't have defaults set
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get a single execution result
        api_response = api_instance.retrieve_result(workspace_id, result_id, offset=offset, limit=limit, excluded_total_dimensions=excluded_total_dimensions)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->retrieve_result: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **result_id** | **str**| Result ID |
 **offset** | **[int]**| Request page with these offsets. Format is offset&#x3D;1,2,3,... - one offset for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **limit** | **[int]**| Return only this number of items. Format is limit&#x3D;1,2,3,... - one limit for each dimensions in ResultSpec from originating AFM. | [optional] if omitted the server will use the default value of []
 **excluded_total_dimensions** | **[str]**| Identifiers of the dimensions where grand total data should not be returned for this request. A grand total will not be returned if all of its totalDimensions are in excludedTotalDimensions. | [optional] if omitted the server will use the default value of []

### Return type

[**ExecutionResult**](ExecutionResult.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Execution result was found and returned. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_data_source**
> ScanResultPdm scan_data_source(data_source_id, scan_request)

Scan a database to get a physical data model (PDM)

It scans a database and transforms its metadata to a declarative definition of the physical data model (PDM). The result of the request contains the mentioned physical data model (PDM) of a database within warning, for example, about unsupported columns.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.scan_request import ScanRequest
from gooddata_api_client.model.scan_result_pdm import ScanResultPdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_request = ScanRequest(
        scan_tables=True,
        scan_views=True,
        schemata=["tpch","demo"],
        separator="__",
        table_prefix="out_table",
        view_prefix="out_view",
    ) # ScanRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Scan a database to get a physical data model (PDM)
        api_response = api_instance.scan_data_source(data_source_id, scan_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->scan_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **scan_request** | [**ScanRequest**](ScanRequest.md)|  |

### Return type

[**ScanResultPdm**](ScanResultPdm.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **scan_sql**
> ScanSqlResponse scan_sql(data_source_id, scan_sql_request)

Collect metadata about SQL query

It executes SQL query against specified data source and extracts metadata. Metadata consist of column names and column data types. It can optionally provide also preview of data returned by SQL query

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.scan_sql_response import ScanSqlResponse
from gooddata_api_client.model.scan_sql_request import ScanSqlRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    scan_sql_request = ScanSqlRequest(
        sql="SELECT a.special_value as result FROM tableA a",
    ) # ScanSqlRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Collect metadata about SQL query
        api_response = api_instance.scan_sql(data_source_id, scan_sql_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->scan_sql: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **scan_sql_request** | [**ScanSqlRequest**](ScanSqlRequest.md)|  |

### Return type

[**ScanSqlResponse**](ScanSqlResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the scan. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source**
> TestResponse test_data_source(data_source_id, test_request)

Test data source connection by data source id

Test if it is possible to connect to a database using an existing data source definition.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_request import TestRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    data_source_id = "myPostgres" # str | Data source id
    test_request = TestRequest(
        cache_path=[
            "cache_path_example",
        ],
        enable_caching=False,
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        schema="public",
        token="token_example",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test data source connection by data source id
        api_response = api_instance.test_data_source(data_source_id, test_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->test_data_source: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**| Data source id |
 **test_request** | [**TestRequest**](TestRequest.md)|  |

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **test_data_source_definition**
> TestResponse test_data_source_definition(test_definition_request)

Test connection by data source definition

Test if it is possible to connect to a database using a connection provided by the data source definition in the request body.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.test_response import TestResponse
from gooddata_api_client.model.test_definition_request import TestDefinitionRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    test_definition_request = TestDefinitionRequest(
        parameters=[
            DataSourceParameter(
                name="name_example",
                value="value_example",
            ),
        ],
        password="admin123",
        schema="public",
        token="token_example",
        type="POSTGRESQL",
        url="jdbc:postgresql://localhost:5432/db_name",
        username="dbadmin",
    ) # TestDefinitionRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Test connection by data source definition
        api_response = api_instance.test_data_source_definition(test_definition_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->test_data_source_definition: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **test_definition_request** | [**TestDefinitionRequest**](TestDefinitionRequest.md)|  |

### Return type

[**TestResponse**](TestResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | The result of the test of a data source connection. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_all_settings**
> [ResolvedSetting] workspace_resolve_all_settings(workspace_id)

Values for all settings.

Resolves values for all settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 

    # example passing only required values which don't have defaults set
    try:
        # Values for all settings.
        api_response = api_instance.workspace_resolve_all_settings(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_all_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **workspace_resolve_settings**
> [ResolvedSetting] workspace_resolve_settings(workspace_id, resolve_settings_request)

Values for selected settings.

Resolves value for selected settings in a workspace by current user, workspace, organization, or default settings.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import actions_api
from gooddata_api_client.model.resolved_setting import ResolvedSetting
from gooddata_api_client.model.resolve_settings_request import ResolveSettingsRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = actions_api.ActionsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    resolve_settings_request = ResolveSettingsRequest(
        settings=["timezone"],
    ) # ResolveSettingsRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Values for selected settings.
        api_response = api_instance.workspace_resolve_settings(workspace_id, resolve_settings_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ActionsApi->workspace_resolve_settings: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **resolve_settings_request** | [**ResolveSettingsRequest**](ResolveSettingsRequest.md)|  |

### Return type

[**[ResolvedSetting]**](ResolvedSetting.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Values for selected settings. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

