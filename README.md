# GoodData.CN Python Foundations

This repository contains Python packages useful for integration with [GoodData Cloud Native](https://www.gooddata.com/developers/cloud-native/).

## Available packages

### API Clients

API clients are generated directly from GoodData.CN OpenAPI specifications and allow you to call any API from
Python. Learn more about the clients in their [dedicated readme](./clients_README.md).

### Python SDK

Python SDK is a layer of convenience and use-case oriented APIs that allows simple interaction with GoodData.CN.

Check out the [gooddata-sdk](./gooddata-sdk) documentation to learn more.

### GoodData.CN Foreign Data Wrapper for PostgreSQL

Foreign Data Wrapper (FDW) presents a way to map GoodData.CN semantic layer and/or insights stored in your GoodData.CN
into PostgreSQL as foreign tables that you can then query using SQL.

Check out the [gooddata-fdw package](./gooddata-fdw) documentation to learn more and get started.

### GoodData to pandas adapters

The [gooddata-pandas](./gooddata-pandas) is a thin layer that utilizes Python SDK and allows you to conveniently
create pandas series and data frames.

## Requirements

-  [GoodData.CN](https://www.gooddata.com/developers/cloud-native/) installation; either running on your cloud
   infrastructure or the free Community Edition running on your workstation

-  Python 3.7 or newer

-  The GoodData.CN Foreign Data Wrapper is tested with the latest version of multicorn (1.4.0) and PostgreSQL 12
