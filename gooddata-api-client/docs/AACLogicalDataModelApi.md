# gooddata_api_client.AACLogicalDataModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logical_model_aac**](AACLogicalDataModelApi.md#get_logical_model_aac) | **GET** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Get logical model in AAC format
[**set_logical_model_aac**](AACLogicalDataModelApi.md#set_logical_model_aac) | **PUT** /api/v1/aac/workspaces/{workspaceId}/logicalModel | Set logical model from AAC format


# **get_logical_model_aac**
> AacLogicalModel get_logical_model_aac(workspace_id)

Get logical model in AAC format

             Retrieve the logical data model of the workspace in Analytics as Code format.                          The returned format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. Use this for exporting models             that can be directly used as YAML configuration files.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_logical_data_model_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_logical_data_model_api.AACLogicalDataModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    include_parents = True # bool |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACLogicalDataModelApi->get_logical_model_aac: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get logical model in AAC format
        api_response = api_instance.get_logical_model_aac(workspace_id, include_parents=include_parents)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACLogicalDataModelApi->get_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_parents** | **bool**|  | [optional]

### Return type

[**AacLogicalModel**](AacLogicalModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model in AAC format. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_logical_model_aac**
> set_logical_model_aac(workspace_id, aac_logical_model)

Set logical model from AAC format

             Set the logical data model of the workspace using Analytics as Code format.                          The input format is compatible with the YAML definitions used by the              GoodData Analytics as Code VSCode extension. This replaces the entire              logical model with the provided definition.         

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import aac_logical_data_model_api
from gooddata_api_client.model.aac_logical_model import AacLogicalModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = aac_logical_data_model_api.AACLogicalDataModelApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    aac_logical_model = AacLogicalModel(
        datasets=[
            AacDataset(
                data_source="my-postgres",
                description="description_example",
                fields={
                    "key": AacField(
                        aggregated_as="SUM",
                        assigned_to="assigned_to_example",
                        data_type="STRING",
                        default_view="default_view_example",
                        description="description_example",
                        is_hidden=True,
                        labels={
                            "key": AacLabel(
                                data_type="INT",
                                description="description_example",
                                geo_area_config=AacGeoAreaConfig(
                                    collection=AacGeoCollectionIdentifier(
                                        id="id_example",
                                        kind="STATIC",
                                    ),
                                ),
                                is_hidden=True,
                                locale="locale_example",
                                show_in_ai_results=True,
                                source_column="source_column_example",
                                tags=[
                                    "tags_example",
                                ],
                                title="title_example",
                                translations=[
                                    AacLabelTranslation(
                                        locale="locale_example",
                                        source_column="source_column_example",
                                    ),
                                ],
                                value_type="TEXT",
                            ),
                        },
                        locale="locale_example",
                        show_in_ai_results=True,
                        sort_column="sort_column_example",
                        sort_direction="ASC",
                        source_column="source_column_example",
                        tags=[
                            "tags_example",
                        ],
                        title="title_example",
                        type="attribute",
                    ),
                },
                id="customers",
                precedence=1,
                primary_key=AacDatasetPrimaryKey(None),
                references=[
                    AacReference(
                        dataset="orders",
                        multi_directional=True,
                        sources=[
                            AacReferenceSource(
                                data_type="INT",
                                source_column="source_column_example",
                                target="target_example",
                            ),
                        ],
                    ),
                ],
                sql="sql_example",
                table_path="public/customers",
                tags=[
                    "tags_example",
                ],
                title="Customers",
                type="dataset",
                workspace_data_filters=[
                    AacWorkspaceDataFilter(
                        data_type="INT",
                        filter_id="filter_id_example",
                        source_column="source_column_example",
                    ),
                ],
            ),
        ],
        date_datasets=[
            AacDateDataset(
                description="description_example",
                granularities=[
                    "granularities_example",
                ],
                id="date",
                tags=[
                    "tags_example",
                ],
                title="Date",
                title_base="title_base_example",
                title_pattern="title_pattern_example",
                type="date",
            ),
        ],
    ) # AacLogicalModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model from AAC format
        api_instance.set_logical_model_aac(workspace_id, aac_logical_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling AACLogicalDataModelApi->set_logical_model_aac: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **aac_logical_model** | [**AacLogicalModel**](AacLogicalModel.md)|  |

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
**204** | Logical model successfully set. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

