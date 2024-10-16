---
title: "get_declarative_notification_channels"
linkTitle: "get_declarative_notification_channels..."
weight: 190
no_list: true
superheading: "catalog_organization."
---



``get_declarative_notification_channels()``

Get all declarative notification channels in the current organization.

{{% parameters-block  title="Parameters" None="yes" %}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="list[CatalogDeclarativeNotificationChannel]" >}}
List of declarative notification channels.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
sdk.catalog_organization.get_declarative_notification_channels()
```
