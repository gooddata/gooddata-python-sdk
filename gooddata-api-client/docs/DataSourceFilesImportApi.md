# gooddata_api_client.DataSourceFilesImportApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**import_csv**](DataSourceFilesImportApi.md#import_csv) | **POST** /api/v1/actions/fileStorage/dataSources/{dataSourceId}/importCsv | Import CSV


# **import_csv**
> [ImportCsvResponse] import_csv(data_source_id, import_csv_request)

Import CSV

Import the CSV files at the given locations in the staging area to the final location.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_files_import_api
from gooddata_api_client.model.import_csv_request import ImportCsvRequest
from gooddata_api_client.model.import_csv_response import ImportCsvResponse
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_files_import_api.DataSourceFilesImportApi(api_client)
    data_source_id = "dataSourceId_example" # str | 
    import_csv_request = ImportCsvRequest(
        tables=[
            ImportCsvRequestTable(
                name="name_example",
                source=ImportCsvRequestTableSource(
                    config=ImportCsvRequestTableSourceConfig(
                        column_date_formats={
                            "key": "key_example",
                        },
                        convert_options=CsvConvertOptions(
                            auto_dict_encode=True,
                            auto_dict_max_cardinality=1,
                            check_utf8=True,
                            column_types=[
                                CsvConvertOptionsColumnType(
                                    name="name_example",
                                    nullable=True,
                                    type="type_example",
                                ),
                            ],
                            decimal_point="decimal_point_example",
                            false_values=[
                                "false_values_example",
                            ],
                            include_columns=[
                                "include_columns_example",
                            ],
                            include_missing_columns=True,
                            null_values=[
                                "null_values_example",
                            ],
                            quoted_strings_can_be_null=True,
                            strings_can_be_null=True,
                            timestamp_parsers=[
                                "timestamp_parsers_example",
                            ],
                            true_values=[
                                "true_values_example",
                            ],
                        ),
                        parse_options=CsvParseOptions(
                            delimiter="delimiter_example",
                            double_quote=True,
                            escape_char={},
                            ignore_empty_lines=True,
                            newlines_in_values=True,
                            quote_char={},
                        ),
                        read_options=CsvReadOptions(
                            auto_generate_column_names=True,
                            block_size=1,
                            column_names=[
                                "column_names_example",
                            ],
                            encoding="encoding_example",
                            skip_rows=1,
                            skip_rows_after_names=1,
                            use_threads=True,
                        ),
                    ),
                    location="location_example",
                ),
            ),
        ],
    ) # ImportCsvRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Import CSV
        api_response = api_instance.import_csv(data_source_id, import_csv_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceFilesImportApi->import_csv: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **data_source_id** | **str**|  |
 **import_csv_request** | [**ImportCsvRequest**](ImportCsvRequest.md)|  |

### Return type

[**[ImportCsvResponse]**](ImportCsvResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful import. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

