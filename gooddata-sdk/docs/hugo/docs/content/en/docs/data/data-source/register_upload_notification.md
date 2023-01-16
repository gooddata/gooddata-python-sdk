---
title: "register_upload_notification"
linkTitle: "register_upload_notification"
weight: 180
superheading: "catalog_data_source."
---

<!-- TODO -->

``register_upload_notification(data_source_id: str)``

Invalidate cache of your computed reports to force your analytics to be recomputed.

{{% parameters-block  title="Parameters"%}}

{{< parameter p_name="data_source_id" p_type="string" >}}
Data Source identification string. e.g. "demo"
{{< /parameter >}}

{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes"%}}
{{% /parameters-block %}}

## Example

```Python
# Recompute analytics by invalidating cache
sdk.catalog_data_source.register_upload_notification(data_source_id="123")
```
