---
title: "load_and_put_declarative_data_sources"
linkTitle: "load_and_put_declarative_data..."
weight: 110
superheading: "catalog_data_source."
---



``load_and_put_declarative_data_sources(layout_root_path: Path = Path.cwd(), credentials_path: Optional[Path] = None, test_data_sources: bool = False)``

This method combines [load_declarative_data_sources](../load_and_put_declarative_data_sources/) and [put_declarative_data_sources](../put_declarative_data_sources/) methods to load and set layouts stored using [store_declarative_data_sources](../store_declarative_data_sources/).

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="layout_root_path" p_type="CatalogDeclarativeDataSources" >}}
Path to the root of the layout directory. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="credentials_path" p_type="Optional[Path]" >}}
Path to the credentials. Defaults to Path.cwd().
{{< /parameter >}}
{{< parameter p_name="test_data_sources" p_type="Optional[Bool]" >}}
If True, the connection of data sources is tested. Defaults to False.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

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
