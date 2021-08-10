# gooddata_metadata_client.OrganizationControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_entity_cookie_security_configurations**](OrganizationControllerApi.md#get_entity_cookie_security_configurations) | **GET** /api/entities/admin/cookieSecurityConfigurations/{id} | 
[**get_entity_organizations**](OrganizationControllerApi.md#get_entity_organizations) | **GET** /api/entities/admin/organizations/{id} | 
[**update_entity_cookie_security_configurations**](OrganizationControllerApi.md#update_entity_cookie_security_configurations) | **PUT** /api/entities/admin/cookieSecurityConfigurations/{id} | 
[**update_entity_organizations**](OrganizationControllerApi.md#update_entity_organizations) | **PUT** /api/entities/admin/organizations/{id} | 


# **get_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument get_entity_cookie_security_configurations(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_controller_api
from gooddata_metadata_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_cookie_security_configurations(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_cookie_security_configurations(id, predicate=predicate, filter=filter)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_cookie_security_configurations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

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

# **get_entity_organizations**
> JsonApiOrganizationOutDocument get_entity_organizations(id)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_controller_api
from gooddata_metadata_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.get_entity_organizations(id)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.get_entity_organizations(id, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->get_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

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

# **update_entity_cookie_security_configurations**
> JsonApiCookieSecurityConfigurationOutDocument update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_controller_api
from gooddata_metadata_client.model.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument
from gooddata_metadata_client.model.json_api_cookie_security_configuration_in_document import JsonApiCookieSecurityConfigurationInDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_cookie_security_configuration_in_document = JsonApiCookieSecurityConfigurationInDocument(
        data=JsonApiCookieSecurityConfigurationIn(
            type="cookieSecurityConfiguration",
            id="id1",
            attributes=JsonApiCookieSecurityConfigurationInAttributes(
                last_rotation=dateutil_parser('1970-01-01T00:00:00.00Z'),
                rotation_interval="P30D",
            ),
        ),
    ) # JsonApiCookieSecurityConfigurationInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=lastRotation==InstantValue;rotationInterval==DurationValue" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_cookie_security_configurations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_cookie_security_configurations(id, json_api_cookie_security_configuration_in_document, predicate=predicate, filter=filter)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_cookie_security_configurations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_cookie_security_configuration_in_document** | [**JsonApiCookieSecurityConfigurationInDocument**](JsonApiCookieSecurityConfigurationInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]

### Return type

[**JsonApiCookieSecurityConfigurationOutDocument**](JsonApiCookieSecurityConfigurationOutDocument.md)

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

# **update_entity_organizations**
> JsonApiOrganizationOutDocument update_entity_organizations(id, json_api_organization_in_document)



### Example

```python
import time
import gooddata_metadata_client
from gooddata_metadata_client.api import organization_controller_api
from gooddata_metadata_client.model.json_api_organization_in_document import JsonApiOrganizationInDocument
from gooddata_metadata_client.model.json_api_organization_out_document import JsonApiOrganizationOutDocument
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_metadata_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_metadata_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = organization_controller_api.OrganizationControllerApi(api_client)
    id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | 
    json_api_organization_in_document = JsonApiOrganizationInDocument(
        data=JsonApiOrganizationIn(
            type="organization",
            id="id1",
            attributes=JsonApiOrganizationInAttributes(
                name="name_example",
                hostname="hostname_example",
                oauth_issuer_location="oauth_issuer_location_example",
                oauth_client_id="oauth_client_id_example",
                oauth_client_secret="oauth_client_secret_example",
            ),
        ),
    ) # JsonApiOrganizationInDocument | 
    predicate = {} # {str: (bool, date, datetime, dict, float, int, list, str, none_type)} | Composed query parameters used for filtering. 'id' parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name=John&language=english,czech&address.city=London&father.id=123). (optional)
    filter = "filter=name==someString;hostname==someString;bootstrapUser.id==321;bootstrapUserGroup.id==321" # str | Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title=='Some Title';description=='desc') (optional)
    include = [
        "include=bootstrapUser,bootstrapUserGroup",
    ] # [str] | Array of included collections or individual relationships. Includes are separated by commas (e.g. include=entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \"ALL\" is present, all possible includes are used (include=ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. (optional)

    # example passing only required values which don't have defaults set
    try:
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_organizations: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        api_response = api_instance.update_entity_organizations(id, json_api_organization_in_document, predicate=predicate, filter=filter, include=include)
        pprint(api_response)
    except gooddata_metadata_client.ApiException as e:
        print("Exception when calling OrganizationControllerApi->update_entity_organizations: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **id** | **str**|  |
 **json_api_organization_in_document** | [**JsonApiOrganizationInDocument**](JsonApiOrganizationInDocument.md)|  |
 **predicate** | [**{str: (bool, date, datetime, dict, float, int, list, str, none_type)}**](bool, date, datetime, dict, float, int, list, str, none_type.md)| Composed query parameters used for filtering. &#39;id&#39; parameter can be used for all objects. Other parameters are present according to object type (title, description,...). You can specify any object parameter and parameter of related entity up to 2nd level (for example name&#x3D;John&amp;language&#x3D;english,czech&amp;address.city&#x3D;London&amp;father.id&#x3D;123). | [optional]
 **filter** | **str**| Filtering parameter in RSQL. See https://github.com/jirutka/rsql-parser.You can specify any object parameter and parameter of related entity up to 2nd level (for example title&#x3D;&#x3D;&#39;Some Title&#39;;description&#x3D;&#x3D;&#39;desc&#39;) | [optional]
 **include** | **[str]**| Array of included collections or individual relationships. Includes are separated by commas (e.g. include&#x3D;entity1s,entity2s). Collection include represents the inclusion of every relationship between this entity and the given collection. Relationship include represents the inclusion of the particular relationships only. If single parameter \&quot;ALL\&quot; is present, all possible includes are used (include&#x3D;ALL).  __WARNING:__ Individual include types (collection, relationship or ALL) cannot be combined together. | [optional]

### Return type

[**JsonApiOrganizationOutDocument**](JsonApiOrganizationOutDocument.md)

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

