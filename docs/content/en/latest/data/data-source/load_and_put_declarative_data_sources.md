---
title: "load_and_put_declarative_data_sources"
linkTitle: "load_and_put_declarative_data..."
weight: 110
superheading: "catalog_data_source."
---

{{< api-ref "sdk.CatalogDataSourceService.load_and_put_declarative_data_sources" >}}

## Example

The load and put can be done two ways.

Either by one call:

```python
# Load and put declarative data sources
sdk.catalog_data_source.load_and_put_declarative_data_sources(
    layout_root_path=Path("abc"),
    credentials_path=Path("credentials")
)
```
Or by two separate calls:

```python
# Load the data source
data_sources = sdk.catalog_data_source.get_declarative_data_sources()

# Put the data source
sdk.catalog_data_source.put_declarative_data_sources(
    declarative_data_sources=data_sources
    layout_root_path=Path("abc"),
    credentials_path=Path("credentials")
)
```

Example of the credential file:

```yaml
data_sources:
  demo-test-ds: "demopass"
  demo-bigquery-ds: "~/home/secrets.json"
```

The result is identical.
