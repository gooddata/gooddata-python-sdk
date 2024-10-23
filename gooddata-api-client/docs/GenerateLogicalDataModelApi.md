# gooddata_api_client.GenerateLogicalDataModelApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**generate_logical_model**](GenerateLogicalDataModelApi.md#generate_logical_model) | **POST** /api/v1/actions/dataSources/{dataSourceId}/generateLogicalModel | Generate logical data model (LDM) from physical data model (PDM)


# **generate_logical_model**
> DeclarativeModel generate_logical_model(data_source_id, generate_ldm_request)

Generate logical data model (LDM) from physical data model (PDM)

Generate logical data model (LDM) from physical data model (PDM) stored in data source.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import generate_logical_data_model_api
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
    api_instance = generate_logical_data_model_api.GenerateLogicalDataModelApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    generate_ldm_request = GenerateLdmRequest(
        date_granularities="all",
        denorm_prefix="dr",
        fact_prefix="f",
        generate_long_ids=False,
        grain_multivalue_reference_prefix="grmr",
        grain_prefix="gr",
        grain_reference_prefix="grr",
        multivalue_reference_prefix="mr",
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
            table_overrides=[
                TableOverride(
                    columns=[
                        ColumnOverride(
                            label_target_column="users",
                            label_type="HYPERLINK",
                            ldm_type_override="FACT",
                            name="column_name",
                        ),
                    ],
                    path=["schema","table_name"],
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
        secondary_label_prefix="ls",
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
        print("Exception when calling GenerateLogicalDataModelApi->generate_logical_model: %s\n" % e)
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

