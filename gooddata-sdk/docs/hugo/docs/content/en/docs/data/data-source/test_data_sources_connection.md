---
title: "test_data_sources_connection"
linkTitle: "test_data_sources_connection"
weight: 220
superheading: "catalog_data_source."
---

<!-- TODO -->

``test_data_sources_connection(declarative_data_sources: CatalogDeclarativeDataSources, credentials_path: Optional[Path] = None)``

Tests connection to declarative data sources. If *credentials_path* is omitted then the connection is tested with empty credentials.
In case some connection failed the ValueError is raised with information about why the connection to the data source failed, e.g. host unreachable or invalid login or password.

**Example of credentials YAML file:**

    data_sources:
        demo-test-ds: "demopass"
        demo-bigquery-ds: "~/home/secrets.json"

## Example

```Python
# Get data sources
declarative_data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Test data source connection
sdk.catalog_data_source.test_data_sources_connection(
    declarative_data_sources=declarative_data_sources,
    credentials_path=Path("credentials")
)
```
