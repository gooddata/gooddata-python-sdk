# (C) 2026 GoodData Corporation
"""Tests for the notification channel destination union.

`CatalogSmtp` / `CatalogDefaultSmtp` used to be commented out in the SDK with a
TODO pointing at the generated client: the composed destination model accepted a
single `type` only, so `to_api()` raised `ApiValueError` for every other
destination. That was the same oneOf-flattening defect covered by
`test_composed_oneof_unions.py`; with it fixed in `model_utils`, all four
destinations are usable and `NotificationChannelDestination.allowed_values` no
longer has to be monkeypatched at import time.
"""

from __future__ import annotations

import pytest
from gooddata_api_client.model.json_api_notification_channel_in_attributes_destination import (
    JsonApiNotificationChannelInAttributesDestination,
)
from gooddata_api_client.model.notification_channel_destination import NotificationChannelDestination
from gooddata_sdk import (
    CatalogDeclarativeNotificationChannel,
    CatalogDefaultSmtp,
    CatalogInPlatform,
    CatalogSmtp,
    CatalogWebhook,
)

DESTINATIONS = {
    "WEBHOOK": (
        CatalogWebhook(url="https://webhook.site/hook", token="secret"),
        {"type": "WEBHOOK", "url": "https://webhook.site/hook", "token": "secret"},
    ),
    "SMTP": (
        CatalogSmtp(
            from_email="sender@example.com",
            from_email_name="Sender",
            host="smtp.example.com",
            port=587,
            username="user",
            password="secret",
        ),
        {
            "type": "SMTP",
            "from_email": "sender@example.com",
            "from_email_name": "Sender",
            "host": "smtp.example.com",
            "port": 587,
            "username": "user",
            "password": "secret",
        },
    ),
    "DEFAULT_SMTP": (
        CatalogDefaultSmtp(from_email="sender@example.com", from_email_name="Sender"),
        {"type": "DEFAULT_SMTP", "from_email": "sender@example.com", "from_email_name": "Sender"},
    ),
    "IN_PLATFORM": (CatalogInPlatform(), {"type": "IN_PLATFORM"}),
}


@pytest.mark.parametrize("destination_type", sorted(DESTINATIONS))
def test_destination_to_api(destination_type: str) -> None:
    """Every destination must survive `to_api()`, not just WEBHOOK."""
    destination, expected = DESTINATIONS[destination_type]

    assert destination.to_api().to_dict() == expected


@pytest.mark.parametrize("destination_type", sorted(DESTINATIONS))
def test_notification_channel_to_api_carries_the_destination(destination_type: str) -> None:
    destination, expected = DESTINATIONS[destination_type]
    channel = CatalogDeclarativeNotificationChannel(
        id=f"channel-{destination_type.lower()}",
        name=f"Channel {destination_type}",
        destination=destination,
        allowed_recipients="CREATOR",
    )

    api_object = channel.to_api()

    assert api_object.to_dict()["destination"] == expected


@pytest.mark.parametrize("destination_type", sorted(DESTINATIONS))
def test_notification_channel_round_trips(destination_type: str) -> None:
    """`from_api` must rebuild the concrete destination class, not a webhook."""
    destination, _ = DESTINATIONS[destination_type]
    channel = CatalogDeclarativeNotificationChannel(
        id=f"channel-{destination_type.lower()}",
        name=f"Channel {destination_type}",
        destination=destination,
        custom_dashboard_url="https://dashboard.site",
        allowed_recipients="CREATOR",
    )

    restored = CatalogDeclarativeNotificationChannel.from_api(channel.to_dict(camel_case=False))

    assert restored == channel
    assert type(restored.destination) is type(destination)
    assert restored.destination is not None
    assert restored.destination.type == destination_type


def test_from_api_rejects_an_unknown_destination_type() -> None:
    with pytest.raises(ValueError, match="Unknown notification channel destination type: TELEPATHY"):
        CatalogDeclarativeNotificationChannel.from_api({"id": "channel", "destination": {"type": "TELEPATHY"}})


@pytest.mark.parametrize(
    "model",
    [NotificationChannelDestination, JsonApiNotificationChannelInAttributesDestination],
    ids=["shared", "json_api"],
)
@pytest.mark.parametrize("destination_type", sorted(DESTINATIONS))
def test_generated_destination_models_accept_every_type(model, destination_type: str) -> None:
    """Pin the generated composed models too - this is where the defect lived."""
    _, payload = DESTINATIONS[destination_type]

    destination = model(**payload)

    assert destination.type == destination_type


def test_destination_model_class_attribute_is_still_collapsed() -> None:
    """Guard the reason the monkeypatch could go: the fix is at validation time.

    The generator still writes a single-variant enum onto the composed parent -
    nothing regenerates that away - so this documents that the models above pass
    because `model_utils` unions the members, not because the class attribute
    got fixed.
    """
    collapsed = NotificationChannelDestination.allowed_values.get(("type",), {})

    assert len(collapsed) == 1
