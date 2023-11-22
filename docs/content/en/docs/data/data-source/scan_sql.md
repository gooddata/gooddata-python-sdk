---
title: "scan_sql"
linkTitle: "scan_sql"
weight: 210
superheading: "catalog_data_source."
---



``scan_sql(data_source_id: str, sql_request: ScanSqlRequest)``

Analyze SELECT SQL query in a given request. Return description of SQL result-set as list of column names with GoodData data types and list of example data returned by SELECT query.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data source identification string. e.g. "demo"
{{< /parameter >}}

{{< parameter p_name="sql_request" p_type="ScanSqlRequest" >}}
SELECT SQL query to analyze.
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}

{{< parameter p_type="ScanSqlResponse" >}}
SELECT query analysis result.
{{< /parameter >}}

{{% /parameters-block %}}

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
