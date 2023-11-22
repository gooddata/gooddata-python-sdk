---
title: "Getting Started"
linkTitle: "Getting Started"
weight: 12
---

Start integrating GoodData into your Python application right now.

## Quick Start

1. [Install Python SDK](../installation/)

1. Ensure you have a running instance of GoodData. If you just want to try things out, we recommend you sign up for a [trial of GoodData Cloud](https://www.gooddata.com/trial/).

1. [Create a personal access token for GoodData API](https://www.gooddata.com/docs/cloud/getting-started/create-api-token/)

1. Import Python SDK into your script:

    ```python
    from gooddata_sdk import GoodDataSdk
    ```

1. Connect to your instance of GoodData using:

    ```python
    # GoodData base URL, e.g. "https://www.example.com"
    host = "https://www.example.com"
    token = "<your_personal_access_token>"
    sdk = GoodDataSdk.create(host, token)
    ```

    Alternatively, you can create the instance from a config file:

    ```python
    # The default path to the profiles.yaml file is set to `~/.gooddata/profiles.yaml`
    # It can be overridden with a custom path
    profiles= Path("~/my_directory/my_profiles.yaml")
    # Profile name defaults to `default. It can be overridden with a custom profile
    sdk = GoodDataSdk.create_from_profile(profile="staging", profiles_path=profiles)
    ```

    profiles.yaml file structure example:

    ```yaml
    default:
        host: http://localhost:3000
        token: YWRtaW46Ym9vdHN0cmFwOmFkbWluMTIz
        custom_headers: #optional
            Host: localhost
        extra_user_agent: xyz #optional
    ```

1. Start using Python SDK! For example, get a list of all workspaces:

    ```python
    workspaces = sdk.catalog_workspace.list_workspaces()
    print(workspaces)


    # [
    #   CatalogWorkspace(id=demo_west, name=Demo West),
    #   CatalogWorkspace(id=demo_west_california, name=Demo West California),
    #   CatalogWorkspace(id=demo, name=Demo)
    # ]
    ```

## About This Documentation

This documentation serves mostly as a referential documentation, altough, you will find example codes scattered throughout it.

### Reading the example code

The are two types of example codes in this documentation.

First is the __standalone__ and the second is the __snippet__ type. The main difference between those two types is that when working with the __standalone__, it contains all the necessary includes and variables used. Meaning, that after changing the __host__ and __token__ representing your URI and API token respectively, the code is executable. Where the __snippet__ type code does not contain any __import__ statements or __variable__ declarations, unless tightly tied to the method used.

{{% alert color="warning" title="Test in non-production environment" %}}
Unless you are sure what you are doing, we __highly__ reccommend you do not execute the Python SDK code examples on your __production__ GoodData account, as it may temper with your workspaces and dashboards.
{{% /alert %}}

#### Standalone type

 The __standalone__ code examples are contained in in the "navigation" parts of the documentation and are usually use-case oriented.

To be able to execute the code, simply replace **host** and **token** variables in the examples. After replacing these two variables with your credentials, you will be able to try the __standalone__ code examples as they are. We reccommend you work in **non_production** environment.

The __standalone__ code examples look as follows:
```python
from gooddata_sdk import GoodDataSdk

# GoodData base URL, e.g. "https://www.example.com"
host = "https://www.example.com"
# GoodData user token
token = "some_user_token"
sdk = GoodDataSdk.create(host, token)

workspace_id = "123"

# Read catalog for demo workspace
catalog = sdk.catalog_workspace_content.get_full_catalog(workspace_id)

# Print all dataset in the workspace
for dataset in catalog.datasets:
    print(dataset)

# Print all metrics in the workspace
for metric in catalog.metrics:
    print(metric)

# Read list of attributes for demo workspace
attributes = sdk.catalog_workspace_content.get_attributes_catalog(workspace_id)

# Read list of facts for demo workspace
facts = sdk.catalog_workspace_content.get_facts_catalog(workspace_id)
```

#### Snippet type

The __snippet__ examples on the other hand are made to be small and quickly digestable. They do NOT contain __import__ statements or __variable__ initialization.

```python
my_analytics_model = sdk.catalog_workspace_content.get_declarative_analytics_model("123")

# Modify the `CatalogDeclarativeAnalytics` object:
my_analytics_model.analytics.analytical_dashboards.clear()

# Put analytics model object back to the server:
sdk.catalog_workspace_content.put_declarative_analytics_model("123",my_analytics_model)
```
