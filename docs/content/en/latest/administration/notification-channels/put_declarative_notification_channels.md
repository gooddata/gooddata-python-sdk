---
title: "put_declarative_notification_channels"
linkTitle: "put_declarative_notification_channels..."
weight: 190
no_list: true
superheading: "catalog_organization."
---



``put_declarative_notification_channels(notification_channels: list[CatalogDeclarativeNotificationChannel])``

Put declarative notification channels in the current organization.

{{% parameters-block title="Parameters"%}}
{{< parameter p_name="notification_channels" p_type="list[CatalogDeclarativeNotificationChannel]" >}}
List of declarative notification channels.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
from gooddata_sdk import CatalogDeclarativeNotificationChannel, CatalogWebhook

notification_channels = [CatalogDeclarativeNotificationChannel(
    id="webhook", name="Webhook", destination=CatalogWebhook(url="https://webhook.site", token="123")
)]
sdk.catalog_organization.put_declarative_notification_channels()
```
