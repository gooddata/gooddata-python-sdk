# gooddata_api_client.LDMDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_logical_model**](LDMDeclarativeAPIsApi.md#get_logical_model) | **GET** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Get logical model
[**set_logical_model**](LDMDeclarativeAPIsApi.md#set_logical_model) | **PUT** /api/v1/layout/workspaces/{workspaceId}/logicalModel | Set logical model


# **get_logical_model**
> DeclarativeModel get_logical_model(workspace_id)

Get logical model

Retrieve current logical model of the workspace in declarative form.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ldm_declarative_apis_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ldm_declarative_apis_api.LDMDeclarativeAPIsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    include_parents = True # bool |  (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LDMDeclarativeAPIsApi->get_logical_model: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get logical model
        api_response = api_instance.get_logical_model(workspace_id, include_parents=include_parents)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LDMDeclarativeAPIsApi->get_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **include_parents** | **bool**|  | [optional]

### Return type

[**DeclarativeModel**](DeclarativeModel.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved current logical model. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **set_logical_model**
> set_logical_model(workspace_id, declarative_model)

Set logical model

Set effective logical model of the workspace.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ldm_declarative_apis_api
from gooddata_api_client.model.declarative_model import DeclarativeModel
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ldm_declarative_apis_api.LDMDeclarativeAPIsApi(api_client)
    workspace_id = "workspaceId_example" # str | 
    declarative_model = DeclarativeModel(
        ldm=DeclarativeLdm(
            dataset_extensions=[
                DeclarativeDatasetExtension(
                    id="customers",
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
            datasets=[
                DeclarativeDataset(
                    attributes=[
                        DeclarativeAttribute(
                            default_view=LabelIdentifier(
                                id="label_id",
                                type="label",
                            ),
                            description="Customer name including first and last name.",
                            id="attr.customers.customer_name",
                            labels=[
                                DeclarativeLabel(
                                    description="Customer name",
                                    id="label.customer_name",
                                    source_column="customer_name",
                                    source_column_data_type="STRING",
                                    tags=["Customers"],
                                    title="Customer name",
                                    value_type="TEXT" | "HYPERLINK" | "GEO" | "GEO_LONGITUDE" | "GEO_LATITUDE",
                                ),
                            ],
                            sort_column="customer_name",
                            sort_direction="ASC" | "DESC",
                            source_column="customer_name",
                            source_column_data_type="STRING",
                            tags=["Customers"],
                            title="Customer Name",
                        ),
                    ],
                    data_source_table_id=DataSourceTableIdentifier(
                        data_source_id="my-postgres",
                        id="customers",
                        path=["table_schema","table_name"],
                        type="dataSource",
                    ),
                    description="The customers of ours.",
                    facts=[
                        DeclarativeFact(
                            description="A number of orders created by the customer - including all orders, even the non-delivered ones.",
                            id="fact.customer_order_count",
                            source_column="customer_order_count",
                            source_column_data_type="NUMERIC",
                            tags=["Customers"],
                            title="Customer order count",
                        ),
                    ],
                    grain=[
                        GrainIdentifier(
                            id="attr.customers.customer_name",
                            type="ATTRIBUTE",
                        ),
                    ],
                    id="customers",
                    references=[
                        DeclarativeReference(
                            identifier=ReferenceIdentifier(
                                id="customers",
                                type="DATASET",
                            ),
                            multivalue=False,
                            source_column_data_types=[
                                "INT",
                            ],
                            source_columns=["customer_id"],
                        ),
                    ],
                    sql=DeclarativeDatasetSql(
                        data_source_id="my-postgres",
                        statement="SELECT * FROM some_table",
                    ),
                    tags=["Customers"],
                    title="Customers",
                    workspace_data_filter_columns=[
                        DeclarativeWorkspaceDataFilterColumn(
                            data_type="INT",
                            name="customer_id",
                        ),
                    ],
                    workspace_data_filter_references=[
                        DeclarativeWorkspaceDataFilterReferences(
                            filter_column="filter_id",
                            filter_column_data_type="INT",
                            filter_id=DatasetWorkspaceDataFilterIdentifier(
                                id="country_id",
                                type="workspaceDataFilter",
                            ),
                        ),
                    ],
                ),
            ],
            date_instances=[
                DeclarativeDateDataset(
                    description="A customer order date",
                    granularities=[
                        "MINUTE",
                    ],
                    granularities_formatting=GranularitiesFormatting(
                        title_base="title_base_example",
                        title_pattern="%titleBase - %granularityTitle",
                    ),
                    id="date",
                    tags=["Customer dates"],
                    title="Date",
                ),
            ],
        ),
    ) # DeclarativeModel | 

    # example passing only required values which don't have defaults set
    try:
        # Set logical model
        api_instance.set_logical_model(workspace_id, declarative_model)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling LDMDeclarativeAPIsApi->set_logical_model: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**|  |
 **declarative_model** | [**DeclarativeModel**](DeclarativeModel.md)|  |

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

