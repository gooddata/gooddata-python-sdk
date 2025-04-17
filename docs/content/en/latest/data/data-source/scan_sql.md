---
title: "scan_sql"
linkTitle: "scan_sql"
weight: 210
superheading: "catalog_data_source."
---

{{< api-ref "sdk.CatalogDataSourceService.scan_sql" >}}

## Example

```python
# Scan sql
sdk.catalog_data_source.scan_sql(data_source_id="123", sql_request=ScanSqlRequest(sql="SELECT * FROM products"))
# ScanSqlResponse(
#   columns=[
#       ScanSqlColumn(data_type='STRING', name='category'),
#       ScanSqlColumn(data_type='INT', name='product_id'),
#       ScanSqlColumn(data_type='STRING', name='product_name')]
#   ],
#   data_preview=[
#       ['150', 'Skirt', 'Clothing'],
#       ['210', 'Artego', 'Electronics'],
#       ...
#   ]
#)
````
